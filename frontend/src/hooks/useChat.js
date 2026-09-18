import { useCallback, useRef, useState } from "react";
import { sendChatMessage } from "../api/chat";
import { ApiError } from "../api/client";

function makeId() {
  return typeof crypto !== "undefined" && crypto.randomUUID
    ? crypto.randomUUID()
    : `${Date.now()}-${Math.random().toString(16).slice(2)}`;
}

/**
 * Owns the message list for a single conversation and talks to the
 * backend through src/api/chat.js. No AI/routing logic lives here —
 * this only manages UI state around one endpoint call.
 */
export function useChat() {
  const [messages, setMessages] = useState(/** @type {import('../api/types').ChatMessage[]} */ ([]));
  const [isLoading, setIsLoading] = useState(false);
  const conversationId = useRef(makeId());

  const runRequest = useCallback(async (text) => {
    setIsLoading(true);
    try {
      const response = await sendChatMessage(text, conversationId.current);
      setMessages((prev) => [
        ...prev,
        {
          id: makeId(),
          role: "assistant",
          content: response.answer,
          route: response.route,
          provider: response.provider,
          model: response.model,
          citations: response.citations || [],
        },
      ]);
    } catch (error) {
      const detail =
        error instanceof ApiError
          ? error.detail || error.message
          : "Something went wrong talking to the backend.";
      setMessages((prev) => [
        ...prev,
        {
          id: makeId(),
          role: "assistant",
          content: detail,
          isError: true,
        },
      ]);
    } finally {
      setIsLoading(false);
    }
  }, []);

  const sendMessage = useCallback(
    (text) => {
      const trimmed = text.trim();
      if (!trimmed || isLoading) return;

      setMessages((prev) => [
        ...prev,
        { id: makeId(), role: "user", content: trimmed },
      ]);
      runRequest(trimmed);
    },
    [isLoading, runRequest],
  );

  /**
   * There is no dedicated /api/chat/regenerate endpoint yet, so this
   * re-sends the last user message rather than pretending a backend
   * feature exists. When the endpoint is added later, only this
   * function needs to change.
   */
  const regenerate = useCallback(() => {
    if (isLoading) return;
    const lastUserMessage = [...messages].reverse().find((m) => m.role === "user");
    if (!lastUserMessage) return;
    runRequest(lastUserMessage.content);
  }, [messages, isLoading, runRequest]);

  const clearConversation = useCallback(() => {
    setMessages([]);
    conversationId.current = makeId();
  }, []);

  return { messages, isLoading, sendMessage, regenerate, clearConversation };
}
