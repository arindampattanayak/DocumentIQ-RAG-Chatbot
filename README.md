## 📚 **DocumentIQ-RAG-Chatbot** 

## **📖 Overview** 

DocumentIQ-RAG-Chatbot is an AI-powered Retrieval-Augmented Generation (RAG) application that enables users to upload documents, build a searchable knowledge base, and interact with their documents through natural language conversations. 

The application combines semantic document retrieval using ChromaDB with Google's Gemini 2.5 Flash model to generate accurate, context-aware responses. Users can upload PDF, DOCX, and HTML files, which are automatically processed, embedded, and indexed for efficient information retrieval. 

## **📖 Features** 

- 📄 Upload and process PDF, DOCX, and HTML documents 

- 🔍 Semantic search using vector embeddings 

- 📄 Context-aware responses powered by Gemini 2.5 Flash 

- 📄 Retrieval-Augmented Generation (RAG) pipeline using LangChain 

- 📄 Persistent chat history stored in MongoDB 

- 📚 Document indexing and management 

- ⚡ FastAPI backend for high-performance API handling 

- 📄 Modern React-based user interface 

- 🗑️ Delete and manage uploaded documents 

- ⚙️ Configurable retrieval and generation parameters 


## **Tech Stack** 🛠️

**Category Technology** Frontend React.js Backend FastAPI Database MongoDB Vector Store ChromaDB LLM Gemini 2.5 Flash Embedding Model all-MiniLM-L6-v2 Framework LangChain Language Python 3.11.11 

## **📖 Core Components** 

## **📖 Large Language Model** 

## **Gemini 2.5 Flash** 

Used for generating intelligent, context-aware responses based on retrieved document chunks. 

## 🔍 **Embedding Model** 

## **all-MiniLM-L6-v2** 

Generates dense vector embeddings from document text for efficient semantic search and retrieval. 

## **Vector Database** 🗄️� 

## **ChromaDB** 

Stores document embeddings and performs similarity searches to retrieve the most relevant document chunks. 

## **📖 Database** 

## **MongoDB** 

Stores: 

- Chat history 

- Conversation logs 

- Uploaded document metadata 

- Document indexing information 

## 📚 **LangChain Components** 

## **Document Loaders** 

- PyPDFLoader – Extracts text from PDF files 

- Docx2txtLoader – Processes DOCX documents 

- UnstructuredHTMLLoader – Extracts content from HTML files 

## **Text Splitter** 

- RecursiveCharacterTextSplitter 

Splits large documents into manageable chunks while preserving contextual information. 

## **⚙️� How It Works** 

1. User uploads a document. 

2. LangChain loads and extracts text from the document. 

3. The document is split into smaller chunks. 

4. Chunks are converted into embeddings using all-MiniLM-L6-v2. 

5. Embeddings are stored in ChromaDB. 

6. User submits a query through the chat interface. 

7. Relevant document chunks are retrieved using semantic search. 

8. Retrieved context is passed to Gemini 2.5 Flash. 

9. The model generates a context-aware response. 

10. Chat history and metadata are stored in MongoDB. 

## 📋 **Prerequisites** 

Before running the application, ensure you have: 

- Python 3.11.11 

- Node.js and npm 

- MongoDB (Local or MongoDB Atlas) 

- Google Gemini API Key 

## **📖 Environment Variables** 

Create a .env file inside the **backend** directory and add the following: 

DB_URI=your_mongodb_connection_string 

DB_NAME=your_database_name 

GEMINI_API_KEY=your_gemini_api_key 

API_URL=http://localhost:8000 FRONTEND_URL=http://localhost:5173 

RETRIEVER_K=5 

LLM_TEMPERATURE=0.7 

## **Environment Variable Description** 

**Variable Description** DB_URI MongoDB connection string DB_NAME MongoDB database name GEMINI_API_KEY Google Gemini API key API_URL Backend API URL FRONTEND_URL Frontend application URL RETRIEVER_K Number of document chunks retrieved LLM_TEMPERATURE Controls response creativity 

## **📖 Installation** 

## **1️⃣ Clone the Repository** 

git clone <repository-url> 

cd DocumentIQ-RAG-Chatbot 

## **2 Create a Virtual Environment** 

python -m venv venv 

## **3️⃣ Activate the Virtual Environment** 

## **Linux / macOS** 

source venv/bin/activate 

## **Windows** 

venv\Scripts\activate 

## **4️⃣ Install Backend Dependencies** 

pip install -r requirements.txt 

## **5 Install Frontend Dependencies** 

npm install 

## **▶️� Running the Application** 

## **Start the Backend** 

Open a terminal: 

source venv/bin/activate 

cd backend 

uvicorn src.main:app --reload 

Backend URL: http://localhost:8000 

## **Start the Frontend** 

Open a new terminal: 

npm run dev 

Frontend URL: http://localhost:5173 

## **📖 Project Structure** 

DocumentIQ-RAG-Chatbot/ 

│ 

├── backend/ 

│   ├── src/ 

│   ├── uploads/ 

│   ├── chroma_db/ 

│   ├── requirements.txt 

│   └── .env 

│ 

├── frontend/ 

│   ├── src/ 

│   ├── public/ 

- │   ├── package.json 

- │   └── vite.config.js 

│ 

├── Images/ 

│   └── RAG.png 

│ 

├── README.md 

│ 

└── venv/ 

## **📖 Example Use Cases** 

- Research Paper Question Answering 

- Company Knowledge Base Assistant 

- Legal Document Exploration 

- Academic Study Assistant 

- Technical Documentation Search 

- Internal Enterprise Knowledge Management 



## **📖 Author** 

## **Arindam Pattanayak** 


