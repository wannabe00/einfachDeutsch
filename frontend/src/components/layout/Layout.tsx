import { Outlet } from "react-router-dom"

import { Sidebar } from "./Sidebar"
import { AIPanelProvider } from "@/contexts/AIPanelContext"
import { AIPanel } from "@/components/ai/AIPanel"

export function Layout() {
  return (
    <AIPanelProvider>
      <div className="flex min-h-screen bg-background text-foreground">
        <Sidebar />
        <main className="flex-1 px-6 py-8">
          <div className="mx-auto max-w-[900px]">
            <Outlet />
          </div>
        </main>
        <AIPanel />
      </div>
    </AIPanelProvider>
  )
}
