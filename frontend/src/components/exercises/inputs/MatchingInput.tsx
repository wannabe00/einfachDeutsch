import { useState } from "react"

import type { ExercisePayload } from "@/types"
import { cn } from "@/lib/utils"

/**
 * Tap an item on the left, then its partner on the right. Tapping a matched
 * left item again lets you change its partner. Right-hand items can repeat
 * (e.g. several nouns all matching "der"), so they never get used up.
 */
export function MatchingInput({
  payload,
  value,
  onChange,
  disabled,
}: {
  payload: ExercisePayload
  value: Record<string, string>
  onChange: (v: Record<string, string>) => void
  disabled: boolean
}) {
  const [selectedLeft, setSelectedLeft] = useState<string | null>(null)
  const left = payload.left ?? []
  const right = payload.right ?? []

  function pickRight(r: string) {
    if (!selectedLeft) return
    onChange({ ...value, [selectedLeft]: r })
    setSelectedLeft(null)
  }

  return (
    <div className="grid grid-cols-2 gap-3">
      <div className="flex flex-col gap-2">
        {left.map((l) => (
          <button
            key={l}
            type="button"
            disabled={disabled}
            onClick={() => setSelectedLeft(selectedLeft === l ? null : l)}
            className={cn(
              "flex flex-col items-start rounded-lg border px-3 py-2 text-left text-sm transition-colors",
              selectedLeft === l
                ? "border-primary bg-primary/10"
                : "border-border bg-background hover:bg-surface-2",
            )}
          >
            <span>{l}</span>
            {value[l] && <span className="mt-0.5 text-xs text-muted-foreground">→ {value[l]}</span>}
          </button>
        ))}
      </div>
      <div className="flex flex-col gap-2">
        {right.map((r) => (
          <button
            key={r}
            type="button"
            disabled={disabled || !selectedLeft}
            onClick={() => pickRight(r)}
            className={cn(
              "rounded-lg border border-border bg-background px-3 py-2 text-left text-sm transition-colors",
              selectedLeft ? "hover:bg-surface-2" : "text-muted-foreground",
            )}
          >
            {r}
          </button>
        ))}
      </div>
    </div>
  )
}
