### LangChain RAG Chatbot – Document Intelligence System

### Project Overview
The LangChain RAG Chatbot is an AI-powered, document-aware conversational system built using Retrieval-Augmented Generation (RAG).
It allows users to upload documents (PDF, DOCX, HTML), index their content using vector embeddings, and interact with a chatbot that provides accurate, context-aware, and document-grounded responses.

Instead of relying solely on a language model’s internal knowledge, the chatbot retrieves relevant information from uploaded documents at query time, significantly reducing hallucinations and improving answer reliability.

The application follows a modern, production-style architecture, with a FastAPI backend, Streamlit frontend, vector database for semantic retrieval, and persistent storage for chat history.

### Key Capabilities

📄 Upload and index documents in multiple formats

🔍 Semantic document search using vector embeddings

💬 Conversational question answering grounded in documents

🧠 Context-aware multi-turn conversations

🗂️ Persistent chat history and document metadata

🎙️ Voice and text-based interaction support

🔐 Secure API key and configuration management

### Tech Stack
## Frontend

Streamlit
Interactive web UI for chat, document upload, and management.

## Backend

FastAPI
REST API for handling document ingestion, indexing, chat queries, and database operations.

Uvicorn
ASGI server for running FastAPI.

## Databases

MongoDB
Stores:

Chat conversation history (session-based)

Uploaded document metadata (filename, timestamps)

ChromaDB
Vector database used for semantic similarity search over document embeddings.

## AI & NLP

LangChain
Orchestrates the RAG pipeline, retrieval chains, prompt templates, and conversational context.

Google Generative AI – Gemini-1.5-Flash
Large Language Model used for answer generation.

HuggingFace all-MiniLM-L6-v2
Embedding model used to convert document chunks and user queries into dense vectors.

## Document Processing

PyPDFLoader – PDF text extraction

Docx2txtLoader – DOCX file processing

UnstructuredHTMLLoader – HTML content parsing

## Utilities

SpeechRecognition – Voice-to-text input

Python-Dotenv – Environment variable management

Pydantic – Request/response validation

Requests – Frontend ↔ backend communication


### Features

Document Upload: Users can upload PDF, DOCX, or HTML files via the Streamlit sidebar, which are then processed and indexed.
Document Indexing: Uploaded documents are split into chunks, embedded using all-MiniLM-L6-v2, and stored in ChromaDB for retrieval.
Chat Interface: A conversational interface where users can ask questions about uploaded documents and receive detailed responses.
Retrieval-Augmented Generation (RAG): Combines document retrieval from ChromaDB with response generation via Gemini-1.5-Flash.
Chat History: Persists and displays the conversation history for each session, stored in MongoDB.
Model Selection: Allows users to choose the language model (currently Gemini-1.5-Flash) for response generation.
Document Management: View a list of uploaded documents and delete them as needed through the sidebar.

### Environment Variables

DB_URI=mongodb://localhost:27017
DB_NAME=rag_chatbot
GEMINI_API_KEY=your_google_gemini_api_key
API_URL=http://localhost:8000
RETRIEVER_K=5
LLM_TEMPERATURE=0.7
