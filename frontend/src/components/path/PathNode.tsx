import { Check, Crown, Lock, Play, Star } from "lucide-react"

import { cn } from "@/lib/utils"

export type NodeState = "completed" | "current" | "available" | "locked"

/*
 * A single lesson step on the Duolingo-style path (Spec v3 / Design v3). Four
 * states: completed (crown/check in the section accent), current (highlighted,
 * pulsing "start"), available (outlined), locked (greyed + lock). `accent` is
 * the unit's section colour.
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
            ? { background: accent, boxShadow: `0 8px 20px -6px ${accent}` }
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
            locked && "bg-surface text-muted-foreground ring-1 ring-white/10",
          )}
          style={
            state === "current"
              ? { background: accent, boxShadow: `0 8px 24px -6px ${accent}` }
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
