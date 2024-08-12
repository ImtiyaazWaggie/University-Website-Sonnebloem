/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "./flaskr/templates/**/*.html",
    "./flaskr/static/src/**/*.js"
  ],
  theme: {
    extend: {},
  },
  plugins: [
    require('@tailwindcss/forms'),
    require('@tailwindcss/aspect-ratio'),
  ],
}
