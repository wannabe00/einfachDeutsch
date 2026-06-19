import path from "node:path"
import { fileURLToPath } from "node:url"

import { defineConfig } from "vite"
import react from "@vitejs/plugin-react"

const __dirname = path.dirname(fileURLToPath(import.meta.url))

// https://vite.dev/config/
export default defineConfig({
  plugins: [react()],
  resolve: {
    alias: {
      "@": path.resolve(__dirname, "./src"),
    },
  },
  // Honor a PORT env var (used by tooling/preview) but default to Vite's 5173.
  server: {
    port: process.env.PORT ? Number(process.env.PORT) : 5173,
  },
})
