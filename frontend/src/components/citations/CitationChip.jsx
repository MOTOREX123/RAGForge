/**
 * A single citation.
 *
 * Document citation:
 * [1] filename.pdf · p.42 · score 3.08
 *
 * Web citation:
 * [1] webpage title
 */
export function CitationChip({ citation }) {
  const isWeb = citation.type === "web";

  const className =
    "inline-flex max-w-full items-center gap-1.5 rounded border " +
    "border-paper-ink/10 bg-paper px-2 py-1 text-xs text-paper-ink";

  return (
    <span className={className}>
      {/* Citation number */}
      <span className="font-mono tabular-nums font-medium shrink-0">
        [{citation.id}]
      </span>

      {/* Source / filename */}
      <span className="truncate">
        {citation.source}
      </span>

      {/* Document page */}
      {!isWeb &&
        citation.page !== null &&
        citation.page !== undefined && (
          <span className="whitespace-nowrap">
            · p.{citation.page}
          </span>
        )}

      {/* Reranker score */}
      {!isWeb &&
        citation.score !== null &&
        citation.score !== undefined && (
          <span className="whitespace-nowrap">
            · score {Number(citation.score).toFixed(2)}
          </span>
        )}
    </span>
  );
}