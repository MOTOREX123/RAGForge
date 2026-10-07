import { useState, useEffect, useRef } from "react";
import { ChevronDown, ChevronUp, FileText, Copy, ExternalLink, X, Loader2, ChevronUp as ChevronUpIcon } from "lucide-react";
import { useConversation } from "../../context/ConversationContext";
import { useToast } from "../../context/ToastContext";

function formatScore(score) {
  if (score === null || score === undefined) return "N/A";
  return `${(score * 100).toFixed(0)}%`;
}

export function SourcesPanel({ citations, isOpen, onClose, retrievalConfidence, chunksRetrieved }) {
  const [expandedCitation, setExpandedCitation] = useState(null);
  const [copiedCitation, setCopiedCitation] = useState(null);
  const { selectedCitationId, selectCitation } = useConversation();
  const { addToast } = useToast();
  const sourceCardRefs = useRef({});

  const handleCopyChunk = async (citation) => {
    try {
      await navigator.clipboard.writeText(citation.chunk || "");
      setCopiedCitation(citation.id);
      addToast("Chunk copied", "success");
      setTimeout(() => setCopiedCitation(null), 1500);
    } catch {
      // Clipboard access denied
    }
  };

  // Auto-expand and scroll to selected citation
  useEffect(() => {
    if (selectedCitationId) {
      const citation = citations.find((c) => c.id === selectedCitationId);
      if (citation) {
        setExpandedCitation(selectedCitationId);
        // Scroll to the source card
        setTimeout(() => {
          sourceCardRefs.current[selectedCitationId]?.scrollIntoView({ behavior: "smooth", block: "center" });
        }, 100);
      }
    }
  }, [selectedCitationId, citations]);

  const documentCitations = citations.filter((c) => c.type === "document");
  const webCitations = citations.filter((c) => c.type === "web");

  // Always render the panel structure, but handle empty state inside
  return (
    <aside
      className={`transition-transform duration-200 ease-out z-40 ${
        // Desktop: side panel
        "hidden lg:block lg:fixed lg:right-0 lg:top-0 lg:h-full lg:w-[340px] lg:border-l lg:border-line lg:bg-surface lg:translate-x-0 " +
        // Mobile: bottom sheet
        "lg:hidden fixed bottom-0 left-0 right-0 max-h-[70vh] border-t border-line bg-surface rounded-t-2xl " +
        (isOpen ? "translate-y-0" : "translate-y-full")
      }`}
    >
      {/* Mobile drag handle */}
      <div className="lg:hidden flex items-center justify-center py-2">
        <div className="w-8 h-1 bg-line rounded-full" />
      </div>

      {/* Close button for mobile */}
      <div className="lg:hidden absolute top-2 right-2 z-10">
        <button
          type="button"
          onClick={onClose}
          className="rounded p-1.5 text-ink-dim hover:text-ink bg-raised"
          aria-label="Close sources panel"
        >
          <X size={18} />
        </button>
      </div>

      <div className="flex flex-col h-full lg:h-full">
        {/* Header */}
        <div className="flex items-center justify-between border-b border-line px-3 py-2.5 lg:px-3 lg:py-2.5">
          <div className="flex items-center gap-2">
            <FileText size={16} className="text-purple" />
            <h2 className="font-display text-base font-semibold text-ink">Sources / Context</h2>
            {citations.length > 0 && (
              <span className="text-[11px] font-mono text-purple">
                {citations.length}
              </span>
            )}
          </div>
          {/* Desktop close button */}
          <button
            type="button"
            onClick={onClose}
            className="lg:hidden hidden rounded p-1.5 text-ink-dim hover:text-ink"
            aria-label="Close sources"
          >
            <X size={16} />
          </button>
        </div>

        {/* Retrieval Confidence Section */}
        <div className="border-b border-line px-3 py-3 space-y-2">
          <div className="flex items-center justify-between">
            <span className="text-[11px] font-medium text-ink-dim">Retrieval confidence</span>
            <span className="text-[11px] font-mono text-purple">
              {retrievalConfidence !== null && retrievalConfidence !== undefined
                ? (retrievalConfidence * 100).toFixed(0) + "%"
                : "—"}
            </span>
          </div>
          <div className="h-1.5 bg-raised rounded-full overflow-hidden">
            <div
              className="h-full bg-purple transition-all duration-300"
              style={{
                width: retrievalConfidence !== null && retrievalConfidence !== undefined
                  ? `${retrievalConfidence * 100}%`
                  : "0%",
              }}
            />
          </div>
          <p className="text-[10px] text-ink-muted font-mono">
            {chunksRetrieved} chunks retrieved
          </p>
        </div>

        {/* Content */}
        <div className="flex-1 overflow-y-auto px-3 py-3 space-y-3">
          {citations.length === 0 ? (
            <div className="flex flex-col items-center justify-center h-full text-center text-ink-muted">
              <FileText size={32} className="mb-2 opacity-30" />
              <p className="text-sm">No sources retrieved yet</p>
              <p className="text-[10px] mt-1 max-w-xs">
                Ask a question to see retrieved documents here
              </p>
            </div>
          ) : (
            <>
              {documentCitations.length > 0 && (
                <div className="space-y-2">
                  <p className="text-[10px] font-medium uppercase tracking-wider text-ink-muted">
                    Documents
                  </p>
                  {documentCitations.map((citation, index) => (
                    <SourceCard
                      key={citation.id}
                      ref={(el) => { sourceCardRefs.current[citation.id] = el; }}
                      citation={citation}
                      index={index + 1}
                      isExpanded={expandedCitation === citation.id}
                      isSelected={selectedCitationId === citation.id}
                      onToggle={() =>
                        setExpandedCitation(
                          expandedCitation === citation.id ? null : citation.id
                        )
                      }
                      onCopyChunk={handleCopyChunk}
                      copied={copiedCitation === citation.id}
                    />
                  ))}
                </div>
              )}

              {webCitations.length > 0 && (
                <div className="space-y-2 pt-3 border-t border-line">
                  <p className="text-[10px] font-medium uppercase tracking-wider text-ink-muted">
                    Web Sources
                  </p>
                  {webCitations.map((citation, index) => (
                    <WebSourceCard key={citation.id} citation={citation} index={index + 1} />
                  ))}
                </div>
              )}
            </>
          )}
        </div>
      </div>
    </aside>
  );
}

