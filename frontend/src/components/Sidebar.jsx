import { useState } from "react";
import { deleteDocument, uploadDocument } from "../api";

export default function Sidebar({
  user,
  model,
  setModel,
  documents,
  onRefreshDocuments,
  onRefreshHistory,
  onNewChat,
  onLogout,
  onDocumentsChanged,
}) {
  const [selectedFile, setSelectedFile] = useState(null);
  const [selectedDeleteId, setSelectedDeleteId] = useState("");
  const [loading, setLoading] = useState(false);

  const handleUpload = async () => {
    if (!selectedFile) return;
    setLoading(true);
    try {
      await uploadDocument(selectedFile);
      setSelectedFile(null);
      await onRefreshDocuments();
      await onRefreshHistory();
    } catch (error) {
      alert(error.message);
    } finally {
      setLoading(false);
    }
  };

  const handleDelete = async () => {
    if (!selectedDeleteId) return;
    setLoading(true);
    try {
      await deleteDocument(selectedDeleteId);
      setSelectedDeleteId("");
      await onRefreshDocuments();
      await onRefreshHistory();
      if (onDocumentsChanged) onDocumentsChanged();
    } catch (error) {
      alert(error.message);
    } finally {
      setLoading(false);
    }
  };

  return (
    <aside className="sidebar">
      <div className="panel">
        <h2>RAG Voice</h2>
        <p className="muted">
          {user?.name} · {user?.email}
        </p>
        <button className="secondary-btn" onClick={onLogout}>
          Logout
        </button>
      </div>

      <div className="panel">
        <label className="label">Model</label>
        <select value={model} onChange={(e) => setModel(e.target.value)}>
          <option value="gemini-2.5-flash">gemini-2.5-flash</option>
        </select>
      </div>

      <div className="panel">
        <label className="label">Upload Document</label>
        <input
          type="file"
          accept=".pdf,.docx,.html"
          onChange={(e) => setSelectedFile(e.target.files?.[0] || null)}
        />
        <button className="primary-btn" onClick={handleUpload} disabled={!selectedFile || loading}>
          Upload
        </button>
      </div>

      <div className="panel">
        <h3>Documents</h3>
        <button className="secondary-btn" onClick={onRefreshDocuments}>
          Refresh
        </button>

        <div className="doc-list">
          {documents.length === 0 && <p className="muted">No documents yet.</p>}
          {documents.map((doc) => (
            <div key={doc.id} className="doc-item">
              <div className="doc-name">{doc.filename}</div>
              <div className="doc-id">ID: {doc.id}</div>
            </div>
          ))}
        </div>

        {documents.length > 0 && (
          <>
            <label className="label">Delete document</label>
            <select
              value={selectedDeleteId}
              onChange={(e) => setSelectedDeleteId(e.target.value)}
            >
              <option value="">Select document</option>
              {documents.map((doc) => (
                <option key={doc.id} value={doc.id}>
                  {doc.filename}
                </option>
              ))}
            </select>
            <button className="danger-btn" onClick={handleDelete} disabled={!selectedDeleteId || loading}>
              Delete
            </button>
          </>
        )}
      </div>

      <div className="panel">
        <button className="secondary-btn" onClick={onNewChat}>
          Start New Chat
        </button>
      </div>
    </aside>
  );
}