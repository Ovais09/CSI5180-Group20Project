import React from "react";
import ChatBoxIcon from "./ChatBoxIcon";

const ChatMessage = ({ chat }) => {
  // if (chat.type === "eventList") {
  //   return (
  //     <div className="message bot-message">
  //       <ChatBoxIcon />
  //       <div className="event-cards">
  //         {Array.isArray(chat.data) &&
  //           chat.data.map((event, index) => (
  //             <div key={index} className="event-card">
  //               <h3>{event.name}</h3>
  //               <p>
  //                 {event.date} | {event.location}
  //               </p>
  //               <a
  //                 href={event.url}
  //                 className="ticket-button"
  //                 target="_blank"
  //                 rel="noopener noreferrer"
  //               >
  //                 Get Tickets
  //               </a>
  //             </div>
  //           ))}
  //       </div>
  //     </div>
  //   );
  // }
  return (
    <div
      className={`message ${chat.type === "model" ? "bot" : "user"}-message`}
    >
      {chat.type === "model" && <ChatBoxIcon />}
      <p
        className="message-text"
        dangerouslySetInnerHTML={{ __html: chat.text }}
      >
        {/* {chat.text} */}
      </p>
    </div>
  );
};

export default ChatMessage;
