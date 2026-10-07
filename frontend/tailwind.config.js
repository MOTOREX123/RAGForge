/** @type {import('tailwindcss').Config} */
export default {
  content: ["./index.html", "./src/**/*.{js,jsx}"],
  theme: {
    extend: {
      colors: {
        bg: "#0B0F14",
        surface: "#11171E",
        raised: "#181F2A",
        line: "rgba(139, 148, 158, 0.12)",
        ink: "#E8ECF1",
        "ink-dim": "#6B7280",
        "ink-muted": "#4B5563",
        purple: "#7C5CFF",
        "purple-dim": "#5B3DCC",
        "purple-glow": "rgba(124, 92, 255, 0.3)",
        "purple-bg": "rgba(124, 92, 255, 0.08)",
        green: "#10B981",
        "green-dim": "#059669",
        yellow: "#F59E0B",
        "yellow-dim": "#D97706",
        red: "#EF4444",
        "red-dim": "#DC2626",
      },
      fontFamily: {
        display: ["'JetBrains Mono'", "ui-monospace", "monospace"],
        sans: ["Inter", "system-ui", "sans-serif"],
        mono: ["'JetBrains Mono'", "ui-monospace", "monospace"],
      },
      maxWidth: {
        prose: "720px",
      },
      spacing: {
        "18": "4.5rem",
        "88": "22rem",
      },
    },
  },
  plugins: [],
};