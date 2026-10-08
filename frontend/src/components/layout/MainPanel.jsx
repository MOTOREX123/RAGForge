import { useState, useEffect } from "react";
import { Menu, ChevronLeft, ChevronRight, ChevronDown, MessageSquare, FolderOpen, BarChart2, Settings, Database, Wifi, Server } from "lucide-react";
import { MessageList } from "../chat/MessageList";
import { ChatInput } from "../chat/ChatInput";
import { RAGPipelineStatus } from "../chat/RAGPipelineStatus";
import { DocumentsView } from "./DocumentsView";
import { SettingsView } from "./SettingsView";
import { AnalyticsView } from "./AnalyticsView";
import { useConversation } from "../../context/ConversationContext";
import { fetchHealth } from "../../api/chat";

export function MainPanel({ onOpenSidebar }) {
  const {
    messages,
    isLoading,
    pipelineStatus,
    sendMessage,
    regenerate,
    retry,
    stopGeneration,
    activeConversation,
    activeNav,
    setActiveNav,
    clearConversation,
    focusChatInput,
  } = useConversation();

  const [providerInfo, setProviderInfo] = useState({
    ollama: "checking",
    openrouter: "checking",
    faiss: "checking",
    model: null,
  });

  // The active model comes from real backend responses (response.model),
  // not a hardcoded default. Null until the backend answers a message.
  const activeModel =
    [...messages].reverse().find((m) => m.role === "assistant" && m.model)?.model ||
    providerInfo.model;

  // Keyboard shortcut: Ctrl/Cmd + K to focus chat input
  useEffect(() => {
    const handleKeyDown = (event) => {
      if ((event.metaKey || event.ctrlKey) && event.key === "k") {
        event.preventDefault();
        focusChatInput();
      }
      if (event.key === "Escape") {
        // Close any open modals/drawers - handled by individual components
      }
    };
    document.addEventListener("keydown", handleKeyDown);
    return () => document.removeEventListener("keydown", handleKeyDown);
  }, [focusChatInput]);

  useEffect(() => {
    const fetchProviderInfo = async () => {
      try {
        const health = await fetchHealth();
        setProviderInfo((prev) => ({
          ...prev,
          ollama: health.ollama_reachable ? "connected" : "disconnected",
          openrouter: health.openrouter_reachable ? "connected" : "disconnected",
          faiss: health.faiss_ready ? "connected" : "disconnected",
          // /api/health exposes no model field; the displayed model is
          // taken from /api/chat responses instead of a hardcoded guess.
          model: health.default_model || null,
        }));
      } catch {
        setProviderInfo((prev) => ({
          ...prev,
          ollama: "disconnected",
          openrouter: "disconnected",
          faiss: "disconnected",
        }));
      }
    };
    fetchProviderInfo();
    const interval = setInterval(fetchProviderInfo, 30000);
    return () => clearInterval(interval);
  }, []);

  const handleSend = (text) => {
    sendMessage(text);
  };

  const handleRegenerate = () => {
    regenerate();
  };

  const handleStop = () => {
    stopGeneration();
  };

  const handleClearChat = () => {
    clearConversation();
  };

  const renderView = () => {
    switch (activeNav) {
      case "documents":
        return <DocumentsView />;
      case "analytics":
        return <AnalyticsView />;
      case "settings":
        return <SettingsView />;
      case "chats":
      default:
        return (
          <div className="flex flex-1 flex-col min-w-0 bg-bg">
            {/* Compact Header */}
            <div className="flex items-center justify-between border-b border-line px-4 py-2.5 bg-surface/50">
              <div className="flex items-center gap-2.5">
                <img
                  src="/assets/ragforge-logo.png"
                  alt="RAGForge"
                  className="w-8 h-8"
                />
                <span className="font-display text-sm font-semibold text-ink">RAGForge</span>
                {activeConversation && (
                  <span className="text-[11px] text-ink-muted px-2 py-0.5 rounded bg-raised">
                    {activeConversation.title}
                  </span>
                )}
              </div>
              <div className="flex items-center gap-2">
                {/* Model Selector */}
                <div className="relative">
                  <button
                    type="button"
                    className="flex items-center gap-1.5 rounded-lg px-2.5 py-1.5 text-[11px] font-medium text-ink-dim transition-colors hover:bg-raised hover:text-ink"
                    aria-label="Select model"
                  >
                    <span className="font-mono">{activeModel || "No active model"}</span>
                    <ChevronDown size={12} />
                  </button>
                </div>
                {/* Status */}
                <div className="flex items-center gap-1.5 text-[11px]">
                  <span
                    className={`w-1.5 h-1.5 rounded-full ${
                      isLoading ? "bg-yellow animate-pulse" : "bg-green"
                    }`}
                  />
                  <span className={isLoading ? "text-yellow" : "text-green"}>
                    {isLoading ? "Generating" : "Ready"}
                  </span>
                </div>
              </div>
            </div>

            {/* Chat Header (Empty State Area) */}
            <div className="px-4 py-5 border-b border-line">
              <div className="w-full">
                <h1 className="font-display text-xl font-semibold text-ink">
                  Ask your knowledge base
                </h1>
                <p className="mt-1 text-sm text-ink-muted max-w-2xl">
                  Search across indexed documents with grounded answers and traceable context.
                </p>
                <div className="mt-4 flex flex-wrap gap-2">
                  {[
                    "Summarize the deployment runbook",
                    "What changed in the v2 API?",
                    "Find the retry policy for failed jobs",
                    "Explain the rollback sequence",
                  ].map((prompt) => (
                    <button
                      key={prompt}
                      type="button"
                      onClick={() => handleSend(prompt)}
                      disabled={isLoading}
                      className="inline-flex items-center gap-1.5 rounded-lg border border-line bg-surface px-3 py-1.5 text-sm text-ink-dim transition-colors hover:border-purple/40 hover:bg-raised hover:text-ink disabled:opacity-50"
                    >
                      <MessageSquare size={14} />
                      {prompt}
                    </button>
                  ))}
                </div>
              </div>
            </div>

            {/* Messages */}
            <MessageList
              messages={messages}
              isLoading={isLoading}
              onRegenerate={handleRegenerate}
              onRetry={retry}
              onSuggestion={handleSend}
            />

            {/* Pipeline status bar (visible during generation) */}
            {pipelineStatus && (
              <div className="border-t border-line px-4 py-2 bg-surface/50">
                <RAGPipelineStatus status={pipelineStatus} className="w-full" />
              </div>
            )}

            {/* Composer */}
            <div className="border-t border-line bg-surface/50">
              <ChatInput
                onSend={handleSend}
                disabled={isLoading}
                onStop={handleStop}
                isGenerating={isLoading}
                model={activeModel || "No active model"}
              />
            </div>
          </div>
        );
    }
  };

  return (
    <div className="flex h-full flex-1 flex-col bg-bg">
      {/* Mobile header */}
      <div className="flex items-center justify-between border-b border-line px-4 py-2.5 lg:hidden bg-surface/50">
        <button
          type="button"
          onClick={onOpenSidebar}
          aria-label="Open sidebar"
          className="text-ink-dim"
        >
          <Menu size={20} />
        </button>
        <div className="flex items-center gap-2">
          <img
            src="/assets/ragforge-logo.png"
            alt="RAGForge"
            className="w-8 h-8"
          />
          <span className="font-display text-sm font-semibold text-ink">
            RAGForge
          </span>
        </div>
        <button
          type="button"
          aria-label="Open sources"
          className="text-ink-dim"
        >
          <ChevronRight size={20} />
        </button>
      </div>

      {/* Desktop layout: Chat area - full width, Sources handled in AppLayout */}
      <div className="flex-1 flex flex-col min-w-0">
        {renderView()}
      </div>
    </div>
  );
}