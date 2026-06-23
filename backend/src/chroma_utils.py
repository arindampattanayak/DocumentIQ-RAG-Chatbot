import logging
import os
from pathlib import Path
from typing import List

from langchain_community.document_loaders import (
    PyPDFLoader,
    Docx2txtLoader,
    UnstructuredHTMLLoader,
)
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma
from langchain_core.documents import Document

LOG_FILE = Path(__file__).resolve().parent.parent / "app.log"
logging.basicConfig(
    filename=str(LOG_FILE),
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
)

BACKEND_DIR = Path(__file__).resolve().parent.parent
PERSIST_DIR = BACKEND_DIR / "data" / "chroma_db"

logging.info(f"Setting Chroma persist directory to: {PERSIST_DIR}")

PERSIST_DIR.mkdir(parents=True, exist_ok=True)

embedding_function = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)

vectorstore = Chroma(
    persist_directory=str(PERSIST_DIR),
    embedding_function=embedding_function,
    collection_name="rag_docs",
)

text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=1000,
    chunk_overlap=300,
    length_function=len,
)


def load_and_split_document(file_path: str) -> List[Document]:
    logging.info(f"Attempting to load and split document from: {file_path}")
    file_path_lower = file_path.lower()

    if file_path_lower.endswith(".pdf"):
        loader = PyPDFLoader(file_path)
    elif file_path_lower.endswith(".docx"):
        loader = Docx2txtLoader(file_path)
    elif file_path_lower.endswith(".html"):
        loader = UnstructuredHTMLLoader(file_path)
    else:
        raise ValueError(f"Unsupported file type: {file_path}")

    documents = loader.load()
    split_docs = text_splitter.split_documents(documents)
    return split_docs


def index_document_to_chroma(file_path: str, file_id: str, user_id: str) -> bool:
    try:
        splits = load_and_split_document(file_path)

        for split in splits:
            split.metadata["file_id"] = str(file_id)
            split.metadata["user_id"] = str(user_id)

        vectorstore.add_documents(splits)
        logging.info(f"Indexed {len(splits)} chunks for file_id={file_id}, user_id={user_id}")
        return True

    except Exception as e:
        logging.error(f"Error indexing document {file_path}: {str(e)}")
        return False


def delete_doc_from_chroma(file_id: str) -> bool:
    try:
        file_id = str(file_id)
        logging.info(f"Attempting to delete documents with file_id: {file_id}")

        docs = vectorstore.get(where={"file_id": file_id})
        count = len(docs.get("ids", []))
        logging.info(f"Found {count} document chunks for file_id={file_id}")

        if count == 0:
            logging.info(f"No Chroma chunks found for file_id={file_id}")
            return True

        vectorstore.delete(where={"file_id": file_id})

        logging.info(f"Deleted Chroma chunks for file_id={file_id}")
        logging.info(f"Chroma collection count after deletion: {vectorstore._collection.count()}")
        return True

    except Exception as e:
        logging.error(f"Error deleting document from Chroma: {str(e)}")
        return False