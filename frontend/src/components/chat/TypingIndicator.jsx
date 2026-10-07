import { BotAvatar } from "./BotAvatar";

export function TypingIndicator() {
  return (
    <div className="flex gap-2.5">
      {/* Avatar indicator */}
      <BotAvatar state="thinking" />

      <div className="flex-1 min-w-0">
        <div className="rounded-xl border-l-3 border-purple bg-surface px-4 py-3">
          <div className="flex items-center gap-2">
            <span className="text-[13px] leading-relaxed text-ink">
              Generating response
              <span className="inline-block w-2 animate-pulse align-bottom" aria-hidden="true">▌</span>
            </span>
          </div>
        </div>
      </div>
    </div>
  );
}