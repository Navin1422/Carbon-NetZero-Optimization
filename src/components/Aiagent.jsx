import React, { useState } from 'react';
import './Aiagent.css';

const Aiagent = () => {
  const [input, setInput] = useState('');
  const [chat, setChat] = useState([]);

  const handleSend = async () => {
    if (input.trim() === '') return;

    const dummyReply = "I'm here to help!";

    setChat([
      ...chat,
      { type: 'user', message: input },
      { type: 'bot', message: dummyReply }
    ]);
    setInput('');
  };

  return (
    <div className="ai-agent-container">
      <h2>🤖 AI Assistant</h2>

      <div className="chat-box">
        {chat.map((msg, idx) => (
          <div key={idx} className={`chat-msg ${msg.type}`}>
            <div className="bubble">
              <strong>{msg.type === 'user' ? 'You' : 'AI'}:</strong> {msg.message}
            </div>
            <div className="plant-below">
              {msg.type === 'user' ? '🪴' : '🌿'}
            </div>
          </div>
        ))}
      </div>

      <div className="input-area">
        <input
          type="text"
          placeholder="Ask me anything..."
          value={input}
          onChange={(e) => setInput(e.target.value)}
        />
        <button onClick={handleSend}>Send</button>
      </div>
    </div>
  );
};

export default Aiagent;
