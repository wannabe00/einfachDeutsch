import { Outlet, useMatch } from "react-router-dom"
import type { ReactNode } from "react"

import { TopBar } from "./TopBar"
import { TabBar } from "./TabBar"
import { AIPanelProvider } from "@/contexts/AIPanelContext"
import { AIPanel } from "@/components/ai/AIPanel"

/*
 * App shell: the top bar (desktop nav), the page, and on phones a bottom tab
 * bar. Lessons and the level exam run full-screen with no navigation, so the
 * learner can focus.
 */
export function Layout({ children }: { children?: ReactNode }) {
  const inLesson = useMatch("/path/:unitId/lesson/:lessonId")
  const inExam = useMatch("/path/exam")
  const page = children ?? <Outlet />

  if (inLesson || inExam) {
    return (
      <div className="min-h-screen bg-background text-foreground">
        <main className="px-4 py-4 sm:px-6 sm:py-6">
          <div className="mx-auto max-w-2xl">{page}</div>
        </main>
      </div>
    )
  }

  return (
    <AIPanelProvider>
      <div className="flex min-h-screen flex-col bg-background text-foreground">
        <TopBar />
        <main className="min-w-0 flex-1 px-4 pb-28 pt-5 sm:px-6 sm:pt-8 lg:pb-12">
          <div className="mx-auto max-w-5xl">{page}</div>
        </main>
        <TabBar />
        <AIPanel />
      </div>
    </AIPanelProvider>
  )
}
