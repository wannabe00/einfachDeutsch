import { Check, X } from "lucide-react"

import type { PartContent } from "@/types"
import { cn } from "@/lib/utils"
import { Input } from "@/components/ui/input"
import { MatchingInput, WordBankInput } from "@/components/exercises/inputs"

/*
 * The answer control for one exercise, shared by the lesson player and the level
 * exam so they behave the same. It holds no state and grades nothing; grading
 * happens on the server. A multi-part ("group") exercise renders each part with
 * this same control, and its value is a list with one answer per part.
 */
export function ExerciseInput({
  content,
  value,
  onChange,
  disabled = false,
  accent = "hsl(var(--brand))",
  autoFocus = false,
  onSubmit,
  results,
}: {
  content: PartContent
  value: unknown
  onChange: (value: unknown) => void
  disabled?: boolean
  accent?: string
  autoFocus?: boolean
  /** Enter on a text answer (e.g. "check"/"next"). */
  onSubmit?: () => void
  /** After checking a group: whether each part was right. */
  results?: boolean[]
}) {
  if (content.type === "group") {
    const parts = content.payload.parts ?? []
    const values = Array.isArray(value) ? value : []
    return (
      <ol className="flex flex-col gap-3">
        {parts.map((part, i) => {
          const result = results?.[i]
          return (
            <li
              key={i}
              className={cn(
                "rounded-xl border p-3",
                result === undefined && "border-border",
                result === true && "border-[hsl(var(--success))]",
                result === false && "border-[hsl(var(--danger))]",
              )}
            >
              <p className="flex items-baseline gap-2 text-sm font-medium">
                <span className="tabular-nums text-muted-foreground">{i + 1}.</span>
                <span className="flex-1">
                  {part.prompt}
                  {part.hint && <span className="ml-2 text-muted-foreground">({part.hint})</span>}
                </span>
                {result === true && <Check className="size-4 text-[hsl(var(--success))]" />}
                {result === false && <X className="size-4 text-[hsl(var(--danger))]" />}
              </p>
              <div className="mt-2">
                <ExerciseInput
                  content={part}
                  value={values[i]}
                  onChange={(v) => {
                    const next = parts.map((_, j) => values[j])
                    next[i] = v
                    onChange(next)
                  }}
                  disabled={disabled}
                  accent={accent}
                  autoFocus={autoFocus && i === 0}
                  onSubmit={onSubmit}
                />
              </div>
            </li>
          )
        })}
      </ol>
    )
  }

  if (content.type === "multiple_choice") {
    const picked = typeof value === "string" ? value : null
    return (
      <div className="grid gap-2">
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
      <div>
        <div className="min-h-14 rounded-xl border-2 border-dashed border-border p-2">
          <div className="flex flex-wrap gap-2">
            {order.map((token, i) => (
              <button
                key={`${token}-${i}`}
                type="button"
                disabled={disabled}
                onClick={() => onChange(order.filter((_, j) => j !== i))}
                className="rounded-lg bg-surface-2 px-3 py-1.5 text-sm font-medium ring-1 ring-border"
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

  if (content.type === "matching") {
    return (
      <MatchingInput
        payload={content.payload}
        value={value && typeof value === "object" && !Array.isArray(value) ? (value as Record<string, string>) : {}}
        onChange={onChange}
        disabled={disabled}
      />
    )
  }

  if (content.type === "word_bank") {
    return (
      <WordBankInput
        payload={content.payload}
        value={Array.isArray(value) ? (value as string[]) : []}
        onChange={onChange}
        disabled={disabled}
      />
    )
  }

  return (
    <Input
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
