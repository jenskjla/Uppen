// src/components/Chatbot.js
import React from "react";
import './Chatbot.css';

const Chatbot = () => {
    return (
      <div className="chatbot">
        <div className="chatbot-header">
          <h3>AI Helper</h3>
        </div>
        <div className="chatbot-body">
          {/* Implement chatbot functionality here */}
        </div>
        <div className="chatbot-footer">
          <input type="text" placeholder="Send your question..." />
          <button>&#8657;</button>
        </div>
      </div>
    );
  };

export default Chatbot;