/** @type {import('tailwindcss').Config} */
export default {
  content: ["./index.html", "./src/**/*.{js,jsx}"],
  theme: {
    extend: {
      colors: {
        bg: "#12151A",
        surface: "#191D24",
        raised: "#1F242C",
        line: "rgba(233, 227, 213, 0.09)",
        ink: "#ECE8DF",
        "ink-dim": "#8B8F98",
        paper: "#E9E2D0",
        "paper-ink": "#2B2823",
        brass: "#C68A3D",
        "brass-dim": "#8A6230",
        teal: "#5B8C99",
        "teal-dim": "#3F626C",
        danger: "#C1594B",
        "danger-dim": "#4A2E2A",
      },
      fontFamily: {
        display: ["'Source Serif 4'", "serif"],
        sans: ["Inter", "system-ui", "sans-serif"],
        mono: ["'IBM Plex Mono'", "ui-monospace", "monospace"],
      },
      maxWidth: {
        prose: "680px",
      },
    },
  },
  plugins: [],
};
