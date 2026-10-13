/** A small circular progress ring (0..1) in a unit's colour. */
export function ProgressRing({
  pct,
  color,
  size = 36,
  stroke = 4,
  label,
}: {
  pct: number
  color: string
  size?: number
  stroke?: number
  label?: string
}) {
  const r = (size - stroke) / 2
  const c = 2 * Math.PI * r
  const p = Math.min(Math.max(pct, 0), 1)
  return (
    <svg
      width={size}
      height={size}
      viewBox={`0 0 ${size} ${size}`}
      role={label ? "img" : undefined}
      aria-label={label}
      aria-hidden={label ? undefined : true}
      className="shrink-0"
    >
      <circle r={r} cx={size / 2} cy={size / 2} fill="none" stroke="hsl(var(--surface-2))" strokeWidth={stroke} />
      <circle
        r={r}
        cx={size / 2}
        cy={size / 2}
        fill="none"
        stroke={color}
        strokeWidth={stroke}
        strokeLinecap="round"
        strokeDasharray={c}
        strokeDashoffset={c * (1 - p)}
        transform={`rotate(-90 ${size / 2} ${size / 2})`}
        className="transition-[stroke-dashoffset] duration-700 ease-out"
      />
    </svg>
  )
}
