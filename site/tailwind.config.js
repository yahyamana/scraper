/** @type {import('tailwindcss').Config} */
module.exports = {
  // Dark rules compile as `.dark .dark\:*`, matching the toggle in index.html.
  // Without this key Tailwind defaults to `media` and the toggle stops working.
  darkMode: 'class',
  content: ["index.html", "./node_modules/flowbite/**/*.js"],
  theme: {
    extend: {},
  },
  plugins: [
    require('flowbite/plugin')
  ],
}
