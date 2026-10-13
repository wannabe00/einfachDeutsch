import type { ReactNode } from "react"

import { cn } from "@/lib/utils"

/** The standard content container: a raised surface with a soft shadow. */
export function Card({ className, children }: { className?: string; children: ReactNode }) {
  return (
    <div className={cn("rounded-2xl bg-surface shadow-card", className)}>{children}</div>
  )
}
