from fastapi import FastAPI, File, UploadFile, HTTPException, Query, Depends
from fastapi.middleware.cors import CORSMiddleware
from pathlib import Path
import os
import uuid
import logging
import shutil

from src.auth_routes import router as auth_router
from src.dependencies import get_current_user
from src.pydantic_models import (
    QueryInput,
    QueryResponse,
    DocumentInfo,
    MessageHistoryItem,
    SessionSummary,
)
from src.langchain_utils import get_rag_chain
from src.db_utils import (
    insert_application_logs,
    get_chat_history,
    get_chat_logs,
    get_user_sessions,
    get_all_documents,
    insert_document_record,
    delete_document_record,
    initialize_database,
)
from src.chroma_utils import index_document_to_chroma, delete_doc_from_chroma

logging.basicConfig(
    filename="app.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
)

app = FastAPI(title="RAG-VOICE API")

# CORS for React frontend
origins = [
    "http://localhost:5173",
    "http://127.0.0.1:5173",
]

frontend_url = os.getenv("FRONTEND_URL")
if frontend_url:
    origins.append(frontend_url)

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_router)

@app.on_event("startup")
def startup_event():
    initialize_database()


@app.get("/health")
def health_check():
    return {"status": "ok"}


@app.post("/chat", response_model=QueryResponse)
def chat(query_input: QueryInput, current_user=Depends(get_current_user)):
    try:
        session_id = query_input.session_id or str(uuid.uuid4())

        chat_history = get_chat_history(current_user["id"], session_id)
        rag_chain = get_rag_chain(
            model=query_input.model.value,
            user_id=current_user["id"],
        )

        result = rag_chain.invoke(
            {
                "input": query_input.question,
                "chat_history": chat_history,
            }
        )

        answer = result["answer"]

        insert_application_logs(
            current_user["id"],
            session_id,
            query_input.question,
            answer,
            query_input.model.value,
        )

        return QueryResponse(
            answer=answer,
            session_id=session_id,
            model=query_input.model,
        )

    except Exception as e:
        logging.exception(f"Error in /chat endpoint: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/upload-doc")
def upload_and_index_document(
    file: UploadFile = File(...),
    current_user=Depends(get_current_user),
):
    allowed_extensions = [".pdf", ".docx", ".html"]
    file_extension = os.path.splitext(file.filename)[1].lower()

    if file_extension not in allowed_extensions:
        raise HTTPException(
            status_code=400,
            detail=f"Unsupported file type. Allowed types are: {', '.join(allowed_extensions)}",
        )

    documents_dir = Path("data/documents")
    documents_dir.mkdir(parents=True, exist_ok=True)

    temp_file_path = documents_dir / f"temp_{file.filename}"

    try:
        with open(temp_file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        file_id = insert_document_record(file.filename, current_user["id"])
        success = index_document_to_chroma(
            str(temp_file_path),
            file_id,
            current_user["id"],
        )

        if success:
            return {
                "message": f"File {file.filename} uploaded and indexed.",
                "file_id": file_id,
            }

        delete_document_record(file_id, current_user["id"])
        raise HTTPException(status_code=500, detail=f"Failed to index {file.filename}.")

    except Exception as e:
        logging.exception(f"Error in /upload-doc endpoint: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

    finally:
        if temp_file_path.exists():
            temp_file_path.unlink()


@app.get("/list-docs", response_model=list[DocumentInfo])
def list_documents(current_user=Depends(get_current_user)):
    try:
        return get_all_documents(current_user["id"])
    except Exception as e:
        logging.exception(f"Error in /list-docs endpoint: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@app.delete("/delete-doc")
def delete_document(
    file_id: str = Query(...),
    current_user=Depends(get_current_user),
):
    try:
        chroma_delete_success = delete_doc_from_chroma(file_id)
        if not chroma_delete_success:
            raise HTTPException(
                status_code=500,
                detail=f"Failed to delete document with file_id {file_id} from Chroma.",
            )

        db_delete_success = delete_document_record(file_id, current_user["id"])
        if db_delete_success:
            return {
                "message": f"Successfully deleted document with file_id {file_id}."
            }

        raise HTTPException(
            status_code=500,
            detail=f"Deleted from Chroma but failed to delete file_id {file_id} from DB.",
        )

    except Exception as e:
        logging.exception(f"Error in /delete-doc endpoint: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/history", response_model=list[MessageHistoryItem])
def get_history(current_user=Depends(get_current_user)):
    try:
        return get_chat_logs(current_user["id"])
    except Exception as e:
        logging.exception(f"Error in /history endpoint: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/sessions", response_model=list[SessionSummary])
def get_sessions(current_user=Depends(get_current_user)):
    try:
        return get_user_sessions(current_user["id"])
    except Exception as e:
        logging.exception(f"Error in /sessions endpoint: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))