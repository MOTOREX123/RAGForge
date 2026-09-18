import { createContext, useContext } from "react";
import { useChat } from "../hooks/useChat";

const ConversationContext = createContext(null);

export function ConversationProvider({ children }) {
  const chat = useChat();
  return (
    <ConversationContext.Provider value={chat}>
      {children}
    </ConversationContext.Provider>
  );
}

export function useConversation() {
  const ctx = useContext(ConversationContext);
  if (!ctx) {
    throw new Error("useConversation must be used within a ConversationProvider");
  }
  return ctx;
}
