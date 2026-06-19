import type { ExercisePayload } from "@/types"
import { cn } from "@/lib/utils"

/* ---- Multiple choice ------------------------------------------------- */
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

/* ---- Sentence order -------------------------------------------------- */
export function SentenceOrderInput({
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
  const tokens = payload.tokens ?? []
  // Remaining = tokens minus those already placed (by position-aware count).
  const used = [...value]
  const remaining: { tok: string; idx: number }[] = []
  tokens.forEach((tok, idx) => {
    const pos = used.indexOf(tok)
    if (pos >= 0) used.splice(pos, 1)
    else remaining.push({ tok, idx })
  })

  return (
    <div className="flex flex-col gap-3">
      <div className="flex min-h-[44px] flex-wrap gap-2 rounded-lg border border-dashed border-border bg-background p-2">
        {value.length === 0 && (
          <span className="self-center text-sm text-muted-foreground">
            Tap the words below in order…
          </span>
        )}
        {value.map((tok, i) => (
          <button
            key={`${tok}-${i}`}
            type="button"
            disabled={disabled}
            onClick={() => onChange(value.filter((_, j) => j !== i))}
            className="rounded-md bg-accent px-2.5 py-1 text-sm text-accent-foreground"
          >
            {tok}
          </button>
        ))}
      </div>
      <div className="flex flex-wrap gap-2">
        {remaining.map(({ tok, idx }) => (
          <button
            key={`${tok}-${idx}`}
            type="button"
            disabled={disabled}
            onClick={() => onChange([...value, tok])}
            className="rounded-md border border-border bg-surface px-2.5 py-1 text-sm text-foreground hover:border-accent"
          >
            {tok}
          </button>
        ))}
      </div>
    </div>
  )
}

/* ---- Matching -------------------------------------------------------- */
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

/* ---- Word bank ------------------------------------------------------- */
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
