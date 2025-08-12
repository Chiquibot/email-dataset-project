import React, { useState, useEffect } from "react";

function App() {
  const [emails, setEmails] = useState([]);
  const [loading, setLoading] = useState(false);

  const fetchProcessedEmails = async () => {
    setLoading(true);
    try {
      const response = await fetch("http://127.0.0.1:8000/processed-emails");
      const data = await response.json();
      setEmails(data.emails || []);
    } catch (error) {
      console.error(error);
      setEmails([]);
    }
    setLoading(false);
  };

  const processEmails = async () => {
    setLoading(true);
    try {
      const response = await fetch("http://127.0.0.1:8000/process-emails", { method: "POST" });
      const data = await response.json();
      console.log("Process emails response:", data);
      await fetchProcessedEmails();
    } catch (error) {
      console.error(error);
    }
    setLoading(false);
  };

  useEffect(() => {
    fetchProcessedEmails();
  }, []);

  return (
    <div style={{ padding: 20 }}>
      <h1>Processed Emails</h1>
      <button onClick={processEmails} disabled={loading} style={{ marginRight: 10 }}>
        {loading ? "Processing..." : "Process Emails"}
      </button>
      <button onClick={fetchProcessedEmails} disabled={loading}>
        {loading ? "Loading..." : "Fetch Processed Emails"}
      </button>

      {!loading && emails.length === 0 && <p>No processed emails found.</p>}

      {!loading && emails.map(email => (
        <div key={email.id} style={{ borderBottom: "1px solid #ccc", marginBottom: 10 }}>
          <p><b>Subject:</b> {email.subject}</p>
          <p><b>Body:</b> {email.body}</p>
          <p><b>BERT Message:</b> {email.bert_message}</p>
          <p><b>LLaMA Response:</b> {email.llama_response}</p>
        </div>
      ))}
    </div>
  );
}

export default App;
