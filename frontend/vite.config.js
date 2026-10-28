import { defineConfig, loadEnv } from 'vite'
import react from '@vitejs/plugin-react'
import tailwindcss from '@tailwindcss/vite'

export default defineConfig(({ mode }) => {
  const env = loadEnv(mode, process.cwd(), '')

  // Where the FastAPI backend runs during local development.
  const apiTarget = env.VITE_DEV_API_TARGET || 'http://127.0.0.1:8000'

  const proxy = {
    '/api': { target: apiTarget, changeOrigin: true },
    '/health': { target: apiTarget, changeOrigin: true },
  }

  return {
    plugins: [react(), tailwindcss()],
    server: { proxy },
    preview: { proxy },
  }
})
