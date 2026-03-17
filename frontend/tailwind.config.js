/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "./app/**/*.{js,ts,jsx,tsx}",
    "./components/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        background: '#0F172A',
        secondary: '#111827',
        surface: '#1F2937',
        borderSoft: 'rgba(255,255,255,0.05)',
        textPrimary: '#F9FAFB',
        textSecondary: '#9CA3AF',
        textMuted: '#6B7280',
        positive: '#22C55E',
        warning: '#F59E0B',
        negative: '#EF4444',
      },
      borderRadius: {
        xl: "16px",
      },
    },
  },
  plugins: [],
};
