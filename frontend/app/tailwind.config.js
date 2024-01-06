/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        LogoBg: 'rgb(214, 240, 247)'
      }
    },
  },
  plugins: [
    require('@tailwindcss/forms')
  ],
}

