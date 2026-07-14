import { Outlet } from "react-router-dom"
import type { ReactNode } from "react"

import { TopBar } from "./TopBar"
import { AIPanelProvider } from "@/contexts/AIPanelContext"
import { AIPanel } from "@/components/ai/AIPanel"

/* App shell (Design v2 — Cinematic). Navigation lives entirely in the top bar
   (desktop dropdowns) and the mobile drawer it owns — there's no left rail — so
   the main column spans the full width beneath it. */
export function Layout({ children }: { children?: ReactNode }) {
  return (
    <AIPanelProvider>
      <div className="flex min-h-screen flex-col bg-background text-foreground">
        <TopBar />
        <main className="min-w-0 flex-1 px-4 py-6 sm:px-6 sm:py-8">
          <div className="mx-auto max-w-5xl">{children ?? <Outlet />}</div>
        </main>
        <AIPanel />
      </div>
    </AIPanelProvider>
  )
}
