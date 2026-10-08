import { ConversationProvider } from "./context/ConversationContext";
import { ToastProvider } from "./context/ToastContext";
import { Sidebar } from "./components/layout/Sidebar";
import { MainPanel } from "./components/layout/MainPanel";
import { SourcesPanel } from "./components/layout/SourcesPanel";
import { useConversation } from "./context/ConversationContext";
import { useEffect, useState } from "react";

function AppLayout() {
  const { lastCitations, setLastCitations, sourcesOpen, setSourcesOpen, messages, sidebarOpen, setSidebarOpen } = useConversation();
  const [mobileSourcesOpen, setMobileSourcesOpen] = useState(false);

  // Update lastCitations when a new assistant message arrives
  useEffect(() => {
    const lastAssistantMessage = [...messages].reverse().find((m) => m.role === "assistant");
    if (lastAssistantMessage?.citations?.length) {
      setLastCitations(lastAssistantMessage.citations);
    }
  }, [messages, setLastCitations]);

  // Close sidebar on mobile when navigation item is clicked
  const handleSidebarClose = () => {
    setSidebarOpen(false);
  };

  // Close mobile sources when clicking outside
  const handleSourcesClose = () => {
    setMobileSourcesOpen(false);
    setSourcesOpen(false);
  };

  return (
    <div className="flex h-screen w-screen overflow-hidden bg-bg">
      {/* Sidebar - becomes drawer on mobile */}
      <Sidebar isOpen={sidebarOpen} onClose={handleSidebarClose} />

      {/* Main content area */}
      <div className="flex-1 flex flex-col min-w-0">
        <MainPanel onOpenSidebar={() => setSidebarOpen(true)} />

        {/* Mobile Sources Button */}
        <div className="lg:hidden fixed bottom-4 right-4 z-40" aria-label="Open sources">
          {lastCitations.length > 0 && (
            <button
              type="button"
              onClick={() => setMobileSourcesOpen(true)}
              className="flex items-center gap-1.5 rounded-lg bg-purple px-3 py-2 text-sm font-medium text-white shadow-lg"
            >
              <span>Sources</span>
              <span className="flex h-5 w-5 items-center justify-center rounded-full bg-white/20 text-[10px] font-mono">
                {lastCitations.length}
              </span>
            </button>
          )}
        </div>
      </div>

      {/* Mobile Sources Panel - Bottom Sheet */}
      <SourcesPanel
        citations={lastCitations}
        isOpen={mobileSourcesOpen || (lastCitations.length > 0 && sourcesOpen)}
        onClose={handleSourcesClose}
      />
    </div>
  );
}

export default function App() {
  return (
    <ToastProvider>
      <ConversationProvider>
        <AppLayout />
      </ConversationProvider>
    </ToastProvider>
  );
}