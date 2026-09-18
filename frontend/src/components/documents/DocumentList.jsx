import { useDocuments } from "../../hooks/useDocuments";
import { DocumentRow } from "./DocumentRow";
import { UploadButton } from "./UploadButton";

export function DocumentList() {
  const { documents, status, uploadError, upload, remove } = useDocuments();

  return (
    <div>
      <p className="mb-2 px-2 text-xs font-medium text-ink-dim">Documents</p>

      {status === "loading" && (
        <p className="px-2 text-xs text-ink-dim">Loading…</p>
      )}

      {status === "unavailable" && (
        <p className="px-2 text-xs text-ink-dim">
          Document management isn't wired up on the backend yet. Your 4
          indexed PDFs are already searchable — this panel is ready for
          upload/list/delete once those endpoints exist.
        </p>
      )}

      {status === "error" && (
        <p className="px-2 text-xs text-danger">
          Couldn't reach the backend to list documents.
        </p>
      )}

      {status === "ready" && documents.length === 0 && (
        <p className="px-2 text-xs text-ink-dim">No documents uploaded yet.</p>
      )}

      {status === "ready" && documents.length > 0 && (
        <div className="flex flex-col gap-0.5">
          {documents.map((doc) => (
            <DocumentRow key={doc.id} document={doc} onDelete={remove} />
          ))}
        </div>
      )}

      <div className="mt-3 px-2">
        <UploadButton onUpload={upload} disabled={status === "unavailable"} />
        {uploadError && (
          <p className="mt-1.5 text-xs text-danger">{uploadError}</p>
        )}
      </div>
    </div>
  );
}
