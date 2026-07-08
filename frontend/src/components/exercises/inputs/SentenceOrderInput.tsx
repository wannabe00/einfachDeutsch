import type { ExercisePayload } from "@/types"

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
  // Remaining = tokens minus those already placed (position-aware count).
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
