import os
from pathlib import Path

from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.chains import create_history_aware_retriever, create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder

from src.chroma_utils import vectorstore

load_dotenv(dotenv_path=Path(__file__).resolve().parent.parent / ".env")

GOOGLE_API_KEY = os.getenv("GEMINI_API_KEY")
if not GOOGLE_API_KEY:
    raise ValueError("GEMINI_API_KEY not found in environment variables.")

RETRIEVER_K = int(os.getenv("RETRIEVER_K", "5"))
LLM_TEMPERATURE = float(os.getenv("LLM_TEMPERATURE", "0.7"))
DEFAULT_MODEL = os.getenv("GEMINI_MODEL", "gemini-2.5-flash")

contextualize_q_system_prompt = os.getenv(
    "CONTEXTUALIZE_Q_PROMPT",
    (
        "Given a chat history and the latest user question, which might reference context in the chat history, "
        "formulate a standalone question that can be understood without the chat history. "
        "Do NOT answer the question. Just reformulate it if needed."
    ),
)

contextualize_q_prompt = ChatPromptTemplate.from_messages(
    [
        ("system", contextualize_q_system_prompt),
        MessagesPlaceholder("chat_history"),
        ("human", "{input}"),
    ]
)

qa_prompt = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            "You are a helpful AI assistant. Use the provided context to answer the user's question clearly and in detail. "
            "If the context does not contain the answer, say you do not know.",
        ),
        ("system", "Context:\n{context}"),
        MessagesPlaceholder(variable_name="chat_history"),
        ("human", "{input}"),
    ]
)


def get_rag_chain(model: str | None = None, user_id: str | None = None):
    selected_model = model or DEFAULT_MODEL

    llm = ChatGoogleGenerativeAI(
        model=selected_model,
        google_api_key=GOOGLE_API_KEY,
        temperature=LLM_TEMPERATURE,
    )

    search_kwargs = {"k": RETRIEVER_K}
    if user_id:
        search_kwargs["filter"] = {"user_id": str(user_id)}

    retriever = vectorstore.as_retriever(search_kwargs=search_kwargs)

    history_aware_retriever = create_history_aware_retriever(
        llm,
        retriever,
        contextualize_q_prompt,
    )

    question_answer_chain = create_stuff_documents_chain(llm, qa_prompt)

    rag_chain = create_retrieval_chain(
        history_aware_retriever,
        question_answer_chain,
    )

    return rag_chain