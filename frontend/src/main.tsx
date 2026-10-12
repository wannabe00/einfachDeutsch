import { StrictMode } from "react"
import { createRoot } from "react-dom/client"
import { BrowserRouter } from "react-router-dom"
import { QueryClient, QueryClientProvider } from "@tanstack/react-query"

// Fonts are self-hosted: the production CSP blocks Google Fonts.
import "@fontsource/space-grotesk/500.css"
import "@fontsource/space-grotesk/700.css"
import "@fontsource/ibm-plex-sans/400.css"
import "@fontsource/ibm-plex-sans/500.css"
import "@fontsource/ibm-plex-sans/600.css"
import "./index.css"
import App from "./App.tsx"
import { AuthProvider } from "@/contexts/AuthContext"
import { GuestLimitProvider } from "@/contexts/GuestLimitContext"

const queryClient = new QueryClient()

createRoot(document.getElementById("root")!).render(
  <StrictMode>
      <QueryClientProvider client={queryClient}>
        <BrowserRouter>
          <AuthProvider>
            <GuestLimitProvider>
              <App />
            </GuestLimitProvider>
          </AuthProvider>
        </BrowserRouter>
      </QueryClientProvider>
  </StrictMode>
)
