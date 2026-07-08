import type { ExercisePayload } from "@/types"
import { cn } from "@/lib/utils"

export function WordBankInput({
  payload,
  value,
  onChange,
  disabled,
}: {
  payload: ExercisePayload
  value: string[]
  onChange: (v: string[]) => void
  disabled: boolean
}) {
  const parts = (payload.text ?? "").split("___")
  const blanks = parts.length - 1
  const bank = payload.bank ?? []

  function fillNext(word: string) {
    if (value.length >= blanks) return
    onChange([...value, word])
  }

  return (
    <div className="flex flex-col gap-3">
      <p className="text-sm leading-7 text-foreground">
        {parts.map((part, i) => (
          <span key={i}>
            {part}
            {i < blanks && (
              <button
                type="button"
                disabled={disabled}
                onClick={() => onChange(value.filter((_, j) => j !== i))}
                className={cn(
                  "mx-1 inline-flex min-w-16 justify-center rounded border-b-2 px-2 py-0.5 align-baseline",
                  value[i]
                    ? "border-accent bg-accent/10 text-foreground"
                    : "border-muted-foreground text-muted-foreground",
                )}
              >
                {value[i] ?? "____"}
              </button>
            )}
          </span>
        ))}
      </p>
      <div className="flex flex-wrap gap-2">
        {bank.map((w, i) => (
          <button
            key={`${w}-${i}`}
            type="button"
            disabled={disabled || value.length >= blanks}
            onClick={() => fillNext(w)}
            className="rounded-md border border-border bg-surface px-2.5 py-1 text-sm text-foreground hover:border-accent disabled:opacity-50"
          >
            {w}
          </button>
        ))}
      </div>
    </div>
  )
}
