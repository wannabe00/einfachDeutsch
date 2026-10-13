import { Infinity as InfinityIcon, Zap } from "lucide-react"

import { cn } from "@/lib/utils"

/*
 * Energy as a compact chip for the top bar: a bolt and how many are left
 * (premium: infinity). When energy isn't full, wide screens also show the
 * countdown to the next refill; everyone gets it in the tooltip. Values come
 * from `useEnergy`.
 */
export function EnergyMeter({
  energy,
  max,
  premium = false,
  secondsUntilNext = null,
  className,
}: {
  energy: number
  max: number
  premium?: boolean
  secondsUntilNext?: number | null
  className?: string
}) {
  const refill =
    !premium && energy < max && secondsUntilNext != null
      ? `+1 in ${formatCountdown(secondsUntilNext)}`
      : null
  const label = premium
    ? "Unlimited energy"
    : `${energy} of ${max} energy${refill ? `, ${refill}` : ""}`

  return (
    <div
      className={cn(
        "inline-flex h-9 items-center gap-1.5 rounded-full bg-surface-2 px-3 text-sm font-bold tabular-nums",
        className,
      )}
      title={label}
      aria-label={label}
    >
      <Zap
        className={cn("size-4", premium || energy > 0 ? "fill-current text-primary" : "text-muted-foreground")}
        aria-hidden="true"
      />
      {premium ? <InfinityIcon className="size-4" aria-hidden="true" /> : <span>{energy}</span>}
      {refill && (
        <span className="hidden text-xs font-medium text-muted-foreground xl:inline">{refill}</span>
      )}
    </div>
  )
}

function formatCountdown(totalSeconds: number): string {
  const s = Math.max(0, totalSeconds)
  const h = Math.floor(s / 3600)
  const m = Math.floor((s % 3600) / 60)
  if (h > 0) return `${h}h ${m}m`
  if (m > 0) return `${m}m`
  return `${s % 60}s`
}
