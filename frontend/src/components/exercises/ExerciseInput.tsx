import { Check, Volume2, X } from "lucide-react"

import type { PartContent, PartSolution } from "@/types"
import { cn } from "@/lib/utils"
import { Input } from "@/components/ui/input"
import { MatchingInput, WordBankInput } from "@/components/exercises/inputs"
import { AudioClip } from "@/components/exercises/AudioClip"
import { canSpeak, decodeSpeech, speak } from "@/lib/speech"

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
      <div className="flex flex-col gap-4">
        {content.payload.audio && <AudioClip audio={content.payload.audio} free={results !== undefined} />}
        {content.payload.context && <ContextText text={content.payload.context} />}
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
      </div>
    )
  }

  if (content.type === "multiple_choice") {
    const picked = typeof value === "string" ? value : null
    const right = typeof solution === "string" ? solution : null
    return (
      <div className="grid gap-2">
        {content.payload.context && <ContextText text={content.payload.context} />}
        {content.payload.audio && <AudioClip audio={content.payload.audio} free={verdict !== undefined} />}
        {content.payload.say && <ListenButtons say={content.payload.say} />}
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

  if (content.type === "error_spot") {
    const picked = typeof value === "number" ? value : null
    const wrongIndex = Array.isArray(solution) ? Number(solution[0]) : null
    return (
      <div className="flex flex-wrap gap-2">
        {(content.payload.tokens ?? []).map((token, i) => {
          const checked = verdict !== undefined
          const isMistake = checked && i === (wrongIndex ?? (verdict ? picked : null))
          const isWrongPick = checked && i === picked && !verdict
          return (
            <button
              key={`${token}-${i}`}
              type="button"
              disabled={disabled}
              aria-pressed={picked === i}
              onClick={() => onChange(i)}
              className={cn(
                "min-h-[44px] rounded-xl border-2 px-3.5 py-2 text-[15px] font-medium transition-colors",
                isMistake
                  ? RIGHT
                  : isWrongPick
                    ? WRONG
                    : picked === i
                      ? CHOSEN
                      : "border-transparent bg-surface-2 hover:bg-border",
              )}
            >
              {token}
            </button>
          )
        })}
      </div>
    )
  }

  if (content.type === "dictation") {
    return (
      <div className="flex flex-col gap-3">
        {content.payload.say && <ListenButtons say={content.payload.say} />}
        <TextAnswer
          value={value}
          onChange={onChange}
          disabled={disabled}
          autoFocus={autoFocus}
          onSubmit={onSubmit}
          verdict={verdict}
          placeholder="Write what you hear…"
        />
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
    <TextAnswer
      value={value}
      onChange={onChange}
      disabled={disabled}
      autoFocus={autoFocus}
      onSubmit={onSubmit}
      verdict={verdict}
    />
  )
}

function TextAnswer({
  value,
  onChange,
  disabled,
  autoFocus,
  onSubmit,
  verdict,
  placeholder = "Your answer…",
}: {
  value: unknown
  onChange: (value: unknown) => void
  disabled: boolean
  autoFocus: boolean
  onSubmit?: () => void
  verdict?: boolean
  placeholder?: string
}) {
  return (
    <Input
      autoFocus={autoFocus}
      value={typeof value === "string" ? value : ""}
      disabled={disabled}
      placeholder={placeholder}
      autoCapitalize="off"
      autoCorrect="off"
      spellCheck={false}
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

/** A dialogue (one line per speaker) or a short reading text. */
function ContextText({ text }: { text: string }) {
  return (
    <div className="whitespace-pre-line rounded-2xl bg-surface-2/70 p-4 text-[15px] leading-relaxed">
      {text}
    </div>
  )
}

/** Play the German (and play it slowly) with the browser's speech synthesis. */
function ListenButtons({ say }: { say: string }) {
  if (!canSpeak()) {
    return <p className="text-sm text-muted-foreground">This browser can't play audio. Skip this one.</p>
  }
  const text = decodeSpeech(say)
  return (
    <div className="flex gap-2">
      <button
        type="button"
        onClick={() => speak(text)}
        className="inline-flex h-12 items-center gap-2 rounded-full bg-primary px-5 font-semibold text-primary-foreground transition hover:brightness-110 active:scale-[0.97]"
      >
        <Volume2 className="size-5" aria-hidden="true" /> Listen
      </button>
      <button
        type="button"
        onClick={() => speak(text, true)}
        className="inline-flex h-12 items-center rounded-full bg-surface-2 px-5 font-semibold transition-colors hover:bg-border"
      >
        Slower
      </button>
    </div>
  )
}
