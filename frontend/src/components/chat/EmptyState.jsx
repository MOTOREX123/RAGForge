const SUGGESTIONS = [
  "What is overfitting?",
  "Summarize the key ideas behind agentic AI.",
  "What's the latest stable Python version?",
];

export function EmptyState({ onSuggestion }) {
  return (
    <div className="flex h-full flex-col items-center justify-center px-6 text-center">
      <h1 className="font-display text-2xl text-ink">
        Ask something, cite everything.
      </h1>
      <p className="mt-2 max-w-sm text-sm text-ink-dim">
        Questions about your documents are answered with page-level
        citations. Time-sensitive questions are routed to the web instead.
      </p>
      <div className="mt-6 flex flex-col gap-2">
        {SUGGESTIONS.map((text) => (
          <button
            key={text}
            type="button"
            onClick={() => onSuggestion(text)}
            className="rounded border border-line px-3 py-2 text-left text-sm text-ink-dim transition-colors hover:border-brass/40 hover:text-ink"
          >
            {text}
          </button>
        ))}
      </div>
    </div>
  );
}
