import type { ExercisePayload } from "@/types"
import { cn } from "@/lib/utils"

export function MatchingInput({
  payload,
  value,
  onChange,
  disabled,
  selectedLeft,
  setSelectedLeft,
}: {
  payload: ExercisePayload
  value: Record<string, string>
  onChange: (v: Record<string, string>) => void
  disabled: boolean
  selectedLeft: string | null
  setSelectedLeft: (v: string | null) => void
}) {
  const left = payload.left ?? []
  const right = payload.right ?? []
  const usedRights = new Set(Object.values(value))

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
              "flex items-center justify-between rounded-lg border px-3 py-2 text-left text-sm transition-colors",
              selectedLeft === l
                ? "border-accent bg-accent/10"
                : "border-border bg-background hover:border-accent",
            )}
          >
            <span className="text-foreground">{l}</span>
            {value[l] && (
              <span className="ml-2 rounded bg-muted px-1.5 text-xs text-muted-foreground">
                {value[l]}
              </span>
            )}
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
              "rounded-lg border px-3 py-2 text-left text-sm transition-colors",
              usedRights.has(r)
                ? "border-border bg-surface text-muted-foreground"
                : "border-border bg-background text-foreground hover:border-accent",
              !selectedLeft && "opacity-60",
            )}
          >
            {r}
          </button>
        ))}
      </div>
    </div>
  )
}
