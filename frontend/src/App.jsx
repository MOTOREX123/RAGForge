import { useState } from "react";
import { ConversationProvider } from "./context/ConversationContext";
import { Sidebar } from "./components/layout/Sidebar";
import { MainPanel } from "./components/layout/MainPanel";

export default function App() {
  const [isSidebarOpen, setIsSidebarOpen] = useState(false);

  return (
    <ConversationProvider>
      <div className="flex h-screen w-screen overflow-hidden">
        {/* Desktop: sidebar sits inline. Mobile: it's an overlay drawer. */}
        <div className="hidden md:block">
          <Sidebar />
        </div>

        {isSidebarOpen && (
          <div className="fixed inset-0 z-20 flex md:hidden">
            <Sidebar />
            <button
              type="button"
              aria-label="Close sidebar"
              onClick={() => setIsSidebarOpen(false)}
              className="flex-1 bg-black/50"
            />
          </div>
        )}

        <MainPanel onOpenSidebar={() => setIsSidebarOpen(true)} />
      </div>
    </ConversationProvider>
  );
}
