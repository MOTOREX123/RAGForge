import { apiClient } from "./client";

/**
 * These map directly to app.py's current placeholder endpoints, which
 * return HTTP 501 until document management is implemented on the
 * backend. Callers should treat a 501 as "not available yet", not as
 * an unexpected error.
 */

/**
 * @returns {Promise<import('./types').DocumentEntry[]>}
 */
export function listDocuments() {
  return apiClient.get("/api/documents").then((response) => response.documents || []);
}

/**
 * @param {File} file
 */
export function uploadDocument(file) {
  const formData = new FormData();
  formData.append("file", file);
  return apiClient.postForm("/api/upload", formData);
}

/**
 * @param {string} documentId
 */
export function deleteDocument(documentId) {
  return apiClient.delete(`/api/documents/${encodeURIComponent(documentId)}`);
}
