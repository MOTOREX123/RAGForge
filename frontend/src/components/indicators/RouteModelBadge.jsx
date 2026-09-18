import { FileText, Globe, MessageCircle } from "lucide-react";

/**
 * Renders based entirely on the `route`/`provider`/`model` fields the
 * backend returned for this message — nothing here is hard-coded per
 * message. Unknown routes (e.g. a future "general") fall back to a
 * neutral style instead of breaking.
 */
const ROUTE_CONFIG = {
  local: {
    label: "Local documents",
    icon: FileText,
    dot: "bg-brass",
    text: "text-brass",
  },
  web: {
    label: "Web search",
    icon: Globe,
    dot: "bg-teal",
    text: "text-teal",
  },
  general: {
    label: "General chat",
    icon: MessageCircle,
    dot: "bg-ink-dim",
    text: "text-ink-dim",
  },
};

const PROVIDER_LABELS = {
  ollama: "Ollama",
  gemini: "Google Search",
  openrouter: "OpenRouter",
};

export function RouteModelBadge({ route, provider, model }) {
  const config = ROUTE_CONFIG[route] || {
    label: route || "Unknown route",
    icon: MessageCircle,
    dot: "bg-ink-dim",
    text: "text-ink-dim",
  };
  const Icon = config.icon;
  const providerLabel = PROVIDER_LABELS[provider] || provider;

  return (
    <div className="flex flex-wrap items-center gap-x-3 gap-y-1 text-xs">
      <span className={`inline-flex items-center gap-1.5 ${config.text}`}>
        <Icon size={13} strokeWidth={2} />
        {config.label}
      </span>
      {model && (
        <span className="font-mono text-ink-dim">
          {model}
          {providerLabel ? ` · ${providerLabel}` : ""}
        </span>
      )}
    </div>
  );
}
