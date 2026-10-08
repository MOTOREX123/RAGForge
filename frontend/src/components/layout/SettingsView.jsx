import { Server, Wifi, Database, BrainCircuit, SlidersHorizontal, Save, Loader2 } from "lucide-react";
import { useState } from "react";

export function SettingsView() {
  const [settings, setSettings] = useState({
    // AI Provider
    primaryProvider: "ollama",
    ollamaModel: "llama3.1:8b",
    ollamaUrl: "http://localhost:11434",
    fallbackProvider: "openrouter",
    openrouterModel: "nvidia/nemotron-3-ultra",
    openrouterApiKey: "", // Not displayed for security

    // Vector Store
    vectorStorePath: "./vectorstore",
    embeddingModel: "nomic-embed-text",
    chunkSize: 512,
    chunkOverlap: 50,

    // Retrieval
    topK: 10,
    candidateK: 10,
    rerankTopK: 5,
    minScore: 0.0,
    maxContextChunks: 3,

    // Conversation
    maxTurns: 5,
  });

  const [saved, setSaved] = useState(false);
  const [saving, setSaving] = useState(false);

  const handleChange = (key, value) => {
    setSettings((prev) => ({ ...prev, [key]: value }));
    setSaved(false);
  };

  const handleSave = async () => {
    setSaving(true);
    // In a real app, this would POST to the backend
    await new Promise((resolve) => setTimeout(resolve, 1000));
    setSaving(false);
    setSaved(true);
    setTimeout(() => setSaved(false), 3000);
  };

  const sectionStyle = "space-y-4";
  const labelStyle = "block mb-1 text-sm font-medium text-ink";
  const inputStyle = "w-full rounded-lg border border-line bg-surface px-3 py-2 text-sm text-ink placeholder:text-ink-muted focus:border-purple/50 focus:outline-none";
  const selectStyle = "w-full rounded-lg border border-line bg-surface px-3 py-2 text-sm text-ink focus:border-purple/50 focus:outline-none";

  return (
    <div className="flex h-full flex-col bg-bg">
      {/* Header */}
      <div className="border-b border-line px-4 py-3">
        <div className="flex items-center gap-2.5">
          <img
            src="/assets/ragforge-logo.png"
            alt="RAGForge"
            className="w-6 h-6"
          />
          <div>
            <h1 className="font-display text-lg font-semibold text-ink">Settings</h1>
            <p className="text-[11px] text-ink-muted">Configure RAGForge behavior and providers</p>
          </div>
        </div>
      </div>

      {/* Content */}
      <div className="flex-1 overflow-y-auto px-4 py-4">
        <div className="w-full space-y-6">
          {/* AI Providers */}
          <section className={sectionStyle}>
            <div className="flex items-center gap-2 mb-3">
              <BrainCircuit size={18} className="text-purple" />
              <h2 className="font-display text-base font-semibold text-ink">AI Providers</h2>
            </div>

            <div className="rounded-lg border border-line bg-surface p-4 space-y-3">
              <div>
                <label className={labelStyle}>Primary Provider</label>
                <select
                  value={settings.primaryProvider}
                  onChange={(e) => handleChange("primaryProvider", e.target.value)}
                  className={selectStyle}
                >
                  <option value="ollama">Ollama (Local)</option>
                  <option value="openrouter">OpenRouter (Cloud)</option>
                </select>
              </div>

              {settings.primaryProvider === "ollama" && (
                <>
                  <div>
                    <label className={labelStyle}>Ollama Model</label>
                    <select
                      value={settings.ollamaModel}
                      onChange={(e) => handleChange("ollamaModel", e.target.value)}
                      className={selectStyle}
                    >
                      <option value="llama3.1:8b">Llama 3.1 8B</option>
                      <option value="llama3.1:70b">Llama 3.1 70B</option>
                      <option value="gemma3:4b">Gemma 3 4B</option>
                      <option value="gemma3:12b">Gemma 3 12B</option>
                      <option value="mistral:7b">Mistral 7B</option>
                    </select>
                  </div>
                  <div>
                    <label className={labelStyle}>Ollama URL</label>
                    <input
                      type="text"
                      value={settings.ollamaUrl}
                      onChange={(e) => handleChange("ollamaUrl", e.target.value)}
                      className={inputStyle}
                      placeholder="http://localhost:11434"
                    />
                  </div>
                </>
              )}

              <div className="pt-2 border-t border-line">
                <label className={labelStyle}>Fallback Provider</label>
                <select
                  value={settings.fallbackProvider}
                  onChange={(e) => handleChange("fallbackProvider", e.target.value)}
                  className={selectStyle}
                >
                  <option value="openrouter">OpenRouter</option>
                  <option value="gemini">Google Gemini</option>
                </select>
              </div>

              {settings.fallbackProvider === "openrouter" && (
                <div>
                  <label className={labelStyle}>OpenRouter Model</label>
                  <select
                    value={settings.openrouterModel}
                    onChange={(e) => handleChange("openrouterModel", e.target.value)}
                    className={selectStyle}
                  >
                    <option value="nvidia/nemotron-3-ultra">Nemotron 3 Ultra</option>
                    <option value="anthropic/claude-3.5-sonnet">Claude 3.5 Sonnet</option>
                    <option value="openai/gpt-4o">GPT-4o</option>
                    <option value="meta-llama/llama-3.1-70b-instruct">Llama 3.1 70B</option>
                  </select>
                </div>
              )}
            </div>
          </section>

          {/* Vector Store */}
          <section className={sectionStyle}>
            <div className="flex items-center gap-2 mb-3">
              <Database size={18} className="text-purple" />
              <h2 className="font-display text-base font-semibold text-ink">Vector Store</h2>
            </div>

            <div className="rounded-lg border border-line bg-surface p-4 space-y-3">
              <div>
                <label className={labelStyle}>Vector Store Path</label>
                <input
                  type="text"
                  value={settings.vectorStorePath}
                  onChange={(e) => handleChange("vectorStorePath", e.target.value)}
                  className={inputStyle}
                  readOnly
                />
                <p className="mt-1 text-[10px] text-ink-muted">Requires server restart to change</p>
              </div>
              <div>
                <label className={labelStyle}>Embedding Model</label>
                <select
                  value={settings.embeddingModel}
                  onChange={(e) => handleChange("embeddingModel", e.target.value)}
                  className={selectStyle}
                >
                  <option value="nomic-embed-text">nomic-embed-text</option>
                  <option value="all-MiniLM-L6-v2">all-MiniLM-L6-v2</option>
                  <option value="mxbai-embed-large">mxbai-embed-large</option>
                </select>
              </div>
              <div className="grid grid-cols-2 gap-3">
                <div>
                  <label className={labelStyle}>Chunk Size</label>
                  <input
                    type="number"
                    value={settings.chunkSize}
                    onChange={(e) => handleChange("chunkSize", parseInt(e.target.value))}
                    className={inputStyle}
                    min="100"
                    max="2000"
                  />
                </div>
                <div>
                  <label className={labelStyle}>Chunk Overlap</label>
                  <input
                    type="number"
                    value={settings.chunkOverlap}
                    onChange={(e) => handleChange("chunkOverlap", parseInt(e.target.value))}
                    className={inputStyle}
                    min="0"
                    max="500"
                  />
                </div>
              </div>
            </div>
          </section>

          {/* Retrieval Configuration */}
          <section className={sectionStyle}>
            <div className="flex items-center gap-2 mb-3">
              <SlidersHorizontal size={18} className="text-purple" />
              <h2 className="font-display text-base font-semibold text-ink">Retrieval Configuration</h2>
            </div>

            <div className="rounded-lg border border-line bg-surface p-4 space-y-3">
              <div className="grid grid-cols-2 gap-3">
                <div>
                  <label className={labelStyle}>Top K (Initial)</label>
                  <input
                    type="number"
                    value={settings.topK}
                    onChange={(e) => handleChange("topK", parseInt(e.target.value))}
                    className={inputStyle}
                    min="1"
                    max="50"
                  />
                </div>
                <div>
                  <label className={labelStyle}>Candidate K</label>
                  <input
                    type="number"
                    value={settings.candidateK}
                    onChange={(e) => handleChange("candidateK", parseInt(e.target.value))}
                    className={inputStyle}
                    min="1"
                    max="50"
                  />
                </div>
              </div>
              <div className="grid grid-cols-2 gap-3">
                <div>
                  <label className={labelStyle}>Rerank Top K</label>
                  <input
                    type="number"
                    value={settings.rerankTopK}
                    onChange={(e) => handleChange("rerankTopK", parseInt(e.target.value))}
                    className={inputStyle}
                    min="1"
                    max="20"
                  />
                </div>
                <div>
                  <label className={labelStyle}>Min Score</label>
                  <input
                    type="number"
                    value={settings.minScore}
                    onChange={(e) => handleChange("minScore", parseFloat(e.target.value))}
                    className={inputStyle}
                    min="0"
                    max="1"
                    step="0.01"
                  />
                </div>
              </div>
              <div>
                <label className={labelStyle}>Max Context Chunks</label>
                <input
                  type="number"
                  value={settings.maxContextChunks}
                  onChange={(e) => handleChange("maxContextChunks", parseInt(e.target.value))}
                  className={inputStyle}
                  min="1"
                  max="10"
                />
              </div>
            </div>
          </section>

          {/* Conversation */}
          <section className={sectionStyle}>
            <div className="flex items-center gap-2 mb-3">
              <Server size={18} className="text-purple" />
              <h2 className="font-display text-base font-semibold text-ink">Conversation</h2>
            </div>

            <div className="rounded-lg border border-line bg-surface p-4 space-y-3">
              <div>
                <label className={labelStyle}>Max Conversation Turns</label>
                <input
                  type="number"
                  value={settings.maxTurns}
                  onChange={(e) => handleChange("maxTurns", parseInt(e.target.value))}
                  className={inputStyle}
                  min="1"
                  max="20"
                />
                <p className="mt-1 text-[10px] text-ink-muted">Number of previous turns to include for context-aware queries</p>
              </div>
            </div>
          </section>

          {/* Save button */}
          <div className="flex justify-end pt-3 border-t border-line">
            <button
              type="button"
              onClick={handleSave}
              disabled={saving}
              className="flex items-center gap-2 rounded-lg bg-purple px-4 py-2 text-sm font-medium text-white transition-opacity disabled:opacity-50"
            >
              {saving ? <Loader2 size={14} className="animate-spin" /> : <Save size={14} />}
              {saving ? "Saving…" : saved ? "Saved!" : "Save Settings"}
            </button>
          </div>
        </div>
      </div>
    </div>
  );
}