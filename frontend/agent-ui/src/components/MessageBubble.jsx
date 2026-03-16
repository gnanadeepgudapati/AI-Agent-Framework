// components/MessageBubble.jsx
// Renders a single message in the chat window.
// Human messages appear on the right, AI messages on the left.

export default function MessageBubble({ message }) {
  const isHuman = message.role === "human";

  return (
    <div className={`flex w-full mb-4 ${isHuman ? "justify-end" : "justify-start"}`}>
      
      {/* AI Avatar */}
      {!isHuman && (
        <div className="w-8 h-8 rounded-full bg-blue-600 flex items-center justify-center text-white text-xs font-bold mr-2 mt-1 shrink-0">
          AI
        </div>
      )}

      {/* Message bubble */}
      <div
        className={`max-w-[70%] rounded-2xl px-4 py-3 text-sm leading-relaxed ${
          isHuman
            ? "bg-blue-600 text-white rounded-tr-sm"
            : "bg-gray-800 text-gray-100 rounded-tl-sm"
        }`}
      >
        {/* Service tag for AI messages */}
        {!isHuman && message.service && (
          <div className="text-xs text-blue-400 font-semibold mb-1 uppercase tracking-wide">
            {message.service}
          </div>
        )}

        {/* Message text */}
        <p className="whitespace-pre-wrap">{message.content}</p>

        {/* Timestamp */}
        <div className={`text-xs mt-1 ${isHuman ? "text-blue-200" : "text-gray-500"}`}>
          {message.timestamp}
        </div>
      </div>

      {/* Human Avatar */}
      {isHuman && (
        <div className="w-8 h-8 rounded-full bg-gray-600 flex items-center justify-center text-white text-xs font-bold ml-2 mt-1 shrink-0">
          You
        </div>
      )}

    </div>
  );
}