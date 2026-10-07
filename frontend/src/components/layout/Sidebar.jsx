import { useState, useEffect } from "react";
import {
  SquarePen,
  MessageSquare,
  FolderOpen,
  Settings,
  ChevronDown,
  ChevronUp,
  Server,
  Wifi,
  WifiOff,
  User,
  X,
  Trash2,
  Edit2,
  MoreHorizontal,
  Database,
  ExternalLink,
} from "lucide-react";
import { useConversation } from "../../context/ConversationContext";
import { fetchHealth } from "../../api/chat";
import { useToast } from "../../context/ToastContext";

const NAV_ITEMS = [
  { id: "documents", label: "Documents", icon: FolderOpen },
  { id: "settings", label: "Settings", icon: Settings },
];

export function Sidebar({ isOpen, onClose }) {
  const {
    clearConversation,
    conversations,
    activeNav,
    setActiveNav,
    createConversation,
    switchConversation,
    deleteConversation,
    updateConversationTitle,
    focusChatInput,
  } = useConversation();
  const { addToast } = useToast();
  const [expandedSections, setExpandedSections] = useState({
    today: true,
    yesterday: true,
    older: false,
  });
  const [providerStatus, setProviderStatus] = useState({
    ollama: "checking",
    openrouter: "checking",
    faiss: "checking",
  });
  const [showChatMenu, setShowChatMenu] = useState(null);
  const [docCount, setDocCount] = useState(0);

  useEffect(() => {
    const checkHealth = async () => {
      try {
        const health = await fetchHealth();
        setProviderStatus({
          ollama: health.ollama_reachable ? "connected" : "disconnected",
          openrouter: health.openrouter_reachable ? "connected" : "disconnected",
          faiss: health.faiss_ready ? "connected" : "disconnected",
        });
        if (health.document_count !== undefined) {
          setDocCount(health.document_count);
        }
      } catch {
        setProviderStatus({
          ollama: "disconnected",
          openrouter: "disconnected",
          faiss: "disconnected",
        });
      }
    };
    checkHealth();
    const interval = setInterval(checkHealth, 30000);
    return () => clearInterval(interval);
  }, []);

  const toggleSection = (sectionId) => {
    setExpandedSections((prev) => ({ ...prev, [sectionId]: !prev[sectionId] }));
  };

  const handleNewChat = () => {
    createConversation();
    focusChatInput();
    onClose?.();
  };

  const handleChatClick = (chatId) => {
    switchConversation(chatId);
    onClose?.();
  };

  const handleChatMenu = (e, chatId) => {
    e.stopPropagation();
    setShowChatMenu(showChatMenu === chatId ? null : chatId);
  };

  const handleRenameChat = (chatId) => {
    const newTitle = prompt("Rename chat:");
    if (newTitle && newTitle.trim()) {
      updateConversationTitle(chatId, newTitle.trim());
      addToast("Conversation renamed", "success");
    }
    setShowChatMenu(null);
  };

  const handleDeleteChat = (chatId) => {
    if (confirm("Delete this chat? This action cannot be undone.")) {
      deleteConversation(chatId);
      addToast("Conversation deleted", "success");
    }
    setShowChatMenu(null);
  };

  const formatTime = (timestamp) => {
    const date = new Date(timestamp);
    const now = new Date();
    const diffMs = now - date;
    const diffMins = Math.floor(diffMs / 60000);
    const diffHours = Math.floor(diffMs / 3600000);
    const diffDays = Math.floor(diffMs / 86400000);

    if (diffMins < 1) return "Just now";
    if (diffMins < 60) return `${diffMins}m ago`;
    if (diffHours < 24) return `${diffHours}h ago`;
    if (diffDays < 7) return `${diffDays}d ago`;
    return date.toLocaleDateString([], { month: "short", day: "numeric" });
  };

  const groupConversations = (convs) => {
    const now = new Date();
    const today = new Date(now.getFullYear(), now.getMonth(), now.getDate());
    const yesterday = new Date(today);
    yesterday.setDate(yesterday.getDate() - 1);

    const groups = { today: [], yesterday: [], older: [] };

    convs.forEach((conv) => {
      const convDate = new Date(conv.updatedAt || conv.createdAt);
      if (convDate >= today) {
        groups.today.push(conv);
      } else if (convDate >= yesterday) {
        groups.yesterday.push(conv);
      } else {
        groups.older.push(conv);
      }
    });

    return groups;
  };

  const groupedConversations = groupConversations(conversations);

  const StatusDot = ({ status }) => {
    const colors = {
      connected: "bg-green",
      disconnected: "bg-red",
      checking: "bg-yellow-dim animate-pulse",
    };
    return <span className={`w-1.5 h-1.5 rounded-full ${colors[status]}`} />;
  };

  const NavIcon = ({ icon: Icon, active }) => (
    <Icon size={16} strokeWidth={active ? 2.5 : 2} className={active ? "text-purple" : "text-ink-dim"} />
  );

  return (
    <aside
      className={`flex h-full w-55 shrink-0 flex-col border-r border-line bg-surface transition-transform duration-200 ease-out ${
        isOpen ? "translate-x-0" : "-translate-x-full md:translate-x-0"
      }`}
    >
      {/* Top: Logo + New Chat */}
      <div className="px-4 py-4 border-b border-line">
        <div className="flex items-center gap-2.5 mb-4">
          <img
            src="/assets/ragforge-logo.png"
            alt="RAGForge"
            className="w-12 h-12"
          />
          <div>
            <span className="font-display text-lg font-semibold text-ink">RAGForge</span>
            <p className="text-[11px] text-ink-muted">RAG assistant workspace</p>
          </div>
        </div>
        <button
          type="button"
          onClick={handleNewChat}
          className="flex w-full items-center justify-center gap-2 rounded-lg bg-purple px-3 py-2.5 text-sm font-medium text-white transition-colors hover:bg-purple-dim hover:shadow-[0_0_12px_rgba(124,92,255,0.4)]"
        >
          <SquarePen size={15} />
          New Chat
        </button>
      </div>

      {/* Conversations */}
      <div className="flex-1 overflow-y-auto px-2 py-3 space-y-3 border-b border-line">
        <p className="px-3 mb-2 text-[10px] font-medium uppercase tracking-wider text-ink-muted">
          Conversations
        </p>
        {Object.entries(groupedConversations).map(([sectionId, chats]) => (
          <div key={sectionId} className={chats.length > 0 ? "" : "hidden"}>
            <button
              type="button"
              onClick={() => toggleSection(sectionId)}
              className="flex w-full items-center justify-between px-3 py-1.5 text-[10px] font-medium uppercase tracking-wider text-ink-muted hover:text-ink"
            >
              <span>{sectionId.charAt(0).toUpperCase() + sectionId.slice(1)}</span>
              <span className="flex items-center gap-1">
                {chats.length}
                {expandedSections[sectionId] ? (
                  <ChevronUp size={11} />
                ) : (
                  <ChevronDown size={11} />
                )}
              </span>
            </button>
            {expandedSections[sectionId] && (
              <div className="space-y-1 mt-1">
                {chats.map((chat) => (
                  <div key={chat.id} className="relative group">
                    <button
                      type="button"
                      onClick={() => handleChatClick(chat.id)}
                      className="flex w-full items-center justify-between gap-2 rounded-lg px-2.5 py-2 text-sm text-ink-dim transition-colors hover:bg-raised hover:text-ink"
                    >
                      <span className="truncate">{chat.title}</span>
                      <span className="shrink-0 text-[10px] text-ink-muted">
                        {formatTime(chat.updatedAt || chat.createdAt)}
                      </span>
                    </button>
                    <button
                      type="button"
                      onClick={(e) => handleChatMenu(e, chat.id)}
                      className="absolute right-1 top-1/2 -translate-y-1/2 rounded p-1 text-ink-dim opacity-0 transition-opacity hover:text-ink group-hover:opacity-100"
                      aria-label="Chat options"
                    >
                      <MoreHorizontal size={13} />
                    </button>
                    {showChatMenu === chat.id && (
                      <div className="absolute right-0 top-full mt-1 z-10 rounded-lg border border-line bg-raised py-1 shadow-lg min-w-[140px]">
                        <button
                          type="button"
                          onClick={() => handleRenameChat(chat.id)}
                          className="flex w-full items-center gap-2 px-3 py-1.5 text-sm text-ink hover:bg-surface"
                        >
                          <Edit2 size={13} />
                          Rename
                        </button>
                        <button
                          type="button"
                          onClick={() => handleDeleteChat(chat.id)}
                          className="flex w-full items-center gap-2 px-3 py-1.5 text-sm text-red hover:bg-red-dim"
                        >
                          <Trash2 size={13} />
                          Delete
                        </button>
                      </div>
                    )}
                  </div>
                ))}
              </div>
            )}
          </div>
        ))}

        {conversations.length === 0 && (
          <p className="px-3 py-4 text-center text-sm text-ink-muted">
            No conversations yet
          </p>
        )}
      </div>

      {/* Navigation */}
      <nav className="px-3 py-3 space-y-1 border-b border-line">
        {NAV_ITEMS.map(({ id, label, icon: Icon }) => (
          <button
            key={id}
            type="button"
            onClick={() => {
              setActiveNav(id);
              onClose?.();
            }}
            className={`flex w-full items-center gap-3 rounded-lg px-3 py-2.5 text-sm font-medium transition-colors ${
              activeNav === id
                ? "bg-purple-bg text-purple"
                : "text-ink-dim hover:bg-raised/50 hover:text-ink"
            }`}
          >
            <NavIcon icon={Icon} active={activeNav === id} />
            {label}
          </button>
        ))}
      </nav>

      {/* Bottom: System Status */}
      <div className="border-t border-line px-4 py-4 space-y-3">
        <p className="text-[10px] font-medium uppercase tracking-wider text-ink-muted">
          System Status
        </p>
        <div className="space-y-2">
          <div className="flex items-center gap-2">
            <Server size={13} className="text-ink-muted shrink-0" />
            <div className="flex-1 min-w-0">
              <p className="text-sm text-ink">Ollama</p>
              <p className="text-[11px] text-ink-muted">Local</p>
            </div>
            <StatusDot status={providerStatus.ollama} />
          </div>
          <div className="flex items-center gap-2">
            <Wifi size={13} className="text-ink-muted shrink-0" />
            <div className="flex-1 min-w-0">
              <p className="text-sm text-ink">OpenRouter</p>
              <p className="text-[11px] text-ink-muted">Fallback</p>
            </div>
            <StatusDot status={providerStatus.openrouter} />
          </div>
          <div className="flex items-center gap-2">
            <Database size={13} className="text-ink-muted shrink-0" />
            <div className="flex-1 min-w-0">
              <p className="text-sm text-ink">FAISS</p>
              <p className="text-[11px] text-ink-muted">Vector DB</p>
            </div>
            <StatusDot status={providerStatus.faiss} />
          </div>
        </div>
        <div className="pt-2 border-t border-line">
          <p className="text-[11px] text-ink-muted flex items-center gap-1.5">
            <ExternalLink size={12} />
            {docCount} documents indexed
          </p>
        </div>
        <div className="flex items-center gap-2 text-[11px]">
          <span className={`w-1.5 h-1.5 rounded-full ${providerStatus.ollama === "connected" || providerStatus.openrouter === "connected" ? "bg-green" : "bg-red"}`} />
          <span className={providerStatus.ollama === "connected" || providerStatus.openrouter === "connected" ? "text-green" : "text-red"}>
            {providerStatus.ollama === "connected" || providerStatus.openrouter === "connected" ? "Backend reachable" : "Backend unreachable"}
          </span>
        </div>
      </div>
    </aside>
  );
}