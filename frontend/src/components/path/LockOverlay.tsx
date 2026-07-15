import type { ReactNode } from "react"
import { Lock } from "lucide-react"

import { cn } from "@/lib/utils"

/*
 * The one consistent "not unlocked yet" treatment (Spec v3) used across the path,
 * Word Bank, Grammar, Videos, History. Blurs + dims its children and overlays a
 * lock with an optional hint ("Finish Lesson 3 to unlock"). When `locked` is
 * false it renders children untouched.
 */
export function LockOverlay({
  locked,
  hint,
  className,
  children,
}: {
  locked: boolean
  hint?: string
  className?: string
  children: ReactNode
}) {
  if (!locked) return <>{children}</>
  return (
    <div className={cn("relative", className)}>
      <div className="pointer-events-none select-none opacity-40 blur-[3px]" aria-hidden="true">
        {children}
      </div>
      <div className="absolute inset-0 flex flex-col items-center justify-center gap-1.5 rounded-2xl bg-background/40">
        <span className="flex size-9 items-center justify-center rounded-full bg-background/80 text-muted-foreground ring-1 ring-white/10">
          <Lock className="size-4" />
        </span>
        {hint && <span className="max-w-[80%] text-center text-xs text-muted-foreground">{hint}</span>}
      </div>
    </div>
  )
}