function SourceCard({
  citation,
  index,
  isExpanded,
  isSelected,
  onToggle,
  onCopyChunk,
  copied,
}) {
  const metadata = citation.metadata || {};

  return (
    <div 
      className={`rounded-lg border overflow-hidden transition-all duration-200 ${
        isSelected 
          ? "border-purple bg-purple-bg/10 ring-2 ring-purple/20" 
          : "border-line bg-raised"
      }`}
    >
      {/* Collapsed header */}
      <button
        type="button"
        onClick={onToggle}
        className="flex w-full items-center justify-between gap-2 p-2.5 text-left transition-colors hover:bg-surface"
      >
        <div className="flex items-center gap-2.5 min-w-0 flex-1">
          <span className="flex h-5 w-5 shrink-0 items-center justify-center rounded bg-purple-bg text-purple text-[10px] font-mono font-medium">
            {index}
          </span>
          <div className="min-w-0">
            <p className="truncate text-sm font-medium text-ink">
              {citation.source}
            </p>
            <p className="flex items-center gap-1.5 text-[10px] text-ink-muted">
              {citation.page !== null && citation.page !== undefined && (
                <>
                  <span>p.{citation.page}</span>
                  <span>·</span>
                </>
              )}
              <span>{formatScore(citation.score)}</span>
            </p>
          </div>
        </div>
        <div className="flex items-center gap-1">
          {isExpanded ? (
            <ChevronUp size={13} className="text-ink-muted" />
          ) : (
            <ChevronDown size={13} className="text-ink-muted" />
          )}
        </div>
      </button>

      {/* Expanded content */}
      {isExpanded && (
        <div className="border-t border-line p-2.5 space-y-2.5 bg-surface/50">
          {/* Retrieved chunk */}
          {citation.chunk && (
            <div className="space-y-1.5">
              <p className="text-[10px] font-medium uppercase tracking-wider text-ink-muted">
                Retrieved Chunk
              </p>
              <div className="relative rounded border border-line bg-bg p-2.5 font-mono text-[10px] leading-relaxed text-ink-dim max-h-40 overflow-y-auto">
                <pre className="whitespace-pre-wrap">{citation.chunk}</pre>
                <button
                  type="button"
                  onClick={() => onCopyChunk(citation)}
                  className="absolute top-1.5 right-1.5 rounded p-1 text-ink-dim hover:text-ink"
                  aria-label={copied ? "Copied" : "Copy chunk"}
                >
                  {copied ? (
                    <span className="text-[9px] text-green">Copied</span>
                  ) : (
                    <Copy size={11} />
                  )}
                </button>
              </div>
            </div>
          )}

          {/* Metadata */}
          <div className="rounded border border-line bg-bg p-2.5 space-y-2">
            <p className="text-[10px] font-medium uppercase tracking-wider text-ink-muted">
              Metadata
            </p>
            <div className="grid grid-cols-2 gap-1.5 text-[10px]">
              <div>
                <p className="text-ink-muted">Page</p>
                <p className="font-mono text-ink">
                  {citation.page !== null && citation.page !== undefined
                    ? citation.page
                    : "—"}
                </p>
              </div>
              <div>
                <p className="text-ink-muted">Chunk Index</p>
                <p className="font-mono text-ink">
                  {metadata.chunkIndex !== undefined ? metadata.chunkIndex : "—"}
                </p>
              </div>
              <div>
                <p className="text-ink-muted">Embedding</p>
                <p className="font-mono text-ink truncate">
                  {metadata.embeddingModel || "nomic-embed-text"}
                </p>
              </div>
              <div>
                <p className="text-ink-muted">Rerank Score</p>
                <p className="font-mono text-ink">
                  {citation.score !== null && citation.score !== undefined
                    ? citation.score.toFixed(4)
                    : "—"}
                </p>
              </div>
              {metadata.faissScore !== undefined && (
                <>
                  <div>
                    <p className="text-ink-muted">FAISS Score</p>
                    <p className="font-mono text-ink">
                      {metadata.faissScore.toFixed(4)}
                    </p>
                  </div>
                  <div>
                    <p className="text-ink-muted">Hybrid Score</p>
                    <p className="font-mono text-ink">
                      {metadata.hybridScore?.toFixed(4) || "—"}
                    </p>
                  </div>
                </>
              )}
            </div>
          </div>
        </div>
      )}
    </div>
  );
}

function WebSourceCard({ citation, index }) {
  return (
    <div className="rounded-lg border border-line bg-raised p-2.5">
      <div className="flex items-start gap-2.5">
        <span className="flex h-5 w-5 shrink-0 items-center justify-center rounded bg-green-dim/30 text-green text-[10px] font-mono font-medium">
          {index}
        </span>
        <div className="flex-1 min-w-0">
          <p className="truncate text-sm font-medium text-ink">
            {citation.source}
          </p>
          {citation.url && (
            <a
              href={citation.url}
              target="_blank"
              rel="noopener noreferrer"
              className="flex items-center gap-1 text-[10px] text-green hover:underline"
            >
              <ExternalLink size={9} />
              View source
            </a>
          )}
        </div>
      </div>
    </div>
  );
}