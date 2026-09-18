import { useRef, useState } from "react";
import { ArrowUp } from "lucide-react";

export function ChatInput({ onSend, disabled }) {
  const [value, setValue] = useState("");
  const textareaRef = useRef(null);

  const submit = () => {
    const trimmed = value.trim();
    if (!trimmed || disabled) return;
    onSend(trimmed);
    setValue("");
    if (textareaRef.current) {
      textareaRef.current.style.height = "auto";
    }
  };

  const handleKeyDown = (event) => {
    if (event.key === "Enter" && !event.shiftKey) {
      event.preventDefault();
      submit();
    }
  };

  const handleChange = (event) => {
    setValue(event.target.value);
    const el = textareaRef.current;
    if (el) {
      el.style.height = "auto";
      el.style.height = `${Math.min(el.scrollHeight, 200)}px`;
    }
  };

  return (
    <div className="mx-auto w-full max-w-prose px-4 pb-5">
      <div className="flex items-end gap-2 rounded-lg border border-line bg-surface px-3 py-2.5 focus-within:border-brass/50">
        <textarea
          ref={textareaRef}
          value={value}
          onChange={handleChange}
          onKeyDown={handleKeyDown}
          disabled={disabled}
          rows={1}
          placeholder="Ask about your documents, or anything else…"
          className="max-h-[200px] flex-1 resize-none bg-transparent text-[15px] leading-relaxed text-ink placeholder:text-ink-dim focus:outline-none"
        />
        <button
          type="button"
          onClick={submit}
          disabled={disabled || !value.trim()}
          aria-label="Send message"
          className="flex h-8 w-8 shrink-0 items-center justify-center rounded-md bg-brass text-bg transition-opacity disabled:opacity-30 hover:opacity-90"
        >
          <ArrowUp size={16} strokeWidth={2.5} />
        </button>
      </div>
      <p className="mt-1.5 text-center text-xs text-ink-dim">
        Enter to send · Shift+Enter for a new line
      </p>
    </div>
  );
}
