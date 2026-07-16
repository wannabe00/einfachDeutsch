import type { ExerciseContent } from "@/types"
import { cn } from "@/lib/utils"
import { Input } from "@/components/ui/input"

/*
 * The answer control for one exercise — shared by the lesson player (23.5) and
 * the level exam (23.14) so the two can't drift apart. Purely presentational:
 * it owns no answer state and does no grading (that's server-side).
 */
export function ExerciseInput({
  content,
  value,
  onChange,
  disabled = false,
  accent = "hsl(var(--brand))",
  autoFocus = false,
  onSubmit,
}: {
  content: ExerciseContent
  value: unknown
  onChange: (value: unknown) => void
  disabled?: boolean
  accent?: string
  autoFocus?: boolean
  /** Enter on a text answer (e.g. "check"/"next"). */
  onSubmit?: () => void
}) {
  if (content.type === "multiple_choice") {
    const picked = typeof value === "string" ? value : null
    return (
      <div className="mt-5 grid gap-2">
        {(content.payload.options ?? []).map((option) => (
          <button
            key={option}
            type="button"
            disabled={disabled}
            onClick={() => onChange(option)}
            className={cn(
              "rounded-xl border-2 px-4 py-3 text-left font-medium transition-colors",
              picked === option
                ? "border-transparent text-white"
                : "border-border hover:border-white/30",
            )}
            style={picked === option ? { background: accent } : undefined}
          >
            {option}
          </button>
        ))}
      </div>
    )
  }

  if (content.type === "sentence_order") {
    const order = Array.isArray(value) ? (value as string[]) : []
    const tokens = content.payload.tokens ?? []
    // A token stays in the pool until every duplicate of it has been used.
    const remaining = tokens.filter(
      (t) => order.filter((o) => o === t).length < tokens.filter((x) => x === t).length,
    )
    return (
      <div className="mt-5">
        <div className="min-h-14 rounded-xl border-2 border-dashed border-border p-2">
          <div className="flex flex-wrap gap-2">
            {order.map((token, i) => (
              <button
                key={`${token}-${i}`}
                type="button"
                disabled={disabled}
                onClick={() => onChange(order.filter((_, j) => j !== i))}
                className="rounded-lg bg-surface-2 px-3 py-1.5 text-sm font-medium ring-1 ring-white/10"
              >
                {token}
              </button>
            ))}
          </div>
        </div>
        <div className="mt-3 flex flex-wrap gap-2">
          {remaining.map((token, i) => (
            <button
              key={`${token}-pool-${i}`}
              type="button"
              disabled={disabled}
              onClick={() => onChange([...order, token])}
              className="rounded-lg border border-border px-3 py-1.5 text-sm font-medium transition-colors hover:border-white/30"
            >
              {token}
            </button>
          ))}
        </div>
      </div>
    )
  }

  return (
    <Input
      className="mt-5"
      autoFocus={autoFocus}
      value={typeof value === "string" ? value : ""}
      disabled={disabled}
      placeholder="Your answer…"
      onChange={(e) => onChange(e.target.value)}
      onKeyDown={(e) => {
        if (e.key === "Enter") onSubmit?.()
      }}
    />
  )
}
