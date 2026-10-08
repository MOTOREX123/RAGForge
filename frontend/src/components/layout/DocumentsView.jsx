import { useDocuments } from "../../hooks/useDocuments";
import { DocumentRow } from "../documents/DocumentRow";
import { UploadButton } from "../documents/UploadButton";
import { Search, Filter, Loader2, Download, Trash2, MoreHorizontal, FileText } from "lucide-react";
import { useState } from "react";
import { useToast } from "../../context/ToastContext";

const STATUS_FILTERS = [
  { id: "all", label: "All" },
  { id: "processed", label: "Ready" },
  { id: "processing", label: "Processing" },
  { id: "failed", label: "Failed" },
];

export function DocumentsView() {
  const { documents, status, uploadError, upload, remove } = useDocuments();
  const { addToast } = useToast();
  const [searchQuery, setSearchQuery] = useState("");
  const [statusFilter, setStatusFilter] = useState("all");
  const [showMenuFor, setShowMenuFor] = useState(null);

  const handleUploadSuccess = () => {
    addToast("Document uploaded successfully", "success");
  };

  const filteredDocuments = documents
    .filter((doc) => {
      if (statusFilter !== "all" && doc.status !== statusFilter) return false;
      if (searchQuery && !doc.filename.toLowerCase().includes(searchQuery.toLowerCase())) return false;
      return true;
    })
    .sort((a, b) => {
      const statusOrder = { processed: 0, processing: 1, failed: 2 };
      return (statusOrder[a.status] || 3) - (statusOrder[b.status] || 3);
    });

  const handleMenuClick = (e, filename) => {
    e.stopPropagation();
    setShowMenuFor(showMenuFor === filename ? null : filename);
  };

  const handleDelete = (filename) => {
    if (confirm(`Delete "${filename}"? This action cannot be undone.`)) {
      remove(filename);
    }
    setShowMenuFor(null);
  };

  const handleDownload = (doc) => {
    console.log("Download document:", doc.id);
    setShowMenuFor(null);
  };

  return (
    <div className="flex h-full flex-col bg-bg">
      {/* Header */}
      <div className="border-b border-line px-4 py-3">
        <div className="flex items-center justify-between mb-3">
          <div className="flex items-center gap-2.5">
            <img
              src="/assets/ragforge-logo.png"
              alt="RAGForge"
              className="w-6 h-6"
            />
            <div>
              <h1 className="font-display text-lg font-semibold text-ink">Documents</h1>
              <p className="text-[11px] text-ink-muted">Manage your knowledge base</p>
            </div>
          </div>
          <UploadButton onUpload={upload} disabled={status === "unavailable"} variant="primary" onSuccess={handleUploadSuccess} />
        </div>

        {/* Search and filters */}
        <div className="flex flex-col sm:flex-row gap-2">
          <div className="relative flex-1">
            <Search className="absolute left-2.5 top-1/2 -translate-y-1/2 text-ink-muted" size={16} />
            <input
              type="text"
              value={searchQuery}
              onChange={(e) => setSearchQuery(e.target.value)}
              placeholder="Search documents…"
              className="w-full rounded-lg border border-line bg-surface pl-9 pr-3 py-2 text-sm text-ink placeholder:text-ink-muted focus:border-purple/50 focus:outline-none"
            />
          </div>
          <div className="flex items-center gap-1.5">
            <Filter className="text-ink-muted" size={16} />
            <select
              value={statusFilter}
              onChange={(e) => setStatusFilter(e.target.value)}
              className="rounded-lg border border-line bg-surface px-2.5 py-2 text-sm text-ink focus:border-purple/50 focus:outline-none"
            >
              {STATUS_FILTERS.map((f) => (
                <option key={f.id} value={f.id}>{f.label}</option>
              ))}
            </select>
          </div>
        </div>
      </div>

      {/* Document list */}
      <div className="flex-1 overflow-y-auto px-4 py-3">
        {status === "loading" && (
          <div className="flex items-center justify-center h-full">
            <Loader2 className="animate-spin text-purple" size={20} />
          </div>
        )}

        {status === "unavailable" && (
          <div className="text-center py-8">
            <p className="text-ink-muted">
              Document management isn&apos;t wired up on the backend yet. Your indexed
              documents are already searchable — this panel is ready for
              upload/list/delete once those endpoints exist.
            </p>
          </div>
        )}

        {status === "error" && (
          <div className="text-center py-8 text-red">
            Couldn&apos;t reach the backend to list documents.
          </div>
        )}

        {status === "ready" && filteredDocuments.length === 0 && searchQuery && (
          <div className="text-center py-8 text-ink-muted">
            No documents match "{searchQuery}".
          </div>
        )}

        {status === "ready" && filteredDocuments.length === 0 && !searchQuery && (
          <div className="text-center py-8">
            <p className="text-ink-muted mb-3">No documents uploaded yet.</p>
<UploadButton onUpload={upload} disabled={status === "unavailable"} variant="primary" onSuccess={handleUploadSuccess} />
          </div>
        )}

        {status === "ready" && filteredDocuments.length > 0 && (
          <div className="space-y-1.5">
            {filteredDocuments.map((doc) => (
              <DocumentRowWithMenu
                key={doc.filename}
                document={doc}
                onDelete={remove}
                showMenu={showMenuFor === doc.filename}
                onMenuClick={(e) => handleMenuClick(e, doc.filename)}
                onDownload={() => handleDownload(doc)}
                onDeleteConfirm={() => handleDelete(doc.filename)}
              />
            ))}
          </div>
        )}
      </div>

      {uploadError && (
        <div className="border-t border-line px-4 py-2 text-sm text-red">
          {uploadError}
        </div>
      )}
    </div>
  );
}

