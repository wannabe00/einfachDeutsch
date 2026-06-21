import { Outlet } from "react-router-dom"
import type { ReactNode } from "react"

import { Sidebar } from "./Sidebar"
import { TopBar } from "./TopBar"
import { AIPanelProvider } from "@/contexts/AIPanelContext"
import { AIPanel } from "@/components/ai/AIPanel"

export function Layout({ children }: { children?: ReactNode }) {
  return (
    <AIPanelProvider>
      <div className="flex min-h-screen flex-col bg-background text-foreground">
        <TopBar />
        <div className="flex flex-1">
          <Sidebar />
          <main className="min-w-0 flex-1 px-4 py-6 sm:px-6 sm:py-8">
            <div className="mx-auto max-w-[900px]">{children ?? <Outlet />}</div>
          </main>
        </div>
        <AIPanel />
      </div>
    </AIPanelProvider>
  )
}
