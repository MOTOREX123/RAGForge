import { useEffect, useRef } from "react";
import { MessageBubble } from "./MessageBubble";
import { TypingIndicator } from "./TypingIndicator";
import { EmptyState } from "./EmptyState";

export function MessageList({ messages, isLoading, onRegenerate, onSuggestion }) {
  const bottomRef = useRef(null);

  useEffect(() => {
    bottomRef.current?.scrollIntoView({ behavior: "smooth", block: "end" });
  }, [messages.length, isLoading]);

  if (messages.length === 0 && !isLoading) {
    return <EmptyState onSuggestion={onSuggestion} />;
  }

  const lastAssistantId = [...messages].reverse().find((m) => m.role === "assistant")?.id;

  return (
    <div className="mx-auto flex w-full max-w-prose flex-1 flex-col gap-5 overflow-y-auto px-4 py-6">
      {messages.map((message) => (
        <MessageBubble
          key={message.id}
          message={message}
          onRegenerate={onRegenerate}
          isLastAssistant={message.id === lastAssistantId && !isLoading}
        />
      ))}
      {isLoading && <TypingIndicator />}
      <div ref={bottomRef} />
    </div>
  );
}
