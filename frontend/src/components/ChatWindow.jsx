export default function ChatWindow({ messages, isSending }) {
  return (
    <div className="chat-window">
      {messages.length === 0 && (
        <div className="empty-state">
          Ask a question about your uploaded documents.
        </div>
      )}

      {messages.map((message, index) => (
        <div key={index} className={`message ${message.role}`}>
          <div className="bubble">{message.content}</div>
        </div>
      ))}

      {isSending && <div className="typing">Generating response...</div>}
    </div>
  );
}