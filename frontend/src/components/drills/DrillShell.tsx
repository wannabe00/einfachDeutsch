import type { ReactNode } from "react"

import { SessionBar } from "@/components/ui/SessionBar"

interface DrillShellProps {
  title: string
  onExit: () => void
  progress?: number // 0-100
  counter?: string
  children: ReactNode
}

/** The frame around a running drill: the session bar on top, the game below. */
export function DrillShell({ title, onExit, progress, counter, children }: DrillShellProps) {
  return (
    <div className="mx-auto flex max-w-3xl flex-col gap-8">
      <SessionBar
        onClose={onExit}
        closeLabel="Back to drills"
        title={title}
        progress={progress}
        counter={counter}
      />
      {children}
    </div>
  )
}
