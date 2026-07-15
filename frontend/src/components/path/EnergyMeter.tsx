import { Infinity as InfinityIcon, Zap } from "lucide-react"

import { cn } from "@/lib/utils"

/*
 * Energy meter (Spec v3). Free users see `max` bolts with `energy` filled and a
 * countdown to the next refill; premium users see an infinity bolt. Presentational
 * only — the live values come from the energy API (wired in brick 23.6).
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
  const brand = "hsl(var(--brand))"

  if (premium) {
    return (
      <div className={cn("inline-flex items-center gap-1.5 text-sm font-semibold", className)} style={{ color: brand }}>
        <Zap className="size-4 fill-current" />
        <InfinityIcon className="size-4" />
      </div>
    )
  }

  return (
    <div className={cn("inline-flex items-center gap-2", className)}>
      <div className="flex items-center gap-1" aria-label={`${energy} of ${max} energy`}>
        {Array.from({ length: max }).map((_, i) => (
          <Zap
            key={i}
            className={cn("size-4", i < energy ? "fill-current" : "text-muted-foreground/30")}
            style={i < energy ? { color: brand } : undefined}
          />
        ))}
      </div>
      {energy < max && secondsUntilNext != null && (
        <span className="text-xs tabular-nums text-muted-foreground">+1 in {formatCountdown(secondsUntilNext)}</span>
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
