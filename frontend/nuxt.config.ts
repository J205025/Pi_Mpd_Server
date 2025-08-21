// nuxt.config.ts
export default defineNuxtConfig({
  // Enable SPA mode for client-side routing
  ssr: false,
  
  // Configure for static generation
  nitro: {
    preset: 'static'
  },
  
  // Disable payload extraction for SPA mode
  experimental: {
    payloadExtraction: false
  },
  
  // Configure the app for SPA deployment
  app: {
    // Base URL if serving from a subdirectory
    // baseURL: '/app/',
    
    // Configure the router for SPA mode
    head: {
      title: 'My Media Player',
      meta: [
        { charset: 'utf-8' },
        { name: 'viewport', content: 'width=device-width, initial-scale=1' }
      ]
    }
  },
  
  // CSS framework (if using Tailwind)
  css: ['~/assets/css/tailwind.css'], // Corrected to use tailwind.css
  
  // Modules
  modules: [
    '@nuxtjs/tailwindcss'
  ],
  
  // Development server configuration
  devtools: { enabled: true },
  
  // Router configuration for SPA
  router: {
    // Ensure proper SPA routing
    mode: 'history'
  }
})