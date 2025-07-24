import React, { useState } from 'react';
import './Aiagent.css';
import { getAICompletion } from './openrouterService';

const Aiagent = () => {
  const [input, setInput] = useState('');
  const [chat, setChat] = useState([]);
  const [loading, setLoading] = useState(false);

  const handleSend = async () => {
    if (input.trim() === '') return;

    // Add user message first
    setChat([...chat, { type: 'user', message: input }]);
    setLoading(true);

    try {
      const aiReply = await getAICompletion(input);
      setChat(prevChat => [
        ...prevChat,
        { type: 'bot', message: aiReply }
      ]);
    } catch (e) {
      setChat(prevChat => [
        ...prevChat,
        { type: 'bot', message: "Sorry, server couldn't reacb to api" }
      ]);
    } finally {
      setInput('');
      setLoading(false);
    }
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
        {loading && <div>AI is typing...</div>}
      </div>
      <div className="input-area">
        <input
          type="text"
          placeholder="Ask me anything..."
          value={input}
          onChange={(e) => setInput(e.target.value)}
          disabled={loading}
        />
        <button onClick={handleSend} disabled={loading}>Send</button>
      </div>
    </div>
  );
};

export default Aiagent;
