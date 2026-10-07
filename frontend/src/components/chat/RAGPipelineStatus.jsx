import { Cpu, Loader2 } from "lucide-react";
import { useEffect, useRef } from "react";

export function RAGPipelineStatus({ status, className = "" }) {
  if (!status) return null;

  // Only "generating" status is used now (backend doesn't expose pipeline stages)
  const isGenerating = status === "generating";
  const previousStatusRef = useRef(null);

  // Announce status changes to screen readers
  useEffect(() => {
    if (status !== previousStatusRef.current) {
      previousStatusRef.current = status;
      // The aria-live region will announce the change
    }
  }, [status]);

  return (
    <div className={`flex items-center gap-2 ${className}`} aria-live="polite" aria-atomic="true">
      <div className="flex items-center gap-1.5 text-[10px] transition-colors">
        <div className="flex items-center gap-1.5">
          <span className="flex h-4 w-4 items-center justify-center rounded-full bg-purple-bg text-purple">
            {isGenerating ? (
              <Loader2 size={8} className="animate-spin" />
            ) : (
              <Cpu size={8} strokeWidth={2} />
            )}
          </span>
          <span className="font-mono text-purple">
            Generating answer…
          </span>
        </div>
      </div>
    </div>
  );
}