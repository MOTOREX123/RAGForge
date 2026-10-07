import { useRef, useState, useEffect } from "react";
import { ArrowUp, Paperclip, ChevronDown, X, Loader2 } from "lucide-react";
import { useConversation } from "../../context/ConversationContext";

export function ChatInput({ onSend, disabled, onStop, isGenerating, model }) {
  const [value, setValue] = useState("");
  const [showModelMenu, setShowModelMenu] = useState(false);
  const textareaRef = useRef(null);
  const menuRef = useRef(null);
  const { setChatInputRef } = useConversation();

  // Register textarea ref with context for external focus
  useEffect(() => {
    setChatInputRef(textareaRef.current);
  }, [setChatInputRef]);

  // Auto-resize textarea
  useEffect(() => {
    if (textareaRef.current) {
      textareaRef.current.style.height = "auto";
      textareaRef.current.style.height = `${Math.min(textareaRef.current.scrollHeight, 160)}px`;
    }
  }, [value]);

  // Close menu on outside click
  useEffect(() => {
    const handleClickOutside = (event) => {
      if (menuRef.current && !menuRef.current.contains(event.target)) {
        setShowModelMenu(false);
      }
    };
    document.addEventListener("mousedown", handleClickOutside);
    return () => document.removeEventListener("mousedown", handleClickOutside);
  }, []);

  const submit = () => {
    const trimmed = value.trim();
    if (!trimmed || disabled) return;
    onSend(trimmed);
    setValue("");
    if (textareaRef.current) {
      textareaRef.current.style.height = "auto";
      // Focus after sending to allow immediate follow-up
      textareaRef.current.focus();
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
  };

  return (
    <div className="px-4 py-3 bg-surface/50">
      <div className="relative">
        <div className="flex items-end gap-2 rounded-lg border border-line bg-surface px-3 py-2 focus-within:border-purple/50">
          {/* Attachment button */}
          <button
            type="button"
            disabled={disabled || isGenerating}
            className="flex h-8 w-8 shrink-0 items-center justify-center rounded-md text-ink-dim transition-colors hover:bg-raised hover:text-ink disabled:opacity-30"
            aria-label="Attach file"
          >
            <Paperclip size={17} strokeWidth={2} />
          </button>

          {/* Textarea */}
          <textarea
            ref={textareaRef}
            value={value}
            onChange={handleChange}
            onKeyDown={handleKeyDown}
            disabled={disabled || isGenerating}
            rows={1}
            placeholder={isGenerating ? "Generating response…" : "Ask RAGForge about your documents…"}
            className="max-h-[160px] flex-1 resize-none bg-transparent text-[13px] leading-relaxed text-ink placeholder:text-ink-dim focus:outline-none"
          />

          {/* Model selector */}
          <div className="relative" ref={menuRef}>
            <button
              type="button"
              onClick={() => setShowModelMenu(!showModelMenu)}
              disabled={disabled || isGenerating}
              className="flex h-8 shrink-0 items-center gap-1.5 rounded-md px-2 py-1 text-[11px] font-medium text-ink-dim transition-colors hover:bg-raised hover:text-ink disabled:opacity-30"
              aria-label="Select model"
              aria-expanded={showModelMenu}
            >
              <span className="font-mono hidden sm:inline">{model}</span>
              <ChevronDown size={11} />
            </button>

            {showModelMenu && (
              <div className="absolute bottom-full right-0 mb-2 z-10 rounded-lg border border-line bg-surface shadow-lg min-w-[180px] overflow-hidden">
                <button
                  type="button"
                  className="flex w-full items-center gap-2 px-3 py-2 text-sm text-left transition-colors bg-purple-bg text-purple"
                >
                  <div className="flex flex-col">
                    <span className="font-medium">Ollama</span>
                    <span className="text-[10px] text-ink-muted">{model}</span>
                  </div>
                  <span className="ml-auto text-[10px] text-ink-muted">Local · Primary</span>
                </button>
                <button
                  type="button"
                  className="flex w-full items-center gap-2 px-3 py-2 text-sm text-left transition-colors text-ink hover:bg-raised"
                >
                  <div className="flex flex-col">
                    <span className="font-medium">OpenRouter</span>
                    <span className="text-[10px] text-ink-muted">Nemotron 3 Ultra</span>
                  </div>
                  <span className="ml-auto text-[10px] text-ink-muted">Cloud · Fallback</span>
                </button>
              </div>
            )}
          </div>

          {/* Send / Stop button */}
          <button
            type="button"
            onClick={isGenerating ? onStop : submit}
            disabled={disabled || (!value.trim() && !isGenerating)}
            aria-label={isGenerating ? "Stop generation" : "Send message"}
            className={`flex h-8 w-8 shrink-0 items-center justify-center rounded-md transition-opacity ${
              isGenerating
                ? "bg-red text-white hover:opacity-90"
                : "bg-purple text-white hover:opacity-90 disabled:opacity-30"
            }`}
          >
            {isGenerating ? (
              <X size={15} strokeWidth={2.5} />
            ) : (
              <ArrowUp size={15} strokeWidth={2.5} />
            )}
          </button>
        </div>

        {/* Hint text */}
        <p className="mt-1.5 text-center text-[10px] text-ink-muted">
          {isGenerating ? "Generating… Press Stop to cancel" : "Enter to send · Shift+Enter for new line"}
        </p>
      </div>
    </div>
  );
}