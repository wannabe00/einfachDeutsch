import { Check, Crown, Lock, Play, Star } from "lucide-react"

import { cn } from "@/lib/utils"

type NodeState = "completed" | "current" | "available" | "locked"

/*
 * One lesson on the path. Four states: completed (crown in the unit colour),
 * current (highlighted, with a "start" label), available (outlined) and locked
 * (grey, with a lock). `accent` is the unit's colour.
 */
export function PathNode({
  state,
  label,
  accent = "hsl(var(--brand))",
  crownLevel = 0,
  onClick,
  className,
}: {
  state: NodeState
  label: string
  accent?: string
  crownLevel?: number
  onClick?: () => void
  className?: string
}) {
  const locked = state === "locked"
  const Icon =
    state === "completed" ? (crownLevel > 0 ? Crown : Check) : state === "current" ? Play : locked ? Lock : Star

  return (
    <div className={cn("flex flex-col items-center gap-1.5", className)}>
      <button
        type="button"
        onClick={onClick}
        disabled={locked}
        aria-label={label}
        className={cn(
          "relative flex size-16 items-center justify-center rounded-full transition-transform",
          !locked && "hover:-translate-y-0.5 active:translate-y-0",
          locked && "cursor-not-allowed",
        )}
        style={
          state === "completed"
            ? { background: accent }
            : undefined
        }
      >
        {/* current: pulsing ring in the accent */}
        {state === "current" && (
          <span
            className="absolute inset-0 animate-ping rounded-full opacity-40"
            style={{ background: accent }}
            aria-hidden="true"
          />
        )}
        <span
          className={cn(
            "relative flex size-16 items-center justify-center rounded-full",
            state === "current" && "text-white",
            state === "available" && "border-2 border-dashed border-white/25 text-muted-foreground",
            locked && "bg-surface text-muted-foreground ring-1 ring-border",
          )}
          style={
            state === "current"
              ? { background: accent }
              : undefined
          }
        >
          <Icon className={cn("size-6", state === "completed" && "text-white")} />
        </span>
      </button>
      <span
        className={cn(
          "max-w-[7rem] truncate text-center text-xs font-medium",
          locked ? "text-muted-foreground/60" : "text-foreground",
        )}
      >
        {label}
      </span>
    </div>
  )
}
