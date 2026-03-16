// components/ChatWindow.jsx
// The main chat interface — message list + input box.
// Manages all state: messages, loading, session ID.

import { useState, useEffect, useRef } from "react";
import MessageBubble from "./MessageBubble";
import ToolCallIndicator from "./ToolCallIndicator";
import { sendMessage, clearSession } from "../services/api_client";

export default function ChatWindow() {
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState("");
  const [isLoading, setIsLoading] = useState(false);
  const [sessionId] = useState(() => `session-${Date.now()}`);
  const bottomRef = useRef(null);

  // Auto scroll to bottom when new messages arrive
  useEffect(() => {
    bottomRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages, isLoading]);

  function getTimestamp() {
    return new Date().toLocaleTimeString([], { hour: "2-digit", minute: "2-digit" });
  }

  async function handleSend() {
    if (!input.trim() || isLoading) return;

    const userMessage = {
      role: "human",
      content: input.trim(),
      timestamp: getTimestamp(),
    };

    setMessages((prev) => [...prev, userMessage]);
    setInput("");
    setIsLoading(true);

    try {
      const reply = await sendMessage(sessionId, userMessage.content);

      const aiMessage = {
        role: "ai",
        content: reply,
        timestamp: getTimestamp(),
      };

      setMessages((prev) => [...prev, aiMessage]);
    } catch (error) {
      const errorMessage = {
        role: "ai",
        content: "Sorry, something went wrong. Please check the server is running and try again.",
        timestamp: getTimestamp(),
      };
      setMessages((prev) => [...prev, errorMessage]);
    } finally {
      setIsLoading(false);
    }
  }

  async function handleClear() {
    await clearSession(sessionId);
    setMessages([]);
  }

  function handleKeyDown(e) {
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault();
      handleSend();
    }
  }

  return (
    <div className="flex flex-col h-screen bg-gray-900 text-white">

      {/* Header */}
      <div className="flex items-center justify-between px-6 py-4 border-b border-gray-700 bg-gray-900">
        <div>
          <h1 className="text-lg font-semibold">Enterprise Assistant</h1>
          <p className="text-xs text-gray-400">HR · IT · Facilities</p>
        </div>
        <button
          onClick={handleClear}
          className="text-xs text-gray-400 hover:text-white border border-gray-600 hover:border-gray-400 px-3 py-1.5 rounded-lg transition-colors"
        >
          New Chat
        </button>
      </div>

      {/* Message list */}
      <div className="flex-1 overflow-y-auto px-4 py-6">
        {messages.length === 0 && (
          <div className="flex flex-col items-center justify-center h-full text-center">
            <div className="text-4xl mb-4">💼</div>
            <h2 className="text-xl font-semibold text-gray-200 mb-2">Enterprise Assistant</h2>
            <p className="text-gray-400 text-sm max-w-md">
              Ask me anything about HR, IT, or Facilities. I'll route your request to the right system automatically.
            </p>
            <div className="mt-6 grid grid-cols-1 gap-2 w-full max-w-md">
              {[
                "How many vacation days does EMP001 have?",
                "Raise a high priority IT ticket for VPN issues",
                "Book a meeting room for 8 people tomorrow at 2pm",
              ].map((suggestion) => (
                <button
                  key={suggestion}
                  onClick={() => setInput(suggestion)}
                  className="text-left text-sm text-gray-300 bg-gray-800 hover:bg-gray-700 px-4 py-3 rounded-xl transition-colors border border-gray-700"
                >
                  {suggestion}
                </button>
              ))}
            </div>
          </div>
        )}

        {messages.map((msg, index) => (
          <MessageBubble key={index} message={msg} />
        ))}

        {isLoading && <ToolCallIndicator />}

        <div ref={bottomRef} />
      </div>

      {/* Input area */}
      <div className="px-4 py-4 border-t border-gray-700 bg-gray-900">
        <div className="flex gap-3 items-end max-w-4xl mx-auto">
          <textarea
            value={input}
            onChange={(e) => setInput(e.target.value)}
            onKeyDown={handleKeyDown}
            placeholder="Ask about HR, IT, or Facilities..."
            rows={1}
            className="flex-1 bg-gray-800 text-white placeholder-gray-500 rounded-xl px-4 py-3 text-sm resize-none focus:outline-none focus:ring-2 focus:ring-blue-500 border border-gray-700"
          />
          <button
            onClick={handleSend}
            disabled={!input.trim() || isLoading}
            className="bg-blue-600 hover:bg-blue-500 disabled:bg-gray-700 disabled:text-gray-500 text-white px-4 py-3 rounded-xl text-sm font-medium transition-colors shrink-0"
          >
            Send
          </button>
        </div>
        <p className="text-xs text-gray-600 text-center mt-2">Press Enter to send · Shift+Enter for new line</p>
      </div>

    </div>
  );
}