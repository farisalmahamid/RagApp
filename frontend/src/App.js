import React, { useState } from 'react';
import axios from 'axios';
import './App.css';

function App() {
  const [file, setFile] = useState(null);
  const [question, setQuestion] = useState("");
  const [chatHistory, setChatHistory] = useState([]);
  const [loading, setLoading] = useState(false);

  const handleFileChange = (e) => {
    setFile(e.target.files[0]);
  };

  const handleUpload = async () => {
    if (!file) return;
    const formData = new FormData();
    formData.append("file", file);

    try {
      await axios.post("http://localhost:8000/upload", formData);
      alert("File uploaded successfully!");
    } catch (error) {
      alert("Upload failed");
    }
  };

  const handleAsk = async () => {
    if (!question) return;

    const newHistory = [...chatHistory, { role: 'user', content: question }];
    setChatHistory(newHistory);
    setLoading(true);

    try {
      const res = await axios.post("http://localhost:8000/chat", {
        question: question
      });
      setChatHistory([...newHistory, { role: 'ai', content: res.data.answer }]);
    } catch (error) {
      setChatHistory([...newHistory, { role: 'ai', content: "Error getting answer." }]);
    }

    setQuestion("");
    setLoading(false);
  };

  return (
    <div className="page">
      <div className="container">
        <header className="header">
          <h1>RAG Assistant</h1>
          <p>Upload a document and chat with it</p>
        </header>

        <div className="card upload-card">
          <h3>Upload Document</h3>
          <input type="file" onChange={handleFileChange} />
          <button onClick={handleUpload}>Upload PDF / TXT</button>
        </div>

        <div className="card chat-card">
          <h3>Chat</h3>

          <div className="chat-history">
            {chatHistory.map((msg, index) => (
              <div key={index} className={`message ${msg.role}`}>
                {msg.content}
              </div>
            ))}
            {loading && <div className="message ai typing">Thinking…</div>}
          </div>

          <div className="input-area">
            <input
              value={question}
              onChange={(e) => setQuestion(e.target.value)}
              placeholder="Ask something about your document…"
              onKeyDown={(e) => e.key === 'Enter' && handleAsk()}
            />
            <button onClick={handleAsk}>Send</button>
          </div>
        </div>
      </div>
    </div>
  );
}

export default App;
