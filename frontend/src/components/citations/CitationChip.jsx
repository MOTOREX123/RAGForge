/**
 * A single citation.
 *
 * Document citation:
 * [1] filename.pdf · p.42 · score 3.08
 *
 * Web citation:
 * [1] webpage title
 */
export function CitationChip({ citation, onClick }) {
  const isWeb = citation.type === "web";

  return (
    <button
      type="button"
      onClick={() => onClick?.(citation)}
      className="inline-flex max-w-full items-center gap-1.5 rounded border border-line bg-raised px-2 py-1 text-[10px] text-ink transition-colors hover:bg-surface hover:border-purple/50 hover:text-purple focus:outline-none focus:ring-2 focus:ring-purple/50"
      aria-label={`View source: ${citation.source}`}
    >
      {/* Citation number */}
      <span className="font-mono tabular-nums font-medium shrink-0 text-purple">
        [{citation.id}]
      </span>

      {/* Source / filename */}
      <span className="truncate max-w-[180px]">
        {citation.source}
      </span>

      {/* Document page */}
      {!isWeb &&
        citation.page !== null &&
        citation.page !== undefined && (
          <span className="whitespace-nowrap text-ink-muted">
            · p.{citation.page}
          </span>
        )}

      {/* Reranker score */}
      {!isWeb &&
        citation.score !== null &&
        citation.score !== undefined && (
          <span className="whitespace-nowrap text-ink-muted">
            · {(citation.score * 100).toFixed(0)}%
          </span>
        )}
    </button>
  );
}