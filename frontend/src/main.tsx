import { StrictMode } from "react"
import { createRoot } from "react-dom/client"
import { BrowserRouter } from "react-router-dom"
import { QueryClient, QueryClientProvider } from "@tanstack/react-query"

import "./index.css"
import App from "./App.tsx"
import { CanonicalUrl } from "@/components/layout/CanonicalUrl"
import { AuthProvider } from "@/contexts/AuthContext"
import { GuestLimitProvider } from "@/contexts/GuestLimitContext"
import { applyTheme, getThemePref } from "@/lib/theme"
import { startMonitoring } from "@/lib/monitoring"

applyTheme(getThemePref())
startMonitoring()

const queryClient = new QueryClient()

createRoot(document.getElementById("root")!).render(
  <StrictMode>
      <QueryClientProvider client={queryClient}>
        <BrowserRouter>
          <AuthProvider>
            <GuestLimitProvider>
              <CanonicalUrl />
              <App />
            </GuestLimitProvider>
          </AuthProvider>
        </BrowserRouter>
      </QueryClientProvider>
  </StrictMode>
)
