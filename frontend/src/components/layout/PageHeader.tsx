import type { ReactNode } from "react"

import { usePageTitle } from "@/lib/usePageTitle"

/* Page title with an optional subtitle and right-aligned actions. */
export function PageHeader({
  title,
  subtitle,
  actions,
}: {
  title: string
  subtitle?: ReactNode
  actions?: ReactNode
}) {
  usePageTitle(title)
  return (
    <div className="flex flex-wrap items-end justify-between gap-3">
      <div className="min-w-0">
        <h1 className="text-3xl font-extrabold sm:text-4xl">{title}</h1>
        {subtitle !== undefined && (
          <div className="mt-1.5 text-[15px] text-muted-foreground">{subtitle}</div>
        )}
      </div>
      {actions && <div className="flex flex-wrap gap-2">{actions}</div>}
    </div>
  )
}
