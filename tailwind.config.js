/** @type {import('tailwindcss').Config} */
const defaultTheme = require("tailwindcss/defaultTheme");

module.exports = {
  content: ["./app/templates/**/*.j2"],
  theme: {
    extend: {
      fontFamily: {
        sans: ['VT323', ...defaultTheme.fontFamily.sans],
      },
    },
  },
  daisyui: {
    themes: [
      {
        "dark": {
          "primary": "#4ade80",
          "secondary": "#fb7185",
          "accent": "#38bdf8",
          "neutral": "#374151",
          "base-100": "#101010",
          "base-content": "#edf0f3",
          "info": "#2094f3",
          "success": "#4ade80",
          "warning": "#facc15",
          "error": "#ef4444"
        },
      },
    ],

  },
  plugins: [require("daisyui")],
}

