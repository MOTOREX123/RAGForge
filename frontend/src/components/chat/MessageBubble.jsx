import { useState } from "react";
import { Check, Copy, RotateCcw, ThumbsUp, ThumbsDown, Flag, ExternalLink } from "lucide-react";
import { BotAvatar } from "./BotAvatar";
import { MarkdownContent } from "./MarkdownContent";
import { CitationRow } from "../citations/CitationRow";
import { RouteModelBadge } from "../indicators/RouteModelBadge";
import { useToast } from "../../context/ToastContext";
import { useConversation } from "../../context/ConversationContext";

const ROUTE_RULE_COLOR = {
  local: "border-purple",
  web: "border-green",
  general: "border-ink-dim",
};

export function MessageBubble({ message, onRegenerate, onRetry, isLastAssistant, retrievalConfidence, chunksRetrieved }) {
  const [copied, setCopied] = useState(false);
  const [feedback, setFeedback] = useState(null);
  const [showConfidence, setShowConfidence] = useState(false);
  const [hovered, setHovered] = useState(false);
  const { addToast } = useToast();
  const { selectCitation, speakingId } = useConversation();

  if (message.role === "user") {
    return (
      <div className="flex justify-end">
        <div className="max-w-[720px] rounded-xl bg-purple-bg px-4 py-3 text-[13px] leading-relaxed text-ink">
          {message.content}
        </div>
      </div>
    );
  }

  const ruleColor = ROUTE_RULE_COLOR[message.route] || "border-ink-dim";

  const handleCopy = async () => {
    try {
      await navigator.clipboard.writeText(message.content);
      setCopied(true);
      addToast("Message copied", "success");
      setTimeout(() => setCopied(false), 1500);
    } catch {
      // Clipboard access denied or unavailable
    }
  };

  const handleFeedback = (value) => {
    setFeedback(value);
    addToast(value === "up" ? "Thanks for the feedback!" : "We'll try to do better", "success");
    console.log("Feedback:", value, "for message:", message.id);
  };

  const formatTime = (timestamp) => {
    const date = new Date(timestamp);
    return date.toLocaleTimeString([], { hour: "2-digit", minute: "2-digit" });
  };

  if (message.isError) {
    return (
      <div className="flex gap-2.5" onMouseEnter={() => setHovered(true)} onMouseLeave={() => setHovered(false)}>
        <div className="flex h-7 w-7 shrink-0 items-center justify-center rounded-full bg-red-dim text-red">
          <Flag size={14} />
        </div>
        <div className="flex-1 rounded-xl border border-red/30 bg-red-dim/30 px-4 py-3">
          <p className="text-[13px] leading-relaxed text-red">{message.content}</p>
          <div className="mt-2 flex items-center gap-2">
            <button
              type="button"
              onClick={onRetry}
              className="inline-flex items-center gap-1.5 rounded px-2 py-1 text-[11px] text-red transition-colors hover:bg-red/10"
            >
              <RotateCcw size={12} />
              Retry
            </button>
          </div>
        </div>
      </div>
    );
  }

  return (
    <div 
      className="flex gap-2.5" 
      onMouseEnter={() => setHovered(true)} 
      onMouseLeave={() => setHovered(false)}
    >
      {/* Avatar indicator */}
      <BotAvatar state={message.id === speakingId ? "speaking" : "idle"} />

      <div className="flex-1 min-w-0">
        {/* Route badge */}
        <div className="mb-1.5">
          <RouteModelBadge
            route={message.route}
            provider={message.provider}
            model={message.model}
          />
        </div>

        {/* Content */}
        <div className={`rounded-xl border-l-3 ${ruleColor} bg-surface px-4 py-3`}>
          <div className="text-[13px] leading-relaxed text-ink">
            <MarkdownContent content={message.content} />
          </div>

          {/* Citations */}
          <CitationRow citations={message.citations} onCitationClick={selectCitation} />

          {/* No relevant documents warning */}
          {(!message.citations || message.citations.length === 0) && chunksRetrieved === 0 && message.route !== "general" && (
            <div className="mt-3 pt-3 border-t border-line flex items-center gap-2 text-yellow bg-yellow-dim/20 rounded px-3 py-2">
              <span className="text-[11px] font-medium">No relevant information found</span>
            </div>
          )}

          {/* Retrieval Confidence */}
          {(retrievalConfidence !== null && retrievalConfidence !== undefined || chunksRetrieved > 0) && (
            <div className="mt-3 pt-3 border-t border-line flex items-center gap-3" onClick={() => setShowConfidence(!showConfidence)}>
              <div className="flex items-center gap-2 cursor-pointer">
                <span className="text-[11px] font-medium text-ink-dim">Retrieval confidence</span>
                <span className="text-[11px] font-mono text-purple">
                  {retrievalConfidence !== null && retrievalConfidence !== undefined
                    ? (retrievalConfidence * 100).toFixed(0) + "%"
                    : "—"}
                </span>
                <div className="w-24 h-1.5 bg-raised rounded-full overflow-hidden">
                  <div
                    className="h-full bg-purple transition-all duration-300"
                    style={{ width: retrievalConfidence !== null && retrievalConfidence !== undefined ? `${retrievalConfidence * 100}%` : "0%" }}
                  />
                </div>
              </div>
              <span className="text-[10px] text-ink-muted font-mono">
                {chunksRetrieved} chunks retrieved
              </span>
            </div>
          )}

          {/* Actions - show on hover or for last assistant */}
          <div className={`mt-3 flex items-center gap-1.5 transition-opacity duration-200 ${hovered || isLastAssistant ? "opacity-100" : "opacity-0"}`}>
            <button
              type="button"
              onClick={handleCopy}
              className="inline-flex items-center gap-1.5 rounded px-2 py-1 text-[10px] text-ink-dim transition-colors hover:bg-raised hover:text-ink"
              aria-label={copied ? "Copied" : "Copy message"}
            >
              {copied ? <Check size={12} /> : <Copy size={12} />}
              {copied ? "Copied" : "Copy"}
            </button>

            {isLastAssistant && (
              <button
                type="button"
                onClick={onRegenerate}
                className="inline-flex items-center gap-1.5 rounded px-2 py-1 text-[10px] text-ink-dim transition-colors hover:bg-raised hover:text-ink"
                aria-label="Regenerate response"
              >
                <RotateCcw size={12} />
                Regenerate
              </button>
            )}

            <div className="flex-1" />

            {/* Feedback */}
            <div className="flex items-center gap-0.5">
              <button
                type="button"
                onClick={() => handleFeedback("up")}
                className={`inline-flex items-center gap-1 rounded px-2 py-1 text-[10px] transition-colors ${
                  feedback === "up"
                    ? "text-green bg-green-dim/30"
                    : "text-ink-dim hover:bg-raised hover:text-ink"
                }`}
                aria-label={feedback === "up" ? "Marked helpful" : "Mark as helpful"}
              >
                <ThumbsUp size={12} />
              </button>
              <button
                type="button"
                onClick={() => handleFeedback("down")}
                className={`inline-flex items-center gap-1 rounded px-2 py-1 text-[10px] transition-colors ${
                  feedback === "down"
                    ? "text-red bg-red-dim/30"
                    : "text-ink-dim hover:bg-raised hover:text-ink"
                }`}
                aria-label={feedback === "down" ? "Marked not helpful" : "Mark as not helpful"}
              >
                <ThumbsDown size={12} />
              </button>
            </div>

            <span className="text-[10px] text-ink-muted shrink-0 ml-2">
              {formatTime(message.timestamp)}
            </span>
          </div>
        </div>
      </div>
    </div>
  );
}