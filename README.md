# DocumentIQ – LangChain-Powered RAG Document Intelligence Platform

## Project Overview
The LangChain RAG Chatbot is an AI-powered, document-aware conversational system built using Retrieval-Augmented Generation (RAG).
It allows users to upload documents (PDF, DOCX, HTML), index their content using vector embeddings, and interact with a chatbot that provides accurate, context-aware, and document-grounded responses.

Instead of relying solely on a language model’s internal knowledge, the chatbot retrieves relevant information from uploaded documents at query time, significantly reducing hallucinations and improving answer reliability.

The application follows a modern, production-style architecture, with a FastAPI backend, Streamlit frontend, vector database for semantic retrieval, and persistent storage for chat history.

## Key Capabilities

📄 Upload and index documents in multiple formats

🔍 Semantic document search using vector embeddings

💬 Conversational question answering grounded in documents

🧠 Context-aware multi-turn conversations

🗂️ Persistent chat history and document metadata

🎙️ Voice and text-based interaction support

🔐 Secure API key and configuration management

## Tech Stack
## Frontend

### Streamlit
Interactive web UI for chat, document upload, and management.

## Backend

### FastAPI
REST API for handling document ingestion, indexing, chat queries, and database operations.

### Uvicorn
ASGI server for running FastAPI.

## Databases

### MongoDB
Stores:

Chat conversation history (session-based)

Uploaded document metadata (filename, timestamps)

### ChromaDB
Vector database used for semantic similarity search over document embeddings.

## AI & LLM

### LangChain
Orchestrates the RAG pipeline, retrieval chains, prompt templates, and conversational context.

### Google Generative AI – Gemini-1.5-Flash
Large Language Model used for answer generation.

### HuggingFace all-MiniLM-L6-v2
Embedding model used to convert document chunks and user queries into dense vectors.

## Document Processing

### PyPDFLoader 
PDF text extraction

### Docx2txtLoader 
DOCX file processing

### UnstructuredHTMLLoader 
HTML content parsing

## Utilities

### SpeechRecognition  
Voice-to-text input

### Python-Dotenv 
Environment variable management

### Pydantic 
Request/response validation

### Requests 
Frontend ↔ backend communication


## Features

## Document Upload
Upload PDF, DOCX, or HTML documents via the interface for processing and indexing.

## Document Indexing
Documents are split into semantic chunks, embedded using all-MiniLM-L6-v2, and stored in ChromaDB for efficient retrieval.

## Conversational Chat Interface
Interact with uploaded documents through a chat-based interface to ask questions and receive detailed, context-aware responses.

## Retrieval-Augmented Generation (RAG)
Combines semantic document retrieval from ChromaDB with response generation using Google Gemini (LLM).

## Chat History Persistence
Maintains session-based conversation history using MongoDB, enabling multi-turn contextual interactions.

## Model Selection
Supports configurable language model selection (currently Gemini-1.5-Flash) for response generation.

## Document Management
View, manage, and delete uploaded documents directly from the interface.

## Environment Variables

```env
DB_URI=mongodb://localhost:27017
DB_NAME=rag_chatbot
GEMINI_API_KEY=your_google_gemini_api_key
API_URL=http://localhost:8000
RETRIEVER_K=5
LLM_TEMPERATURE=0.7
```
