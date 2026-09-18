import { Menu } from "lucide-react";
import { MessageList } from "../chat/MessageList";
import { ChatInput } from "../chat/ChatInput";
import { useConversation } from "../../context/ConversationContext";

export function MainPanel({ onOpenSidebar }) {
  const { messages, isLoading, sendMessage, regenerate } = useConversation();

  return (
    <div className="flex h-full flex-1 flex-col bg-bg">
      <div className="flex items-center gap-3 border-b border-line px-4 py-3 md:hidden">
        <button
          type="button"
          onClick={onOpenSidebar}
          aria-label="Open sidebar"
          className="text-ink-dim"
        >
          <Menu size={18} />
        </button>
        <span className="font-display text-sm text-ink">MultiDocumentRAG</span>
      </div>
      <MessageList
        messages={messages}
        isLoading={isLoading}
        onRegenerate={regenerate}
        onSuggestion={sendMessage}
      />
      <ChatInput onSend={sendMessage} disabled={isLoading} />
    </div>
  );
}
