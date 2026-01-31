/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "./app/**/*.{js,ts,jsx,tsx}",
    "./components/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        bg: "#020617",
        panel: "#0f172a",
        border: "rgba(255,255,255,0.08)",
        muted: "#94a3b8",
        text: "#e5e7eb",
        good: "#22c55e",
        warn: "#f59e0b",
        bad: "#ef4444",
      },
      borderRadius: {
        xl: "16px",
      },
    },
  },
  plugins: [],
};
