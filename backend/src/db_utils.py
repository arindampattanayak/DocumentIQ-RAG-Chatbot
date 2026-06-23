from datetime import datetime
from pathlib import Path
import logging
import os
from typing import Optional

from bson.objectid import ObjectId
from dotenv import load_dotenv
from pymongo import MongoClient
from pymongo.errors import ConnectionFailure
from langchain_core.messages import HumanMessage, AIMessage

load_dotenv(dotenv_path=Path(__file__).resolve().parent.parent / ".env")

DB_URI = os.getenv("DB_URI")
DB_NAME = os.getenv("DB_NAME")

if not DB_URI:
    raise ValueError("DB_URI not found in environment variables.")
if not DB_NAME:
    raise ValueError("DB_NAME not found in environment variables.")

LOG_FILE = Path(__file__).resolve().parent.parent / "app.log"
logging.basicConfig(
    filename=str(LOG_FILE),
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
)


def get_db_connection():
    try:
        client = MongoClient(DB_URI)
        client.admin.command("ping")
        return client[DB_NAME]
    except ConnectionFailure as e:
        logging.error(f"Failed to connect to MongoDB: {str(e)}")
        raise


def initialize_database():
    db = get_db_connection()

    db.users.create_index("email", unique=True)

    db.application_logs.create_index("user_id")
    db.application_logs.create_index("session_id")
    db.application_logs.create_index("created_at")
    logging.info("Indexes created for application_logs collection.")

    db.document_store.create_index([("user_id", 1), ("filename", 1)], unique=True)
    db.document_store.create_index("upload_timestamp")
    logging.info("Indexes created for document_store collection.")

    logging.info("Database initialization complete.")


# -------------------------
# Users
# -------------------------
def create_user(name: str, email: str, password_hash: str):
    db = get_db_connection()
    result = db.users.insert_one(
        {
            "name": name.strip(),
            "email": email.lower().strip(),
            "password_hash": password_hash,
            "created_at": datetime.utcnow(),
        }
    )
    return str(result.inserted_id)


def get_user_by_email(email: str):
    db = get_db_connection()
    user = db.users.find_one({"email": email.lower()})
    if not user:
        return None
    return {
        "id": str(user["_id"]),
        "name": user.get("name", ""),
        "email": user["email"],
        "password_hash": user["password_hash"],
        "created_at": user.get("created_at"),
    }


def get_user_by_id(user_id: str):
    db = get_db_connection()
    try:
        obj_id = ObjectId(user_id)
    except Exception:
        return None

    user = db.users.find_one({"_id": obj_id})
    if not user:
        return None

    return {
        "id": str(user["_id"]),
        "name": user.get("name", ""),
        "email": user["email"],
        "password_hash": user["password_hash"],
        "created_at": user.get("created_at"),
    }


# -------------------------
# Chat logs
# -------------------------
def insert_application_logs(user_id, session_id, user_query, gpt_response, model):
    db = get_db_connection()
    db.application_logs.insert_one(
        {
            "user_id": str(user_id),
            "session_id": session_id,
            "user_query": user_query,
            "gpt_response": gpt_response,
            "model": model,
            "created_at": datetime.utcnow(),
        }
    )
    logging.info("Chat log inserted successfully.")


def get_chat_history(user_id: str, session_id: Optional[str] = None):
    db = get_db_connection()
    query = {"user_id": str(user_id)}
    if session_id:
        query["session_id"] = session_id

    logs = db.application_logs.find(query).sort("created_at", 1)

    messages = []
    for log in logs:
        messages.append(HumanMessage(content=log["user_query"]))
        messages.append(AIMessage(content=log["gpt_response"]))

    return messages


def get_chat_logs(user_id: str, session_id: Optional[str] = None):
    db = get_db_connection()
    query = {"user_id": str(user_id)}
    if session_id:
        query["session_id"] = session_id

    logs = db.application_logs.find(query).sort("created_at", -1)

    return [
        {
            "session_id": log["session_id"],
            "user_query": log["user_query"],
            "gpt_response": log["gpt_response"],
            "model": log["model"],
            "created_at": log["created_at"],
        }
        for log in logs
    ]


def get_user_sessions(user_id: str):
    db = get_db_connection()
    pipeline = [
        {"$match": {"user_id": str(user_id)}},
        {
            "$group": {
                "_id": "$session_id",
                "last_activity": {"$max": "$created_at"},
                "message_count": {"$sum": 1},
            }
        },
        {"$sort": {"last_activity": -1}},
    ]

    result = db.application_logs.aggregate(pipeline)

    return [
        {
            "session_id": item["_id"],
            "last_activity": item["last_activity"],
            "message_count": item["message_count"],
        }
        for item in result
    ]


# -------------------------
# Documents
# -------------------------
def insert_document_record(filename: str, user_id: str):
    db = get_db_connection()
    document = {
        "user_id": str(user_id),
        "filename": filename,
        "upload_timestamp": datetime.utcnow(),
    }
    result = db.document_store.insert_one(document)
    return str(result.inserted_id)


def delete_document_record(file_id: str, user_id: str):
    db = get_db_connection()
    try:
        obj_id = ObjectId(file_id)
    except Exception as e:
        logging.error(f"Invalid file_id: {file_id}, error: {str(e)}")
        return False

    result = db.document_store.delete_one({"_id": obj_id, "user_id": str(user_id)})
    logging.info(
        f"Delete result for file_id {file_id}: deleted_count={result.deleted_count}"
    )
    return result.deleted_count > 0


def get_all_documents(user_id: str):
    db = get_db_connection()
    documents = db.document_store.find({"user_id": str(user_id)}).sort("upload_timestamp", -1)

    return [
        {
            "id": str(doc["_id"]),
            "filename": doc["filename"],
            "upload_timestamp": doc["upload_timestamp"],
        }
        for doc in documents
    ]