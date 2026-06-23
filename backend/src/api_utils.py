from dotenv import load_dotenv
import os
import requests

# Load environment variables
load_dotenv()

API_URL = os.getenv("API_URL", "http://127.0.0.1:8000")


def get_api_response(question, session_id=None, model="gemini-2.5-flash"):
    headers = {
        "accept": "application/json",
        "Content-Type": "application/json",
    }

    data = {
        "question": question,   # must match backend QueryInput
        "model": model
    }

    if session_id:
        data["session_id"] = session_id

    try:
        response = requests.post(
            f"{API_URL}/chat",
            headers=headers,
            json=data,
            timeout=120,
        )

        if response.status_code != 200:
            print(f"Chat API Error: {response.status_code} - {response.text}")
            return None

        return response.json()

    except requests.exceptions.RequestException as e:
        print(f"Chat API Error: {str(e)}")
        return None


def upload_document(file):
    try:
        files = {
            "file": (file.name, file, file.type)
        }

        response = requests.post(
            f"{API_URL}/upload-doc",
            files=files,
            timeout=300,
        )

        if response.status_code != 200:
            print(f"Upload API Error: {response.status_code} - {response.text}")
            return None

        return response.json()

    except requests.exceptions.RequestException as e:
        print(f"Upload API Error: {str(e)}")
        return None


def list_documents():
    try:
        response = requests.get(
            f"{API_URL}/list-docs",
            timeout=60,
        )

        if response.status_code != 200:
            print(f"List Documents API Error: {response.status_code} - {response.text}")
            return []

        return response.json()

    except requests.exceptions.RequestException as e:
        print(f"List Documents API Error: {str(e)}")
        return []


def delete_document(file_id):
    try:
        response = requests.delete(
            f"{API_URL}/delete-doc",
            params={"file_id": file_id},
            timeout=60,
        )

        if response.status_code != 200:
            print(f"Delete API Error: {response.status_code} - {response.text}")
            return None

        return response.json()

    except requests.exceptions.RequestException as e:
        print(f"Delete API Error: {str(e)}")
        return None