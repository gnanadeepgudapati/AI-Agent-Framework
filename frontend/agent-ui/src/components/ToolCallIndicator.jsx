// components/ToolCallIndicator.jsx
// Shows a subtle animation while the agent is calling a tool.
// Appears between the user message and the AI response.

export default function ToolCallIndicator({ service }) {
  const serviceConfig = {
    hr: { label: "HR System", color: "text-green-400", bg: "bg-green-400" },
    it: { label: "IT System", color: "text-yellow-400", bg: "bg-yellow-400" },
    facilities: { label: "Facilities System", color: "text-purple-400", bg: "bg-purple-400" },
    default: { label: "Processing", color: "text-blue-400", bg: "bg-blue-400" },
  };

  const config = serviceConfig[service?.toLowerCase()] || serviceConfig.default;

  return (
    <div className="flex justify-start mb-4">
      <div className="w-8 h-8 rounded-full bg-blue-600 flex items-center justify-center text-white text-xs font-bold mr-2 mt-1 shrink-0">
        AI
      </div>

      <div className="bg-gray-800 rounded-2xl rounded-tl-sm px-4 py-3 flex items-center gap-3">
        {/* Pulsing dots animation */}
        <div className="flex gap-1">
          <div className={`w-2 h-2 rounded-full ${config.bg} animate-bounce`} style={{ animationDelay: "0ms" }} />
          <div className={`w-2 h-2 rounded-full ${config.bg} animate-bounce`} style={{ animationDelay: "150ms" }} />
          <div className={`w-2 h-2 rounded-full ${config.bg} animate-bounce`} style={{ animationDelay: "300ms" }} />
        </div>

        {/* Service label */}
        <span className={`text-xs font-semibold ${config.color} uppercase tracking-wide`}>
          Querying {config.label}...
        </span>
      </div>
    </div>
  );
}
