import React, { useState } from "react";
import "./App.css";

const App = () => {
  const [messages, setMessages] = useState([]);
  const [isSending, setIsSending] = useState(false);
  const [users, setUsers] = useState([]);
  const [selectedUserId, setSelectedUserId] = useState(null);

  // Fetch users when component mounts
  React.useEffect(() => {
    const fetchUsers = async () => {
      try {
        const response = await fetch("http://localhost:8000/users/");
        const data = await response.json();
        setUsers(data);
        // Set first user as default if available
        if (data.length > 0) {
          setSelectedUserId(data[0].id);
        }
      } catch (error) {
        console.error("Error fetching users:", error);
      }
    };
    fetchUsers();
  }, []);

  const addMessage = (message) => {
    setMessages((prevMessages) => [...prevMessages, message]);
  };

  const sendMessage = async (question) => {
    setIsSending(true); // Start sending and show loader
    addMessage({ author: "user", content: question });

    // Convert messages to chat history format (last 10 messages for context)
    const chatHistory = messages.slice(-10).map((msg) => ({
      role: msg.author === "user" ? "user" : "assistant",
      content: msg.content,
    }));

    try {
      const response = await fetch("http://localhost:8000/chat-bot/ask", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          question,
          user_id: selectedUserId,
          include_images: true, // Request image metadata
          chat_history: chatHistory, // Send conversation history
        }),
      });

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      const data = await response.json();

      // Handle new response format with images
      addMessage({
        author: "bot",
        content: data.text || data.response, // Support both old and new format
        images: data.images || [],
        hasImages: data.has_images || false,
        responseTime: data.response_time_ms || null,
      });
    } catch (error) {
      console.error("There was an error!", error);

      let errorMessage = "Sorry, there was an issue getting a response.";
      if (error.message.includes("Failed to fetch")) {
        errorMessage =
          "Cannot connect to server. Please check if the backend is running.";
      }

      addMessage({
        author: "bot",
        content: errorMessage,
        images: [],
        hasImages: false,
      });
    }

    setIsSending(false); // Done sending, remove loader
  };

  return (
    <div className="app-container">
      <div className="app-wrapper">
        <Header />
        <ChatArea messages={messages} isSending={isSending} />
        <InputArea
          onSendMessage={sendMessage}
          isSending={isSending}
          users={users}
          selectedUserId={selectedUserId}
          onUserSelect={setSelectedUserId}
        />
      </div>
    </div>
  );
};

const Header = () => {
  const [showExamples, setShowExamples] = React.useState(false);

  const exampleQueries = [
    "Show me all posts with images",
    "Get posts from user 1",
    "Show me user profiles",
    "Find recent posts",
    "List all places",
    "Who follows me?",
  ];

  return (
    <div className="header">
      <h1>POC MultiAgent</h1>
      <p>Your personal assistant with image support 📸</p>

      <button
        className="examples-toggle"
        onClick={() => setShowExamples(!showExamples)}
      >
        {showExamples ? "Hide" : "Show"} Example Queries
      </button>
      {showExamples && (
        <div className="example-queries">
          {exampleQueries.map((query, index) => (
            <div key={index} className="example-query">
              💬 {query}
            </div>
          ))}
        </div>
      )}
    </div>
  );
};

const ChatArea = ({ messages, isSending }) => {
  // Helper function to render markdown-style text
  const renderContent = (content) => {
    if (!content) return "";

    // Simple markdown image rendering: ![alt](url)
    const imageRegex = /!\[([^\]]*)\]\(([^)]+)\)/g;
    const parts = [];
    let lastIndex = 0;
    let match;

    try {
      while ((match = imageRegex.exec(content)) !== null) {
        // Add text before the image
        if (match.index > lastIndex) {
          parts.push(
            <span key={`text-${lastIndex}`}>
              {content.substring(lastIndex, match.index)}
            </span>
          );
        }

        // Add the image - match[1] is alt text, match[2] is URL
        const altText = match[1] || "Image";
        const imageUrl = match[2];

        if (imageUrl) {
          parts.push(
            <img
              key={`img-${match.index}`}
              src={imageUrl}
              alt={altText}
              className="message-inline-image"
              onError={(e) => {
                e.target.style.display = "none";
                console.error("Failed to load image:", imageUrl);
              }}
            />
          );
        }

        lastIndex = match.index + match[0].length;
      }

      // Add remaining text
      if (lastIndex < content.length) {
        parts.push(
          <span key={`text-${lastIndex}`}>{content.substring(lastIndex)}</span>
        );
      }

      return parts.length > 0 ? parts : content;
    } catch (error) {
      console.error("Error rendering content:", error);
      return content;
    }
  };

  return (
    <div className="chat-area">
      {messages.map((message, index) => (
        <div key={index} className={`message ${message.author}`}>
          <div className="message-header">
            {message.author === "user" ? "QN:" : "Assistant:"}
          </div>
          <div className="message-content">
            {message.author === "user" ? (
              message.content
            ) : (
              <>
                {renderContent(message.content)}
                {message.responseTime && (
                  <div className="response-time">
                    ⏱️ {message.responseTime}ms
                  </div>
                )}
                {message.hasImages &&
                  message.images &&
                  message.images.length > 0 && (
                    <div className="image-gallery">
                      {message.images.map((img, imgIndex) => (
                        <div key={imgIndex} className="image-container">
                          <img
                            src={img.url}
                            alt={img.alt || `Image ${imgIndex + 1}`}
                            className="gallery-image"
                            onError={(e) => {
                              e.target.style.display = "none";
                              console.error("Failed to load image:", img.url);
                            }}
                            onClick={() => window.open(img.url, "_blank")}
                          />
                        </div>
                      ))}
                    </div>
                  )}
              </>
            )}
          </div>
        </div>
      ))}
      {isSending &&
        messages.length > 0 &&
        messages[messages.length - 1].author === "user" && (
          <div className="message bot">
            <div className="message-header">Assistant:</div>
            <div className="message-content">
              <div className="loader">
                <div className="dot"></div>
                <div className="dot"></div>
                <div className="dot"></div>
              </div>
            </div>
          </div>
        )}
    </div>
  );
};

const InputArea = ({
  onSendMessage,
  isSending,
  users,
  selectedUserId,
  onUserSelect,
}) => {
  const [question, setQuestion] = useState("");

  const handleSendMessage = () => {
    if (question.trim()) {
      onSendMessage(question);
      setQuestion(""); // Clear the input after sending
    }
  };

  return (
    <div className="input-area">
      {users.length > 0 && (
        <select
          className="user-dropdown"
          value={selectedUserId || ""}
          onChange={(e) => onUserSelect(Number(e.target.value))}
          disabled={isSending}
        >
          {users.map((user) => (
            <option key={user.id} value={user.id}>
              {user.name}
            </option>
          ))}
        </select>
      )}
      <input
        type="text"
        placeholder="Message Assistant..."
        value={question}
        onChange={(e) => setQuestion(e.target.value)}
        onKeyPress={(e) => {
          if (e.key === "Enter") {
            handleSendMessage();
          }
        }}
        disabled={isSending} // Disable input when sending
      />
      <button onClick={handleSendMessage} disabled={isSending}>
        Send
      </button>
    </div>
  );
};

export default App;
