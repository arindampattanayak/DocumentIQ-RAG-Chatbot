export default function HistoryPanel({ history }) {
  if (!history || history.length === 0) {
    return (
      <div className="panel">
        <h3>Your Chat History</h3>
        <p className="muted">No chat history yet.</p>
      </div>
    );
  }

  const grouped = history.reduce((acc, item) => {
    if (!acc[item.session_id]) acc[item.session_id] = [];
    acc[item.session_id].push(item);
    return acc;
  }, {});

  const sessionEntries = Object.entries(grouped);

  return (
    <div className="panel">
      <h3>Your Chat History</h3>

      <div className="history-list">
        {sessionEntries.map(([sessionId, items]) => (
          <div key={sessionId} className="history-session">
            <div className="history-session-title">
              Session: {sessionId}
            </div>

            {items
              .slice()
              .reverse()
              .map((item, idx) => (
                <div key={idx} className="history-item">
                  <div><strong>You:</strong> {item.user_query}</div>
                  <div><strong>AI:</strong> {item.gpt_response}</div>
                  <div className="muted">
                    {new Date(item.created_at).toLocaleString()}
                  </div>
                </div>
              ))}
          </div>
        ))}
      </div>
    </div>
  );
}