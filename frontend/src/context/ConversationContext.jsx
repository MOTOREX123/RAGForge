import { createContext, useContext, useState, useCallback, useMemo, useRef } from "react";
import { useChat } from "../hooks/useChat";

const ConversationContext = createContext(null);

function generateId() {
  return typeof crypto !== "undefined" && crypto.randomUUID
    ? crypto.randomUUID()
    : `${Date.now()}-${Math.random().toString(16).slice(2)}`;
}

function generateTitle(firstMessage) {
  const text = firstMessage.slice(0, 50);
  return text.length < firstMessage.length ? text + "…" : text;
}

export function ConversationProvider({ children }) {
  const chat = useChat();
  const [conversations, setConversations] = useState([]);
  const [activeConversationId, setActiveConversationId] = useState(null);
  const [activeNav, setActiveNav] = useState("chats");
  const [sidebarOpen, setSidebarOpen] = useState(false);
  const [lastCitations, setLastCitations] = useState([]);
  const [sourcesOpen, setSourcesOpen] = useState(false);
  const [selectedCitationId, setSelectedCitationId] = useState(null);
  const chatInputRef = useRef(null);

  const activeConversation = useMemo(
    () => conversations.find((c) => c.id === activeConversationId) || null,
    [conversations, activeConversationId]
  );

  const createConversation = useCallback(() => {
    const id = generateId();
    const newConv = {
      id,
      title: "New Chat",
      messages: [],
      createdAt: Date.now(),
      updatedAt: Date.now(),
    };
    setConversations((prev) => [newConv, ...prev]);
    setActiveConversationId(id);
    setActiveNav("chats");
    return id;
  }, []);

  const switchConversation = useCallback((id) => {
    setActiveConversationId(id);
    setActiveNav("chats");
  }, []);

  const deleteConversation = useCallback((id) => {
    setConversations((prev) => prev.filter((c) => c.id !== id));
    if (activeConversationId === id) {
      const remaining = conversations.filter((c) => c.id !== id);
      setActiveConversationId(remaining[0]?.id || null);
    }
  }, [activeConversationId, conversations]);

  const updateConversationTitle = useCallback((id, title) => {
    setConversations((prev) =>
      prev.map((c) =>
        c.id === id ? { ...c, title, updatedAt: Date.now() } : c
      )
    );
  }, []);

  const addMessageToActive = useCallback((message) => {
    if (!activeConversationId) return;
    setConversations((prev) =>
      prev.map((c) => {
        if (c.id !== activeConversationId) return c;
        const updatedMessages = [...c.messages, message];
        const newTitle =
          c.messages.length === 0 && message.role === "user"
            ? generateTitle(message.content)
            : c.title;
        return {
          ...c,
          messages: updatedMessages,
          title: newTitle,
          updatedAt: Date.now(),
        };
      })
    );
  }, [activeConversationId]);

  const replaceActiveMessages = useCallback((messages) => {
    if (!activeConversationId) return;
    setConversations((prev) =>
      prev.map((c) =>
        c.id === activeConversationId
          ? { ...c, messages, updatedAt: Date.now() }
          : c
      )
    );
  }, [activeConversationId]);

  const clearActiveConversation = useCallback(() => {
    if (!activeConversationId) return;
    replaceActiveMessages([]);
  }, [activeConversationId, replaceActiveMessages]);

  const setChatInputRef = useCallback((ref) => {
    chatInputRef.current = ref;
  }, []);

  const focusChatInput = useCallback(() => {
    chatInputRef.current?.focus();
  }, []);

  const selectCitation = useCallback((citation) => {
    if (citation) {
      setSelectedCitationId(citation.id);
      setSourcesOpen(true);
    } else {
      setSelectedCitationId(null);
    }
  }, []);

  const value = {
    ...chat,
    conversations,
    activeConversation,
    activeConversationId,
    activeNav,
    setActiveNav,
    createConversation,
    switchConversation,
    deleteConversation,
    updateConversationTitle,
    addMessageToActive,
    replaceActiveMessages,
    clearActiveConversation,
    sidebarOpen,
    setSidebarOpen,
    lastCitations,
    setLastCitations,
    sourcesOpen,
    setSourcesOpen,
    selectedCitationId,
    selectCitation,
    setChatInputRef,
    focusChatInput,
  };

  return (
    <ConversationContext.Provider value={value}>
      {children}
    </ConversationContext.Provider>
  );
}

export function useConversation() {
  const ctx = useContext(ConversationContext);
  if (!ctx) {
    throw new Error(
      "useConversation must be used within a ConversationProvider"
    );
  }
  return ctx;
}