import { SquarePen } from "lucide-react";
import { DocumentList } from "../documents/DocumentList";
import { useConversation } from "../../context/ConversationContext";

export function Sidebar() {
  const { clearConversation } = useConversation();

  return (
    <aside className="flex h-full w-64 shrink-0 flex-col border-r border-line bg-surface">
      <div className="px-4 py-5">
        <h1 className="font-display text-lg leading-tight text-ink">
          MultiDocument
          <br />
          RAG
        </h1>
      </div>

      <div className="px-3">
        <button
          type="button"
          onClick={clearConversation}
          className="flex w-full items-center gap-2 rounded border border-line px-3 py-2 text-sm text-ink transition-colors hover:border-brass/40 hover:bg-raised"
        >
          <SquarePen size={14} />
          New chat
        </button>
      </div>

      <div className="mt-6 flex-1 overflow-y-auto px-1">
        <DocumentList />
      </div>

      <div className="border-t border-line px-4 py-3">
        <p className="text-[11px] text-ink-dim">
          Local docs via Ollama · Gemma 3 4B. Web answers via Gemini
          search grounding.
        </p>
      </div>
    </aside>
  );
}
