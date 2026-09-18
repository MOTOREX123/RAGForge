import { apiClient } from "./client";

/**
 * Send a chat message to the backend.
 *
 * @param {string} message
 * @param {string|null} conversationId
 * @returns {Promise<import('./types').ChatResponse>}
 */
export function sendChatMessage(message, conversationId) {
  return apiClient.post("/api/chat", {
    message,
    conversation_id: conversationId ?? null,
  });
}

/**
 * Check backend/vectorstore/Ollama health.
 */
export function fetchHealth() {
  return apiClient.get("/api/health");
}