function DocumentRowWithMenu({ document, onDelete, showMenu, onMenuClick, onDownload, onDeleteConfirm }) {
  const STATUS_ICON = {
    processed: null,
    processing: Loader2,
    failed: null,
  };

  const StatusIcon = STATUS_ICON[document.status];

  return (
    <div className="relative group">
      <div className="group flex items-center gap-2.5 rounded-lg border border-line bg-surface px-3 py-2.5 transition-colors hover:border-purple/30">
        <div className="flex h-9 w-9 shrink-0 items-center justify-center rounded-lg bg-purple-bg text-purple">
          <FileText size={18} />
        </div>
        <div className="min-w-0 flex-1">
          <p className="truncate text-sm font-medium text-ink">{document.filename}</p>
          <div className="flex items-center gap-2 mt-0.5">
            <span className="font-mono text-[10px] text-ink-muted">
              {document.type?.toUpperCase()}
              {Array.isArray(document.pages) && document.pages.length > 0 ? ` · ${document.pages.length}p` : document.pages != null ? ` · ${document.pages}p` : ""}
            </span>
            <StatusBadge status={document.status} />
          </div>
        </div>
        {StatusIcon && (
          <StatusIcon
            size={14}
            className={
              document.status === "failed"
                ? "shrink-0 text-red"
                : "shrink-0 animate-spin text-ink-muted"
            }
          />
        )}
        <button
          type="button"
          onClick={onMenuClick}
          className="shrink-0 rounded p-1 text-ink-muted opacity-0 transition-opacity hover:text-ink group-hover:opacity-100"
          aria-label={`Options for ${document.filename}`}
        >
          <MoreHorizontal size={14} />
        </button>
      </div>

      {showMenu && (
        <div className="absolute right-3 top-full mt-1 z-10 rounded-lg border border-line bg-raised py-1 shadow-lg min-w-[140px]">
          <button
            type="button"
            onClick={onDownload}
            className="flex w-full items-center gap-2 px-3 py-1.5 text-sm text-ink hover:bg-surface"
          >
            <Download size={13} />
            Download
          </button>
          <button
            type="button"
            onClick={onDeleteConfirm}
            className="flex w-full items-center gap-2 px-3 py-1.5 text-sm text-red hover:bg-red-dim"
          >
            <Trash2 size={13} />
            Delete
          </button>
        </div>
      )}
    </div>
  );
}

function StatusBadge({ status }) {
  const styles = {
    processed: "bg-green-dim/20 text-green",
    processing: "bg-yellow-dim/20 text-yellow",
    failed: "bg-red-dim/20 text-red",
  };
  const labels = {
    processed: "Ready",
    processing: "Processing",
    failed: "Failed",
  };

  return (
    <span className={`inline-flex items-center gap-1 rounded px-1.5 py-0.5 text-[9px] font-medium ${styles[status] || "bg-line text-ink-muted"}`}>
      {labels[status] || status}
    </span>
  );
}