import { useState } from "react";
import { FileText, Loader2, Trash2, TriangleAlert, AlertCircle } from "lucide-react";

const STATUS_ICON = {
  processed: null,
  processing: Loader2,
  failed: TriangleAlert,
};

const STATUS_LABEL = {
  processed: "Ready",
  processing: "Processing",
  failed: "Failed",
};

const STATUS_STYLE = {
  processed: "bg-green-dim/20 text-green",
  processing: "bg-yellow-dim/20 text-yellow",
  failed: "bg-red-dim/20 text-red",
};

export function DocumentRow({ document, onDelete }) {
  const StatusIcon = STATUS_ICON[document.status];
  const [showConfirm, setShowConfirm] = useState(false);

  const handleDelete = () => {
    if (confirm(`Delete "${document.filename}"? This action cannot be undone.`)) {
      onDelete(document.id);
    }
  };

  return (
    <div className="group flex items-center gap-2 rounded-lg px-2 py-1.5 text-sm hover:bg-raised">
      <div className="flex h-8 w-8 shrink-0 items-center justify-center rounded-lg bg-purple-bg text-purple">
        <FileText size={14} />
      </div>
      <div className="min-w-0 flex-1">
        <p className="truncate text-ink">{document.filename}</p>
        <div className="flex items-center gap-1.5 mt-0.5">
          <span className="font-mono text-[10px] text-ink-muted">
            {document.type?.toUpperCase()}
            {Array.isArray(document.pages) && document.pages.length > 0 ? ` · ${document.pages.length}p` : document.pages != null ? ` · ${document.pages}p` : ""}
          </span>
          <span className={`inline-flex items-center gap-1 rounded px-1.5 py-0.5 text-[9px] font-medium ${STATUS_STYLE[document.status] || "bg-line text-ink-muted"}`}>
            {document.chunks != null ? (
              <>
                {document.chunks} chunks · {STATUS_LABEL[document.status] || document.status}
              </>
            ) : (
              STATUS_LABEL[document.status] || document.status
            )}
          </span>
        </div>
      </div>
      {StatusIcon && (
        <StatusIcon
          size={12}
          className={
            document.status === "failed"
              ? "shrink-0 text-red"
              : "shrink-0 animate-spin text-ink-muted"
          }
        />
      )}
      {showConfirm ? (
        <div className="flex items-center gap-1">
          <button
            type="button"
            onClick={() => setShowConfirm(false)}
            className="shrink-0 rounded p-1 text-ink-dim hover:text-ink"
            aria-label="Cancel"
          >
            <span className="text-[10px]">No</span>
          </button>
          <button
            type="button"
            onClick={handleDelete}
            className="shrink-0 rounded p-1 text-red hover:bg-red-dim/10"
            aria-label={`Confirm delete ${document.filename}`}
          >
            <span className="text-[10px]">Yes</span>
          </button>
        </div>
      ) : (
        <button
          type="button"
          onClick={() => setShowConfirm(true)}
          aria-label={`Remove ${document.filename}`}
          className="shrink-0 rounded p-1 text-ink-dim opacity-0 transition-opacity hover:text-red group-hover:opacity-100"
        >
          <Trash2 size={12} />
        </button>
      )}
    </div>
  );
}