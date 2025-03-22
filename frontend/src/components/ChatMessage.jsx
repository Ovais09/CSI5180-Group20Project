import React from "react";
import ChatBoxIcon from "./ChatBoxIcon";

const ChatMessage = ({ chat }) => {
  return (
    <div
      className={`message ${chat.type === "model" ? "bot" : "user"}-message`}
    >
      {chat.type === "model" && <ChatBoxIcon />}
      <p className="message-text">{chat.text}</p>
    </div>
  );
};

export default ChatMessage;
