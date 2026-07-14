import type { ReactNode } from "react"

/* Shared page header (Design v2 — Cinematic). One consistent title treatment
   across study pages: a bold Space Grotesk heading (via the global h1 rule),
   an optional subtitle, and optional right-aligned actions. */
export function PageHeader({
  title,
  subtitle,
  actions,
}: {
  title: string
  subtitle?: ReactNode
  actions?: ReactNode
}) {
  return (
    <div className="flex flex-wrap items-end justify-between gap-3">
      <div className="min-w-0">
        <h1 className="text-2xl font-bold tracking-tight sm:text-3xl">{title}</h1>
        {subtitle !== undefined && (
          <div className="mt-1 text-sm text-muted-foreground">{subtitle}</div>
        )}
      </div>
      {actions && <div className="flex flex-wrap gap-2">{actions}</div>}
    </div>
  )
}
