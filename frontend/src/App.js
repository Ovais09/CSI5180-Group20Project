import logo from "./logo.svg";
import "./App.css";
import { useState } from "react";

import ChatBoxIcon from "./components/ChatBoxIcon";
import ChatForm from "./components/ChatForm";
import ChatMessage from "./components/ChatMessage";
function App() {
  const [chatHistory, setChatHistory] = useState([]);

  const generateEventSphereResponse = async (history) => {
    console.log(history);
    const response = await fetch("http://127.0.0.1:5000/process", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ input: history }),
    });

    const data = await response.json();
    console.log("Response from backend:", data);
    // setResult(data.result);
  };

  return (
    <div className="container">
      <div className="chatbot-popup">
        {/* Chat Header */}
        <div className="chat-header">
          <div className="header-info">
            <ChatBoxIcon />
            <h2 className="logo-text">EventSphereAI</h2>
          </div>
        </div>

        {/* Chat Body */}
        <div className="chat-body">
          <div className="message bot-message">
            <ChatBoxIcon />
            <p className="message-text">
              No plans? No problem! I can find you something cool happening near
              you right now!
            </p>
          </div>
          {/* Render the chat history via the ChatMessage component */}
          {chatHistory.map((chat, index) => (
            <ChatMessage key={index} chat={chat} />
          ))}
        </div>

        {/* Chat Footer */}
        <div className="chat-footer">
          <ChatForm
            chatHistory={chatHistory}
            setChatHistory={setChatHistory}
            generateEventSphereResponse={generateEventSphereResponse}
          />
        </div>
      </div>
    </div>
  );
}

export default App;
