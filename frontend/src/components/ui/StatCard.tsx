import type { LucideIcon } from "lucide-react"

import { cn } from "@/lib/utils"

interface StatCardProps {
  icon: LucideIcon
  value: number
  label: string
  accent?: boolean
}

export function StatCard({ icon: Icon, value, label, accent }: StatCardProps) {
  return (
    <div
      className={cn(
        "flex flex-col gap-2 rounded-xl border bg-surface p-5 shadow-sm",
        accent ? "border-accent" : "border-border",
      )}
    >
      <Icon
        className={cn("size-5", accent ? "text-accent" : "text-muted-foreground")}
        aria-hidden="true"
      />
      <span className="text-3xl font-bold tracking-tight text-foreground">
        {value}
      </span>
      <span className="text-sm text-muted-foreground">{label}</span>
    </div>
  )
}
