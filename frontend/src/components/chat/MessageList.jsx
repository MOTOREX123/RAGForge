import { useEffect, useRef } from "react";
import { MessageBubble } from "./MessageBubble";
import { TypingIndicator } from "./TypingIndicator";
import { EmptyState } from "./EmptyState";

export function MessageList({ messages, isLoading, onRegenerate, onRetry, onSuggestion, retrievalConfidence, chunksRetrieved }) {
  const bottomRef = useRef(null);

  useEffect(() => {
    bottomRef.current?.scrollIntoView({ behavior: "smooth", block: "end" });
  }, [messages.length, isLoading]);

  if (messages.length === 0 && !isLoading) {
    return <EmptyState onSuggestion={onSuggestion} />;
  }

  const lastAssistantId = [...messages].reverse().find((m) => m.role === "assistant")?.id;

  return (
    <div className="flex w-full flex-1 flex-col gap-4 overflow-y-auto px-4 py-4">
      {messages.map((message) => (
        <MessageBubble
          key={message.id}
          message={message}
          onRegenerate={onRegenerate}
          onRetry={onRetry}
          isLastAssistant={message.id === lastAssistantId && !isLoading}
          retrievalConfidence={retrievalConfidence}
          chunksRetrieved={chunksRetrieved}
        />
      ))}
      {isLoading && <TypingIndicator />}
      <div ref={bottomRef} />
    </div>
  );
}