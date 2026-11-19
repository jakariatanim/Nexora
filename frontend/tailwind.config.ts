import type { Config } from "tailwindcss";

const config: Config = {
  darkMode: "class",
  content: [
    "./src/pages/**/*.{js,ts,jsx,tsx,mdx}",
    "./src/components/**/*.{js,ts,jsx,tsx,mdx}",
    "./src/app/**/*.{js,ts,jsx,tsx,mdx}",
  ],
  theme: {
    extend: {
      colors: {
        obsidian: {
          950: "#05070A",
          900: "#07090E",
          850: "#0C1017",
          800: "#131924",
          700: "#1E2738"
        },
        cyan: {
          glow: "#00E5FF",
          subtle: "#00B4D8",
          deep: "#0077B6"
        },
        titanium: {
          light: "#E2E8F0",
          base: "#94A3B8",
          dark: "#475569"
        }
      },
      screens: {
        xs: "375px",
        sm: "640px",
        md: "768px",
        tablet: "834px",
        ipad: "1024px",
        lg: "1024px",
        xl: "1280px",
        "2xl": "1536px",
      },
      fontFamily: {
        sans: ["-apple-system", "BlinkMacSystemFont", "SF Pro Display", "SF Pro Text", "Helvetica Neue", "Segoe UI", "sans-serif"],
        display: ["-apple-system", "BlinkMacSystemFont", "SF Pro Display", "Helvetica Neue", "sans-serif"],
        mono: ["-apple-system", "BlinkMacSystemFont", "SF Pro Text", "Helvetica Neue", "sans-serif"]
      },
      boxShadow: {
        "cyan-glow": "0 0 35px -5px rgba(0, 229, 255, 0.25)",
        "cyan-pill": "0 0 20px 0px rgba(0, 229, 255, 0.35)",
        "glass": "0 8px 32px 0 rgba(0, 0, 0, 0.37)"
      }
    },
  },
  plugins: [
    require('@tailwindcss/container-queries'),
  ],
};
export default config;
