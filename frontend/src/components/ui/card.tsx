import type { ReactNode } from "react"

import { cn } from "@/lib/utils"

/** The standard content container: a solid surface with a hairline border. */
export function Card({ className, children }: { className?: string; children: ReactNode }) {
  return (
    <div className={cn("rounded-xl border border-border bg-surface", className)}>{children}</div>
  )
}
