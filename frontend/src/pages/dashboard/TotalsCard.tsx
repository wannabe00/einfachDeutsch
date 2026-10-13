/** Lifetime totals as big numbers. */
export function TotalsCard({
  items,
  className = "",
}: {
  items: { label: string; value: number }[]
  className?: string
}) {
  return (
    <section className={`d-card grid grid-cols-2 gap-x-3 gap-y-5 p-5 sm:p-6 ${className}`} aria-label="Totals">
      {items.map((it) => (
        <div key={it.label}>
          <p className="d-num text-[30px] leading-tight">{it.value.toLocaleString("en-US")}</p>
          <p className="text-[13px] text-[var(--d-muted)]">{it.label}</p>
        </div>
      ))}
    </section>
  )
}
