import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

// https://vite.dev/config/
export default defineConfig({
  plugins: [react()],
  server:{
    proxy:{
      '/Video':  { target: 'http://localhost:5246', changeOrigin: true },
      '/api':    { target: 'http://localhost:5246', changeOrigin: true },
      '/videos': { target: 'http://localhost:5246', changeOrigin: true },
    }
  },
})
