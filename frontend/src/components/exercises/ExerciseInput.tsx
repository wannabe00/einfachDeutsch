import { Check, X } from "lucide-react"

import type { PartContent, PartSolution } from "@/types"
import { cn } from "@/lib/utils"
import { Input } from "@/components/ui/input"
import { MatchingInput, WordBankInput } from "@/components/exercises/inputs"

/*
 * The answer control for one exercise, shared by the lesson player, practice
 * and the level exam so they behave the same. It holds no state and grades
 * nothing; grading happens on the server. A multi-part ("group") exercise
 * renders each part with this same control, and its value is a list with one
 * answer per part.
 *
 * Colours: a chosen answer that hasn't been checked yet uses the neutral
 * "choice" colour. After checking (`results`, plus `solution` where the
 * control can show more detail), right is green and wrong is red. Green and
 * red mean nothing else here.
 */

const RIGHT = "border-[hsl(var(--success))] bg-[hsl(var(--success-bg))]"
const WRONG = "border-[hsl(var(--danger))] bg-[hsl(var(--danger-bg))]"
const CHOSEN = "border-[hsl(var(--choice))] bg-[hsl(var(--choice-bg))]"

export function ExerciseInput({
  content,
  value,
  onChange,
  disabled = false,
  autoFocus = false,
  onSubmit,
  results,
  solution,
}: {
  content: PartContent
  value: unknown
  onChange: (value: unknown) => void
  disabled?: boolean
  autoFocus?: boolean
  /** Enter on a text answer (e.g. "check"/"next"). */
  onSubmit?: () => void
  /** After checking: whether each part was right (one entry for a single exercise). */
  results?: boolean[]
  /** After checking: the solution, one per part for a group. */
  solution?: PartSolution | PartSolution[]
}) {
  const verdict = results?.[0]

  if (content.type === "group") {
    const parts = content.payload.parts ?? []
    const values = Array.isArray(value) ? value : []
    const solutions = Array.isArray(solution) ? (solution as PartSolution[]) : []
    return (
      <ol className="flex flex-col gap-3">
        {parts.map((part, i) => {
          const result = results?.[i]
          return (
            <li
              key={i}
              className={cn(
                "rounded-2xl border-2 p-3.5",
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
                  autoFocus={autoFocus && i === 0}
                  onSubmit={onSubmit}
                  results={result === undefined ? undefined : [result]}
                  solution={solutions[i]}
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
    const right = typeof solution === "string" ? solution : null
    return (
      <div className="grid gap-2">
        {(content.payload.options ?? []).map((option) => {
          const checked = verdict !== undefined
          const isRight = checked && option === (right ?? (verdict ? picked : null))
          const isWrong = checked && option === picked && !verdict
          return (
            <button
              key={option}
              type="button"
              disabled={disabled}
              onClick={() => onChange(option)}
              className={cn(
                "flex min-h-[56px] items-center justify-between gap-3 rounded-2xl border-2 px-4 py-3 text-left text-base font-semibold transition-colors",
                isRight
                  ? RIGHT
                  : isWrong
                    ? WRONG
                    : picked === option
                      ? CHOSEN
                      : "border-transparent bg-surface-2 hover:bg-border",
              )}
            >
              {option}
              {isRight && <Check className="size-5 shrink-0 text-[hsl(var(--success))]" />}
              {isWrong && <X className="size-5 shrink-0 text-[hsl(var(--danger))]" />}
            </button>
          )
        })}
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
        <div
          className={cn(
            "min-h-[60px] rounded-2xl border-2 p-2",
            verdict === true ? RIGHT : verdict === false ? WRONG : "border-dashed border-border",
          )}
        >
          <div className="flex flex-wrap gap-2">
            {order.map((token, i) => (
              <button
                key={`${token}-${i}`}
                type="button"
                disabled={disabled}
                onClick={() => onChange(order.filter((_, j) => j !== i))}
                className="min-h-[44px] rounded-xl bg-surface px-3.5 py-2 text-[15px] font-medium shadow-card ring-1 ring-border"
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
              className="min-h-[44px] rounded-xl bg-surface-2 px-3.5 py-2 text-[15px] font-medium transition-colors hover:bg-border"
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
        solution={Array.isArray(solution) ? (solution as [string, string][]) : undefined}
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
        solution={Array.isArray(solution) ? (solution as string[]) : undefined}
      />
    )
  }

  return (
    <Input
      autoFocus={autoFocus}
      value={typeof value === "string" ? value : ""}
      disabled={disabled}
      placeholder="Your answer…"
      className={cn(
        verdict === true && "border-2 border-[hsl(var(--success))] disabled:opacity-100",
        verdict === false && "border-2 border-[hsl(var(--danger))] disabled:opacity-100",
      )}
      onChange={(e) => onChange(e.target.value)}
      onKeyDown={(e) => {
        if (e.key === "Enter") onSubmit?.()
      }}
    />
  )
}
