import type { CSSProperties } from "react"

export interface RingStat {
  label: string
  value: string
  /** 0..1 */
  pct: number
  color: string
}

/** Apple Fitness-style rings, outermost first, with a legend beside them. */
export function TodayRings({ rings }: { rings: RingStat[] }) {
  return (
    <section className="d-card flex items-center gap-5 p-5 sm:p-6" aria-label="Progress rings">
      <svg width="140" height="140" viewBox="0 0 140 140" className="shrink-0" aria-hidden="true">
        {rings.map((r, i) => (
          <Ring key={r.label} radius={60 - i * 18} pct={r.pct} color={r.color} />
        ))}
      </svg>
      <div className="flex min-w-0 flex-col gap-2.5">
        {rings.map((r) => (
          <div key={r.label}>
            <p className="d-num text-xl leading-tight" style={{ color: r.color }}>
              {r.value}
            </p>
            <p className="text-[13px] text-[var(--d-muted)]">{r.label}</p>
          </div>
        ))}
      </div>
    </section>
  )
}

function Ring({ radius, pct, color }: { radius: number; pct: number; color: string }) {
  const c = 2 * Math.PI * radius
  const clamped = Math.min(Math.max(pct, 0), 1)
  return (
    <>
      <circle r={radius} cx="70" cy="70" fill="none" stroke={color} strokeOpacity={0.2} strokeWidth={14} />
      <circle
        r={radius}
        cx="70"
        cy="70"
        fill="none"
        stroke={color}
        strokeWidth={14}
        strokeLinecap="round"
        strokeDasharray={c}
        strokeDashoffset={c * (1 - clamped)}
        transform="rotate(-90 70 70)"
        className="d-ring-fill"
        style={{ "--c": c } as CSSProperties}
      />
    </>
  )
}
