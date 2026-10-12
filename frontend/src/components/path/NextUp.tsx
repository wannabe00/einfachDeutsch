import { Link } from "react-router-dom"
import { ArrowRight } from "lucide-react"

/*
 * "What's next" banner, shown on the path, the Dashboard and locked pages.
 * Tapping it continues where you left off.
 */
export function NextUp({
  kicker = "Continue",
  title,
  subtitle,
  href,
  accent = "hsl(var(--brand))",
}: {
  kicker?: string
  title: string
  subtitle?: string
  href: string
  accent?: string
}) {
  return (
    <Link
      to={href}
      className="group flex items-center gap-4 rounded-xl border border-border bg-surface p-4 transition-colors hover:bg-surface-2"
    >
      <span
        className="flex size-12 shrink-0 items-center justify-center rounded-xl text-white"
        style={{ background: accent }}
      >
        <ArrowRight className="size-6 transition-transform group-hover:translate-x-0.5" />
      </span>
      <div className="min-w-0">
        <p className="text-xs font-semibold uppercase tracking-wider text-muted-foreground">{kicker}</p>
        <p className="truncate font-bold">{title}</p>
        {subtitle && <p className="truncate text-sm text-muted-foreground">{subtitle}</p>}
      </div>
    </Link>
  )
}
