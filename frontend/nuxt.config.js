
// nuxt.config.js
// nuxt.config.js
import { defineNuxtConfig } from 'nuxt/config'

export default defineNuxtConfig({
  css: ['~/assets/css/tailwind.css'],
  postcss: {
    plugins: {
      '@tailwindcss/postcss': {}, // 👈 serve per Tailwind v4
      autoprefixer: {},
    },
  },
  devtools: { enabled: true },
})
