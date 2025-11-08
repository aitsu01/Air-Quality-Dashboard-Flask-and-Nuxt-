
// nuxt.config.js
import { defineNuxtConfig } from 'nuxt/config'

export default defineNuxtConfig({
  
  css: ['~/assets/css/tailwind.css'],
  postcss: {
    plugins: {
      '@tailwindcss/postcss': {}, 
      autoprefixer: {},
    },
  },
  devtools: { enabled: true },
})





