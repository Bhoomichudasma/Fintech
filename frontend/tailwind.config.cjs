/** @type {import('tailwindcss').Config} */
module.exports = {
  content: ["./index.html", "./src/**/*.{js,ts,jsx,tsx}"],
  theme: {
    extend: {
      colors: {
        midnight: "#0d0f1a",
        panel: "#121526",
        accent: "#8ef5b9",
        accent2: "#8c7bff",
        danger: "#ff6b6b",
        warning: "#f9cf58",
      },
      boxShadow: {
        soft: "0 10px 40px rgba(0,0,0,0.35)",
      },
      fontFamily: {
        sans: ["'Manrope'", "Inter", "system-ui", "sans-serif"],
      },
    },
  },
  plugins: [],
};
