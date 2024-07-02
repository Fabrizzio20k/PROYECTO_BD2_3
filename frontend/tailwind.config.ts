import type { Config } from "tailwindcss";

const config: Config = {
  content: [
    "./src/pages/**/*.{js,ts,jsx,tsx,mdx}",
    "./src/components/**/*.{js,ts,jsx,tsx,mdx}",
    "./src/app/**/*.{js,ts,jsx,tsx,mdx}",
  ],
  theme: {
    extend: {
      backgroundImage: {
        "gradient-radial": "radial-gradient(var(--tw-gradient-stops))",
        "gradient-conic":
          "conic-gradient(from 180deg at 50% 50%, var(--tw-gradient-stops))",
      },
      colors: {
        'midnight': {
          '50': '#e4f7ff',
          '100': '#cff0ff',
          '200': '#a8e1ff',
          '300': '#74caff',
          '400': '#3ea0ff',
          '500': '#1375ff',
          '600': '#0063ff',
          '700': '#0063ff',
          '800': '#0059e4',
          '900': '#003eb0',
          '950': '#000f2e',
        },

      },
    },
  },
  plugins: [],
};
export default config;
