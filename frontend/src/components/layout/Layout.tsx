import { Outlet } from "react-router-dom"
import type { ReactNode } from "react"

import { Sidebar } from "./Sidebar"
import { AIPanelProvider } from "@/contexts/AIPanelContext"
import { AIPanel } from "@/components/ai/AIPanel"

export function Layout({ children }: { children?: ReactNode }) {
  return (
    <AIPanelProvider>
      <div className="flex min-h-screen bg-background text-foreground">
        <Sidebar />
        <main className="min-w-0 flex-1 px-4 py-6 sm:px-6 sm:py-8">
          <div className="mx-auto max-w-[900px]">{children ?? <Outlet />}</div>
        </main>
        <AIPanel />
      </div>
    </AIPanelProvider>
  )
}
