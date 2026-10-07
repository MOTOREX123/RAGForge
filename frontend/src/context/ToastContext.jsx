import { createContext, useContext, useState, useCallback, useMemo } from "react";
import { X, CheckCircle, AlertCircle, Info } from "lucide-react";

const ToastContext = createContext(null);

const TOAST_TYPES = {
  success: { icon: CheckCircle, color: "text-green", bg: "bg-green-dim/20 border-green/30" },
  error: { icon: AlertCircle, color: "text-red", bg: "bg-red-dim/20 border-red/30" },
  info: { icon: Info, color: "text-blue", bg: "bg-blue-dim/20 border-blue/30" },
  default: { icon: Info, color: "text-ink", bg: "bg-raised border-line" },
};

let toastId = 0;

export function ToastProvider({ children }) {
  const [toasts, setToasts] = useState([]);

  const addToast = useCallback((message, type = "default", duration = 3000) => {
    const id = ++toastId;
    const toast = { id, message, type };
    setToasts((prev) => [...prev, toast]);
    if (duration > 0) {
      setTimeout(() => {
        setToasts((prev) => prev.filter((t) => t.id !== id));
      }, duration);
    }
    return id;
  }, []);

  const removeToast = useCallback((id) => {
    setToasts((prev) => prev.filter((t) => t.id !== id));
  }, []);

  const value = useMemo(() => ({ toasts, addToast, removeToast }), [toasts, addToast, removeToast]);

  return (
    <ToastContext.Provider value={value}>
      {children}
      <ToastContainer toasts={toasts} onRemove={removeToast} />
    </ToastContext.Provider>
  );
}

export function useToast() {
  const ctx = useContext(ToastContext);
  if (!ctx) {
    throw new Error("useToast must be used within a ToastProvider");
  }
  return ctx;
}

function ToastContainer({ toasts, onRemove }) {
  return (
    <div className="fixed bottom-4 right-4 z-50 flex flex-col gap-2 pointer-events-none">
      {toasts.map((toast) => (
        <ToastItem key={toast.id} toast={toast} onRemove={onRemove} />
      ))}
    </div>
  );
}

function ToastItem({ toast, onRemove }) {
  const config = TOAST_TYPES[toast.type] || TOAST_TYPES.default;
  const Icon = config.icon;

  return (
    <div
      className={`pointer-events-auto flex items-center gap-2.5 rounded-lg border px-3 py-2.5 text-sm ${config.bg} ${config.color} shadow-lg animate-slide-in`}
      role="alert"
      aria-live="polite"
    >
      <Icon size={16} strokeWidth={2} className="shrink-0" />
      <span className="max-w-[300px]">{toast.message}</span>
      <button
        type="button"
        onClick={() => onRemove(toast.id)}
        className="shrink-0 ml-2 rounded p-0.5 hover:bg-black/10 transition-colors"
        aria-label="Dismiss"
      >
        <X size={14} strokeWidth={2} />
      </button>
    </div>
  );
}