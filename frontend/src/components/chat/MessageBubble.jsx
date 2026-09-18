import { useState } from "react";
import { Check, Copy, RotateCcw } from "lucide-react";
import { MarkdownContent } from "./MarkdownContent";
import { CitationRow } from "../citations/CitationRow";
import { RouteModelBadge } from "../indicators/RouteModelBadge";

const ROUTE_RULE_COLOR = {
  local: "border-brass",
  web: "border-teal",
  general: "border-ink-dim",
};

export function MessageBubble({ message, onRegenerate, isLastAssistant }) {
  const [copied, setCopied] = useState(false);

  if (message.role === "user") {
    return (
      <div className="flex justify-end">
        <div className="max-w-prose whitespace-pre-wrap text-[15px] leading-relaxed text-ink">
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
      setTimeout(() => setCopied(false), 1500);
    } catch {
      // Clipboard access denied or unavailable — fail quietly, the
      // button simply won't show the "copied" confirmation.
    }
  };

  if (message.isError) {
    return (
      <div className="border-l-2 border-danger py-1 pl-4">
        <p className="text-[15px] leading-relaxed text-danger">
          {message.content}
        </p>
      </div>
    );
  }

  return (
    <div className={`border-l-2 ${ruleColor} py-1 pl-4`}>
      <div className="mb-2">
        <RouteModelBadge
          route={message.route}
          provider={message.provider}
          model={message.model}
        />
      </div>

      <div className="text-[15px] leading-relaxed text-ink">
        <MarkdownContent content={message.content} />
      </div>

      <CitationRow citations={message.citations} />

      <div className="mt-2 flex items-center gap-1">
        <button
          type="button"
          onClick={handleCopy}
          className="inline-flex items-center gap-1.5 rounded px-2 py-1 text-xs text-ink-dim transition-colors hover:bg-raised hover:text-ink"
        >
          {copied ? <Check size={13} /> : <Copy size={13} />}
          {copied ? "Copied" : "Copy"}
        </button>
        {isLastAssistant && (
          <button
            type="button"
            onClick={onRegenerate}
            className="inline-flex items-center gap-1.5 rounded px-2 py-1 text-xs text-ink-dim transition-colors hover:bg-raised hover:text-ink"
          >
            <RotateCcw size={13} />
            Regenerate
          </button>
        )}
      </div>
    </div>
  );
}
