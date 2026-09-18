import { useRef, useState } from "react";
import { Upload } from "lucide-react";

export function UploadButton({ onUpload, disabled }) {
  const inputRef = useRef(null);
  const [isUploading, setIsUploading] = useState(false);

  const handleChange = async (event) => {
    const file = event.target.files?.[0];
    event.target.value = ""; // allow re-selecting the same file later
    if (!file) return;

    setIsUploading(true);
    try {
      await onUpload(file);
    } finally {
      setIsUploading(false);
    }
  };

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
        className="flex w-full items-center justify-center gap-2 rounded border border-dashed border-line px-3 py-2 text-xs text-ink-dim transition-colors hover:border-brass/40 hover:text-ink disabled:opacity-50"
      >
        <Upload size={13} />
        {isUploading ? "Uploading…" : "Upload document"}
      </button>
    </>
  );
}
