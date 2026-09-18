import { FileText, Loader2, Trash2, TriangleAlert } from "lucide-react";

const STATUS_ICON = {
  processed: null,
  processing: Loader2,
  failed: TriangleAlert,
};

export function DocumentRow({ document, onDelete }) {
  const StatusIcon = STATUS_ICON[document.status];

  return (
    <div className="group flex items-center gap-2 rounded px-2 py-1.5 text-sm hover:bg-raised">
      <FileText size={14} className="shrink-0 text-ink-dim" />
      <div className="min-w-0 flex-1">
        <p className="truncate text-ink">{document.filename}</p>
        <p className="font-mono text-[11px] text-ink-dim">
          {document.type?.toUpperCase()}
          {document.pages != null ? ` · ${document.pages}p` : ""}
        </p>
      </div>
      {StatusIcon && (
        <StatusIcon
          size={13}
          className={
            document.status === "failed"
              ? "shrink-0 text-danger"
              : "shrink-0 animate-spin text-ink-dim"
          }
        />
      )}
      <button
        type="button"
        onClick={() => onDelete(document.id)}
        aria-label={`Remove ${document.filename}`}
        className="shrink-0 rounded p-1 text-ink-dim opacity-0 transition-opacity hover:text-danger group-hover:opacity-100"
      >
        <Trash2 size={13} />
      </button>
    </div>
  );
}
