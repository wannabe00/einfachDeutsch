import type { ReactNode } from "react"

import { cn } from "@/lib/utils"

/*
 * Design v3 "dark + depth" card. Instead of a hairline outline on flat black,
 * it uses a soft surface gradient, real elevation, and an optional accent bar +
 * glow so cards feel layered and (optionally) colour-coded per section.
 */
export function SectionCard({
  accent,
  glow = false,
  className,
  children,
}: {
  /** CSS colour (e.g. from `resolveAccent`) for the top bar + glow. */
  accent?: string
  glow?: boolean
  className?: string
  children: ReactNode
}) {
  return (
    <div
      className={cn(
        "relative overflow-hidden rounded-2xl border border-white/10",
        "bg-gradient-to-b from-surface-2 to-surface shadow-lg shadow-black/40",
        className,
      )}
    >
      {accent && (
        <div className="absolute inset-x-0 top-0 h-1" style={{ background: accent }} aria-hidden="true" />
      )}
      {glow && accent && (
        <div
          className="pointer-events-none absolute -right-12 -top-16 size-44 rounded-full opacity-20 blur-3xl"
          style={{ background: accent }}
          aria-hidden="true"
        />
      )}
      <div className="relative">{children}</div>
    </div>
  )
}
