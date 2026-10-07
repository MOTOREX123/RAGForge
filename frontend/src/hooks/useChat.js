import { useCallback, useEffect, useRef, useState } from "react";
import { sendChatMessage } from "../api/chat";
import { ApiError } from "../api/client";

function makeId() {
  return typeof crypto !== "undefined" && crypto.randomUUID
    ? crypto.randomUUID()
    : `${Date.now()}-${Math.random().toString(16).slice(2)}`;
}

function getHumanReadableError(error) {
  if (error instanceof ApiError) {
    if (error.status === null) {
      return "Unable to connect to the backend. Is the server running?";
    }
    if (error.status === 500) {
      return "Backend error. Please try again.";
    }
    if (error.status === 503) {
      return "Service temporarily unavailable. Please try again.";
    }
    if (error.status === 502 || error.status === 500) {
      // The backend forwards raw Ollama/provider errors on these codes;
      // show a friendly state instead of leaking internals into the chat.
      return "The answer service (Ollama) is unavailable right now. Please try again in a moment.";
    }
    if (error.status === 404) {
      return "Endpoint not found. Please check the backend configuration.";
    }
    return error.detail || error.message || "Something went wrong talking to the backend.";
  }
  if (error.name === "AbortError") {
    return "Generation stopped.";
  }
  return "Something went wrong. Please try again.";
}

/**
 * Owns the message list for a single conversation and talks to the
 * backend through src/api/chat.js. No AI/routing logic lives here —
 * this only manages UI state around one endpoint call.
 */
export function useChat() {
  const [messages, setMessages] = useState(
    /** @type {import('../api/types').ChatMessage[]} */ ([])
  );
  const [isLoading, setIsLoading] = useState(false);
  const [pipelineStatus, setPipelineStatus] = useState(null); // 'generating' | null
  const [speakingId, setSpeakingId] = useState(null); // id of assistant msg being presented
  const conversationId = useRef(makeId());
  const abortControllerRef = useRef(null);
  const lastUserMessageRef = useRef(null);
  const pendingErrorRef = useRef(null);
  const speakTimerRef = useRef(null);

  // Append an assistant response and animate the bot "speaking" for a
  // duration bounded to the answer length (purely presentational).
  const pushAssistant = useCallback((response) => {
    const id = makeId();
    setMessages((prev) => [
      ...prev,
      {
        id,
        role: "assistant",
        content: response.answer,
        route: response.route,
        provider: response.provider,
        model: response.model,
        citations: response.citations,
        timestamp: Date.now(),
        conversationId: conversationId.current,
      },
    ]);
    setSpeakingId(id);
    clearTimeout(speakTimerRef.current);
    const speakMs = Math.min(2500 + (response.answer?.length || 0) * 12, 9000);
    speakTimerRef.current = setTimeout(() => setSpeakingId(null), speakMs);
  }, []);

  const pushError = useCallback((detail) => {
    setMessages((prev) => [
      ...prev,
      {
        id: makeId(),
        role: "assistant",
        content: detail,
        isError: true,
        timestamp: Date.now(),
        conversationId: conversationId.current,
      },
    ]);
  }, []);

  const runRequest = useCallback(async (text, conversationIdRef) => {
    setIsLoading(true);
    setPipelineStatus("generating");
    lastUserMessageRef.current = text;

    abortControllerRef.current = new AbortController();

    try {
      const response = await sendChatMessage(text, conversationIdRef.current);
      setPipelineStatus(null);
      pendingErrorRef.current = null;

      // Enhance citations with chunk text if available from backend
      const enhancedCitations = (response.citations || []).map((c) => ({
        ...c,
        chunk: c.chunk || null,
        metadata: c.metadata || {},
      }));

      return {
        answer: response.answer,
        route: response.route,
        provider: response.provider,
        model: response.model,
        citations: enhancedCitations,
      };
    } catch (error) {
      setPipelineStatus(null);
      pendingErrorRef.current = error;
      throw error;
    } finally {
      setIsLoading(false);
    }
  }, []);

  const sendMessage = useCallback(
    (text) => {
      const trimmed = text.trim();
      if (!trimmed || isLoading) return;

      const userMessage = {
        id: makeId(),
        role: "user",
        content: trimmed,
        timestamp: Date.now(),
        conversationId: conversationId.current,
      };

      setMessages((prev) => [...prev, userMessage]);
      runRequest(trimmed, conversationId).then(pushAssistant).catch((error) => {
        pushError(getHumanReadableError(error));
      });
    },
    [isLoading, runRequest, pushAssistant, pushError]
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

    // Remove the last assistant message if it exists
    const lastAssistantIndex = [...messages].reverse().findIndex(
      (m) => m.role === "assistant"
    );
    if (lastAssistantIndex !== -1) {
      const actualIndex = messages.length - 1 - lastAssistantIndex;
      setMessages((prev) => prev.filter((_, i) => i !== actualIndex));
    }

    runRequest(lastUserMessage.content, conversationId).then(pushAssistant).catch((error) => {
      pushError(getHumanReadableError(error));
    });
  }, [messages, isLoading, runRequest, pushAssistant, pushError]);

  const retry = useCallback(() => {
    if (isLoading) return;
    const lastUserMessage = lastUserMessageRef.current;
    if (!lastUserMessage) return;

    // Remove the last error message if it exists
    const lastMessage = messages[messages.length - 1];
    if (lastMessage?.isError) {
      setMessages((prev) => prev.slice(0, -1));
    }

    runRequest(lastUserMessage, conversationId).then(pushAssistant).catch((error) => {
      pushError(getHumanReadableError(error));
    });
  }, [isLoading, messages.length, runRequest, pushAssistant, pushError]);

  const stopGeneration = useCallback(() => {
    if (abortControllerRef.current) {
      abortControllerRef.current.abort();
    }
    setIsLoading(false);
    setPipelineStatus(null);
    setSpeakingId(null);
  }, []);

  const clearConversation = useCallback(() => {
    setMessages([]);
    conversationId.current = makeId();
    setPipelineStatus(null);
    setSpeakingId(null);
    clearTimeout(speakTimerRef.current);
    lastUserMessageRef.current = null;
    pendingErrorRef.current = null;
  }, []);

  useEffect(() => () => clearTimeout(speakTimerRef.current), []);

  return {
    messages,
    isLoading,
    pipelineStatus,
    speakingId,
    sendMessage,
    regenerate,
    retry,
    stopGeneration,
    clearConversation,
    conversationId: conversationId.current,
    hasPendingError: !!pendingErrorRef.current,
  };
}