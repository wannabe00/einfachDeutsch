import { Link } from "react-router-dom"
import { ArrowRight } from "lucide-react"

/*
 * The persistent "what's next" indicator (Spec v3) — shown atop the path, on the
 * Dashboard, and on gated pages. One tap continues where you left off.
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
      className="group flex items-center gap-4 rounded-2xl border border-white/10 bg-gradient-to-b from-surface-2 to-surface p-4 shadow-lg shadow-black/40 transition-transform hover:-translate-y-0.5"
    >
      <span
        className="flex size-12 shrink-0 items-center justify-center rounded-xl text-white"
        style={{ background: accent, boxShadow: `0 8px 20px -6px ${accent}` }}
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
