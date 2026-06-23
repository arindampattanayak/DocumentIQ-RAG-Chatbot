import { useEffect, useState } from "react";
import AuthPanel from "./components/AuthPanel";
import Sidebar from "./components/Sidebar";
import ChatWindow from "./components/ChatWindow";
import ChatInput from "./components/ChatInput";
import HistoryPanel from "./components/HistoryPanel";
import {
  me,
  logout,
  listDocuments,
  sendChat,
  getHistory,
} from "./api";
import "./index.css";

function App() {
  const [user, setUser] = useState(null);
  const [authLoading, setAuthLoading] = useState(true);
  const [documents, setDocuments] = useState([]);
  const [messages, setMessages] = useState([]);
  const [history, setHistory] = useState([]);
  const [sessionId, setSessionId] = useState(null);
  const [model, setModel] = useState("gemini-2.5-flash");
  const [loading, setLoading] = useState(false);

  const loadDocuments = async () => {
    const docs = await listDocuments();
    setDocuments(Array.isArray(docs) ? docs : []);
  };

  const loadHistory = async () => {
    const logs = await getHistory();
    setHistory(Array.isArray(logs) ? logs : []);
  };

  const loadMe = async () => {
    try {
      const currentUser = await me();
      setUser(currentUser);
      await loadDocuments();
      await loadHistory();
    } catch {
      localStorage.removeItem("token");
      setUser(null);
    } finally {
      setAuthLoading(false);
    }
  };

  useEffect(() => {
    const token = localStorage.getItem("token");
    if (token) {
      loadMe();
    } else {
      setAuthLoading(false);
    }
  }, []);

  const handleAuthSuccess = async (userData) => {
    setUser(userData);
    await loadDocuments();
    await loadHistory();
  };

  const handleLogout = async () => {
    try {
      await logout();
    } catch {
      // ignore logout API errors
    } finally {
      localStorage.removeItem("token");
      setUser(null);
      setDocuments([]);
      setMessages([]);
      setHistory([]);
      setSessionId(null);
    }
  };

  const handleNewChat = () => {
    setMessages([]);
    setSessionId(null);
  };

  const handleSendMessage = async (text) => {
    const userMessage = { role: "user", content: text };
    setMessages((prev) => [...prev, userMessage]);

    try {
      setLoading(true);

      const response = await sendChat({
        question: text,
        session_id: sessionId,
        model,
      });

      const answer = response?.answer || "No answer returned.";
      const nextSessionId = response?.session_id || sessionId;

      setSessionId(nextSessionId);
      setMessages((prev) => [
        ...prev,
        { role: "assistant", content: answer },
      ]);

      await loadHistory();
    } catch (error) {
      setMessages((prev) => [
        ...prev,
        { role: "assistant", content: `Error: ${error.message}` },
      ]);
    } finally {
      setLoading(false);
    }
  };

  const refreshDocuments = async () => {
    await loadDocuments();
  };

  const refreshHistory = async () => {
    await loadHistory();
  };

  if (authLoading) {
    return <div className="loading-screen">Loading...</div>;
  }

  if (!user) {
    return <AuthPanel onAuthSuccess={handleAuthSuccess} />;
  }

  return (
    <div className="app-shell">
      <Sidebar
        user={user}
        model={model}
        setModel={setModel}
        documents={documents}
        onRefreshDocuments={refreshDocuments}
        onRefreshHistory={refreshHistory}
        onNewChat={handleNewChat}
        onLogout={handleLogout}
      />

      <main className="main-area">
        <div className="hero">
          <h1>LangChain RAG Chatbot</h1>
          <p>
            Upload documents, ask questions, and see your full lifetime history after login.
          </p>
        </div>

        <ChatWindow messages={messages} isSending={loading} />
        <ChatInput onSend={handleSendMessage} disabled={loading} />

        <HistoryPanel history={history} />
      </main>
    </div>
  );
}

export default App;