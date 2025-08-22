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
  css: ['~/assets/css/tailwind.css'],
  
  // Modules
  modules: [
    '@nuxtjs/tailwindcss'
  ],
  
  // Development server configuration
  devtools: { enabled: true },
  
  // Runtime configuration
  runtimeConfig: {
    // 這些變數只在伺服器端可用
    // privateRuntimeConfig: {}, 
    
    // public 中的變數在客戶端和伺服器端都可用
    public: {
      apiBase: process.env.NUXT_PUBLIC_API_BASE || 'http://127.0.0.1:8001'
    }
  }
  
  // Note: router.mode is deprecated in Nuxt 3
  // SPA routing is handled by ssr: false
})
