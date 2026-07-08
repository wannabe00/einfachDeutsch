import type { ExercisePayload } from "@/types"
import { cn } from "@/lib/utils"

export function MultipleChoiceInput({
  payload,
  value,
  onChange,
  disabled,
}: {
  payload: ExercisePayload
  value: string
  onChange: (v: string) => void
  disabled: boolean
}) {
  return (
    <div className="flex flex-col gap-2">
      {(payload.options ?? []).map((opt) => (
        <button
          key={opt}
          type="button"
          disabled={disabled}
          onClick={() => onChange(opt)}
          className={cn(
            "rounded-lg border px-4 py-2.5 text-left text-sm transition-colors",
            value === opt
              ? "border-accent bg-accent/10 text-foreground"
              : "border-border bg-background text-foreground hover:border-accent",
          )}
        >
          {opt}
        </button>
      ))}
    </div>
  )
}
