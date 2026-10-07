import { useRef, useState } from "react";
import { Upload, Loader2, CheckCircle, X, AlertCircle } from "lucide-react";

export function UploadButton({ onUpload, disabled }) {
  const inputRef = useRef(null);
  const [isUploading, setIsUploading] = useState(false);
  const [selectedFile, setSelectedFile] = useState(null);
  const [uploadProgress, setUploadProgress] = useState(0);
  const [error, setError] = useState(null);

  const handleChange = async (event) => {
    const file = event.target.files?.[0];
    event.target.value = ""; // allow re-selecting the same file later
    if (!file) return;

    setSelectedFile(file);
    setError(null);
    setUploadProgress(0);

    // Simulate progress for better UX
    const progressInterval = setInterval(() => {
      setUploadProgress((prev) => Math.min(prev + 10, 90));
    }, 200);

    setIsUploading(true);
    try {
      await onUpload(file);
      clearInterval(progressInterval);
      setUploadProgress(100);
      setSelectedFile(null);
      // Keep success state briefly
      setTimeout(() => {
        setIsUploading(false);
        setUploadProgress(0);
      }, 1000);
    } catch (err) {
      clearInterval(progressInterval);
      setError(err.message || "Upload failed");
      setIsUploading(false);
      setUploadProgress(0);
    }
  };

  const handleRetry = () => {
    if (selectedFile) {
      setError(null);
      handleChange({ target: { files: [selectedFile] } });
    }
  };

  const handleDismiss = () => {
    setSelectedFile(null);
    setError(null);
  };

  const formatFileSize = (bytes) => {
    if (bytes < 1024) return `${bytes} B`;
    if (bytes < 1024 * 1024) return `${(bytes / 1024).toFixed(1)} KB`;
    return `${(bytes / (1024 * 1024)).toFixed(1)} MB`;
  };

  if (selectedFile || isUploading) {
    return (
      <div className="w-full space-y-2">
        <div className="flex items-center gap-2 rounded-lg border border-line bg-surface p-2.5">
          <div className="flex h-8 w-8 shrink-0 items-center justify-center rounded-lg bg-purple-bg text-purple">
            <Upload size={14} />
          </div>
          <div className="flex-1 min-w-0">
            <p className="truncate text-sm font-medium text-ink">{selectedFile?.name || "Document"}</p>
            <p className="text-[10px] text-ink-muted">{selectedFile ? formatFileSize(selectedFile.size) : ""}</p>
          </div>
          <div className="flex items-center gap-2">
            {isUploading && (
              <>
                <div className="w-24 h-1.5 bg-raised rounded-full overflow-hidden">
                  <div
                    className="h-full bg-purple transition-all duration-300"
                    style={{ width: `${uploadProgress}%` }}
                  />
                </div>
                <Loader2 size={14} className="animate-spin text-purple" />
              </>
            )}
            {!isUploading && !error && <CheckCircle size={14} className="text-green" />}
            {error && <AlertCircle size={14} className="text-red" />}
            <button
              type="button"
              onClick={handleDismiss}
              className="shrink-0 rounded p-1 text-ink-dim hover:text-ink"
              aria-label="Remove file"
            >
              <X size={14} />
            </button>
          </div>
        </div>
        {error && (
          <div className="flex items-center gap-2 text-sm text-red bg-red-dim/20 border border-red/30 rounded p-2">
            <AlertCircle size={13} />
            <span className="flex-1">{error}</span>
            <button
              type="button"
              onClick={handleRetry}
              className="text-sm font-medium text-red hover:underline"
            >
              Retry
            </button>
          </div>
        )}
      </div>
    );
  }

  return (
    <>
      <input
        ref={inputRef}
        type="file"
        accept=".pdf,.docx"
        className="hidden"
        onChange={handleChange}
      />
      <button
        type="button"
        onClick={() => inputRef.current?.click()}
        disabled={disabled || isUploading}
        className="flex items-center justify-center gap-1.5 rounded-lg border border-dashed border-line bg-surface/50 px-3 py-2 text-xs text-ink-dim transition-colors hover:border-purple/40 hover:bg-purple-bg hover:text-purple disabled:opacity-50"
      >
        <Upload size={13} />
        Upload document
      </button>
    </>
  );
}