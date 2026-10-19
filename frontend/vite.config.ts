import path from "node:path"
import { fileURLToPath } from "node:url"

import { defineConfig, type Plugin } from "vite"
import react from "@vitejs/plugin-react"

const __dirname = path.dirname(fileURLToPath(import.meta.url))

// The public address, used in index.html (%VITE_SITE_URL%), the sitemap and
// robots.txt. One setting to change when the site moves to its own domain.
process.env.VITE_SITE_URL ??= "https://einfach-deutsch.vercel.app"
process.env.VITE_GOOGLE_SITE_VERIFICATION ??= ""
const SITE_URL = process.env.VITE_SITE_URL.replace(/\/$/, "")

// Pages a search engine should index; the rest of the app needs a login.
const PUBLIC_PAGES = ["/", "/login", "/terms", "/privacy", "/refunds", "/cookies"]
const APP_PAGES = ["/path", "/review", "/exercises", "/drills", "/words", "/grammar", "/books", "/videos", "/history", "/lesen", "/schreiben", "/hoeren", "/talk", "/ai", "/settings", "/onboarding", "/auth", "/chapters", "/check", "/welcome", "/reset-password", "/speak"]

/** robots.txt and sitemap.xml, written into the build from SITE_URL. */
function seoFiles(): Plugin {
  return {
    name: "seo-files",
    apply: "build",
    generateBundle() {
      const today = new Date().toISOString().slice(0, 10)
      const urls = PUBLIC_PAGES.map(
        (p) => `  <url><loc>${SITE_URL}${p}</loc><lastmod>${today}</lastmod></url>`,
      ).join("\n")
      this.emitFile({
        type: "asset",
        fileName: "sitemap.xml",
        source: `<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n${urls}\n</urlset>\n`,
      })
      this.emitFile({
        type: "asset",
        fileName: "robots.txt",
        source: `User-agent: *\n${APP_PAGES.map((p) => `Disallow: ${p}`).join("\n")}\n\nSitemap: ${SITE_URL}/sitemap.xml\n`,
      })
    },
  }
}

// https://vite.dev/config/
export default defineConfig({
  plugins: [react(), seoFiles()],
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
