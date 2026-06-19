import type { ReactNode } from "react"
import { ArrowLeft } from "lucide-react"

interface DrillShellProps {
  title: string
  onExit: () => void
  progress?: number // 0-100
  counter?: string
  children: ReactNode
}

export function DrillShell({ title, onExit, progress, counter, children }: DrillShellProps) {
  return (
    <div>
      <div className="mb-4 flex items-center justify-between">
        <button
          onClick={onExit}
          className="inline-flex items-center gap-1.5 text-sm text-muted-foreground hover:text-accent"
        >
          <ArrowLeft className="size-4" /> Drills
        </button>
        <div className="flex items-center gap-3">
          <span className="text-sm font-medium text-foreground">{title}</span>
          {counter && <span className="text-sm text-muted-foreground">{counter}</span>}
        </div>
      </div>
      {progress !== undefined && (
        <div className="mb-8 h-1 w-full rounded-full bg-border">
          <div
            className="h-1 rounded-full bg-accent transition-all duration-300"
            style={{ width: `${progress}%` }}
          />
        </div>
      )}
      {children}
    </div>
  )
}
