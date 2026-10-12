import { cn } from "@/lib/utils"

interface StatCardProps {
  value: number | string
  label: string
  /** Draw attention to this stat (e.g. reviews due today). */
  highlight?: boolean
  className?: string
}

export function StatCard({ value, label, highlight, className }: StatCardProps) {
  return (
    <div
      className={cn(
        "rounded-xl border bg-surface px-4 py-3",
        highlight ? "border-primary/60" : "border-border",
        className,
      )}
    >
      <p className="font-grotesk text-2xl font-bold tabular-nums">{value}</p>
      <p className="mt-0.5 text-sm text-muted-foreground">{label}</p>
    </div>
  )
}
