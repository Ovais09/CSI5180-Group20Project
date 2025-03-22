import React, { use, useState } from "react";
import { useRef } from "react";

const ChatForm = ({
  chatHistory,
  setChatHistory,
  generateEventSphereResponse,
}) => {
  const [userInput, setUserInput] = useState("");
  const [result, setResult] = useState("");
  const inputRef = useRef();

  const handleSubmit = async (e) => {
    e.preventDefault();
    setUserInput(inputRef.current.value.trim());
    inputRef.current.value = "";
    // Update user-side chat history
    setChatHistory((history) => [
      ...history,
      { type: "user", text: userInput },
    ]);
    //console.log(userInput);

    //update chat history with bot response
    setTimeout(
      () =>
        setChatHistory((history) => [
          ...history,
          { type: "model", text: "Thinking..." },
        ]),
      generateEventSphereResponse([
        ...chatHistory,
        { type: "user", text: userInput },
      ]),
      600
    );
  };
  return (
    <form className="chat-form" onSubmit={handleSubmit}>
      <input
        type="text"
        ref={inputRef}
        //value={userInput}
        className="message-input"
        onChange={(e) => setUserInput(e.target.value)}
        placeholder="Message..."
      />
      <button class="material-symbols-rounded" type="submit">
        send
      </button>
      {/* <p>Result: {result}</p> */}
    </form>
  );
};

export default ChatForm;
