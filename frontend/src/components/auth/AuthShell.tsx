import type { ReactNode } from "react"

import { cn } from "@/lib/utils"
import { SITE_NAME } from "@/lib/site"

/** Centred single-column layout for the pages before the app: login,
    profile setup and level onboarding. */
export function AuthShell({
  children,
  maxWidth = "max-w-md",
}: {
  children: ReactNode
  maxWidth?: string
}) {
  return (
    <div className="flex min-h-screen items-center justify-center bg-background px-4 py-10">
      <div className={cn("w-full", maxWidth)}>{children}</div>
    </div>
  )
}

export function AuthWordmark() {
  return (
    <p className="text-center text-sm font-semibold uppercase tracking-[0.2em] text-primary">
      {SITE_NAME}
    </p>
  )
}
