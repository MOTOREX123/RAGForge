import { FileText, Search, GitCompare, Lightbulb, MessageSquare } from "lucide-react";
import { BotAvatar } from "./BotAvatar";

const EXAMPLE_PROMPTS = [
  {
    label: "Summarize the deployment runbook",
    description: "Get a concise overview with citations",
  },
  {
    label: "What changed in the v2 API?",
    description: "Extract key changes from changelogs",
  },
  {
    label: "Find the retry policy for failed jobs",
    description: "Search for specific configuration details",
  },
  {
    label: "Explain the rollback sequence",
    description: "Get step-by-step procedures with sources",
  },
];

export function EmptyState({ onSuggestion, retrievalConfidence, chunksRetrieved }) {
  return (
    <div className="flex flex-1 flex-col items-center justify-center px-4 text-center">
      <div className="mb-4 flex flex-col items-center gap-3">
        <BotAvatar state="idle" size="md" className="w-16 h-16" />
        <img
          src="/assets/ragforge-logo.png"
          alt="RAGForge"
          className="mx-auto w-16 h-16 opacity-60"
        />
      </div>
      <h1 className="font-display text-xl font-semibold text-ink">
        Ask your knowledge base
      </h1>
      <p className="mt-1.5 max-w-xl text-sm text-ink-muted leading-relaxed">
        Search across indexed documents with grounded answers and traceable context.
      </p>

      <div className="mt-5 w-full max-w-xl">
        <p className="mb-2.5 text-left text-[11px] font-medium uppercase tracking-wider text-ink-muted">
          Example prompts
        </p>
        <div className="grid grid-cols-2 gap-2">
          {EXAMPLE_PROMPTS.map(({ label, description }) => (
            <button
              key={label}
              type="button"
              onClick={() => onSuggestion(label)}
              className="group relative rounded-lg border border-line bg-surface p-3 text-left transition-colors hover:border-purple/40 hover:bg-raised hover:text-ink"
            >
              <div className="flex items-start gap-2.5">
                <div className="flex h-8 w-8 shrink-0 items-center justify-center rounded bg-purple-bg text-purple">
                  <MessageSquare size={16} strokeWidth={2} />
                </div>
                <div className="min-w-0">
                  <p className="font-medium text-ink group-hover:text-purple text-sm leading-snug">
                    {label}
                  </p>
                  <p className="text-[10px] text-ink-muted mt-0.5">{description}</p>
                </div>
              </div>
            </button>
          ))}
        </div>
      </div>

      <div className="mt-5 flex items-center justify-center gap-4 text-[10px] text-ink-muted">
        <span className="flex items-center gap-1.5">
          <FileText size={11} />
          Local RAG (Ollama)
        </span>
        <span className="flex items-center gap-1.5">
          <Search size={11} />
          Web Search (Gemini)
        </span>
      </div>
    </div>
  );
}