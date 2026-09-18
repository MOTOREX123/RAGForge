import { useCallback, useEffect, useState } from "react";
import { listDocuments, uploadDocument, deleteDocument } from "../api/documents";
import { ApiError } from "../api/client";

/**
 * Manages the Documents sidebar section. The backend endpoints are
 * currently honest 501 placeholders, so this hook surfaces a distinct
 * "not implemented yet" state rather than showing an empty list (which
 * would look like "you have zero documents" instead of "this feature
 * isn't wired up yet").
 */
export function useDocuments() {
  const [documents, setDocuments] = useState(/** @type {import('../api/types').DocumentEntry[]} */ ([]));
  const [status, setStatus] = useState("loading"); // loading | ready | unavailable | error
  const [uploadError, setUploadError] = useState(null);

  const refresh = useCallback(async () => {
    setStatus("loading");
    try {
      const docs = await listDocuments();
      setDocuments(docs || []);
      setStatus("ready");
    } catch (error) {
      if (error instanceof ApiError && error.status === 501) {
        setStatus("unavailable");
      } else {
        setStatus("error");
      }
    }
  }, []);

  useEffect(() => {
    refresh();
  }, [refresh]);

  const upload = useCallback(async (file) => {
    setUploadError(null);
    try {
      await uploadDocument(file);
      await refresh();
    } catch (error) {
      const detail =
        error instanceof ApiError && error.status === 501
          ? "Document upload isn't available yet."
          : error?.detail || "Upload failed.";
      setUploadError(detail);
    }
  }, [refresh]);

  const remove = useCallback(async (documentId) => {
    try {
      await deleteDocument(documentId);
      await refresh();
    } catch {
      // Deletion is also a 501 placeholder right now; nothing to
      // reconcile locally since we never optimistically removed it.
    }
  }, [refresh]);

  return { documents, status, uploadError, upload, remove };
}
