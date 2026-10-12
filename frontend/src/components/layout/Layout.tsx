import { Outlet } from "react-router-dom"
import type { ReactNode } from "react"

import { TopBar } from "./TopBar"
import { AIPanelProvider } from "@/contexts/AIPanelContext"
import { AIPanel } from "@/components/ai/AIPanel"

/* App shell. All navigation is in the top bar (and its mobile drawer), so the
   main column takes the full width below it. */
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
