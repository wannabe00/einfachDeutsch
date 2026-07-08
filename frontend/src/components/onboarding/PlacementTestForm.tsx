import { useEffect, useMemo, useState } from "react"

import type { PlacementQuestion, PlacementTest, ReadingPassage } from "@/types"
import { Button } from "@/components/ui/button"
import { cn } from "@/lib/utils"

const mmss = (s: number) => `${Math.floor(s / 60)}:${String(s % 60).padStart(2, "0")}`
const GRAMMAR_PER_STEP = 5

type Step =
  | { kind: "grammar"; label: string; questions: PlacementQuestion[] }
  | { kind: "reading"; label: string; passage: ReadingPassage }
  | { kind: "writing"; label: string }

/** Break the test into one screen per step: grammar in groups of 5, then one
    screen per reading passage, then the free-write. */
function buildSteps(test: PlacementTest): Step[] {
  const steps: Step[] = []
  const groups: PlacementQuestion[][] = []
  for (let i = 0; i < test.grammar.length; i += GRAMMAR_PER_STEP) {
    groups.push(test.grammar.slice(i, i + GRAMMAR_PER_STEP))
  }
  groups.forEach((questions, i) =>
    steps.push({ kind: "grammar", label: `Grammatik ${i + 1}/${groups.length}`, questions }),
  )
  test.reading.forEach((passage, i) =>
    steps.push({ kind: "reading", label: `Lesen ${i + 1}/${test.reading.length}`, passage }),
  )
  steps.push({ kind: "writing", label: "Schreiben" })
  return steps
}

/**
 * Paginated placement test: one step per screen with Previous/Next. Answers are
 * kept across steps; the free-write is the last step. Soft count-up timer (never
 * auto-submits). Submit (on the last step) is enabled once every MCQ is answered.
 */
export function PlacementTestForm({
  test,
  submitting,
  onSubmit,
}: {
  test: PlacementTest
  submitting: boolean
  onSubmit: (answers: Record<string, string>, writing: string) => void
}) {
  const steps = useMemo(() => buildSteps(test), [test])
  const [stepIndex, setStepIndex] = useState(0)
  const [answers, setAnswers] = useState<Record<string, string>>({})
  const [writing, setWriting] = useState("")
  const [elapsed, setElapsed] = useState(0)

  // Count up while taking the test; pause once grading starts (B4).
  useEffect(() => {
    if (submitting) return
    const id = window.setInterval(() => setElapsed((e) => e + 1), 1000)
    return () => window.clearInterval(id)
  }, [submitting])

  const mcqIds = useMemo(
    () => [
      ...test.grammar.map((q) => q.id),
      ...test.reading.flatMap((p) => p.questions.map((q) => q.id)),
    ],
    [test],
  )
  const answered = mcqIds.filter((id) => answers[id] !== undefined).length
  const remaining = mcqIds.length - answered

  const step = steps[stepIndex]
  const isLast = stepIndex === steps.length - 1

  function pick(id: string, option: string) {
    setAnswers((a) => ({ ...a, [id]: option }))
  }

  function go(next: number) {
    setStepIndex(next)
    window.scrollTo({ top: 0, behavior: "smooth" })
  }

  return (
    <div className="mt-8 flex flex-col gap-6 rounded-xl border border-border bg-surface p-6">
      <div className="flex flex-wrap items-center justify-between gap-2">
        <div>
          <h2 className="text-lg font-semibold">Placement test</h2>
          <p className="text-sm text-muted-foreground">
            Step {stepIndex + 1} of {steps.length} — {step.label}
          </p>
        </div>
        <div className="text-right text-xs text-muted-foreground tabular-nums">
          <div>⏱ {mmss(elapsed)}</div>
          <div>
            {answered}/{mcqIds.length} answered
          </div>
        </div>
      </div>

      {step.kind === "grammar" && (
        <div className="flex flex-col gap-5">
          {step.questions.map((q, i) => (
            <Question
              key={q.id}
              q={q}
              index={stepIndex * GRAMMAR_PER_STEP + i + 1}
              chosen={answers[q.id]}
              onPick={pick}
            />
          ))}
        </div>
      )}

      {step.kind === "reading" && (
        <div className="flex flex-col gap-4">
          <div>
            <h3 className="text-xs font-semibold uppercase tracking-wide text-muted-foreground">
              {step.passage.title}
            </h3>
            <p className="mt-2 whitespace-pre-wrap rounded-lg bg-background p-3 text-sm leading-relaxed">
              {step.passage.text}
            </p>
          </div>
          {step.passage.questions.map((q, i) => (
            <Question key={q.id} q={q} index={i + 1} chosen={answers[q.id]} onPick={pick} />
          ))}
        </div>
      )}

      {step.kind === "writing" && (
        <div className="flex flex-col gap-2">
          <label className="text-sm" htmlFor="placement-writing">
            {test.writing.prompt}
          </label>
          <textarea
            id="placement-writing"
            value={writing}
            onChange={(e) => setWriting(e.target.value)}
            rows={4}
            placeholder="Auf Deutsch…"
            className="w-full rounded-lg border border-border bg-background p-3 text-sm"
          />
          {remaining > 0 && (
            <p className="text-xs text-[hsl(var(--danger))]">
              {remaining} question{remaining === 1 ? "" : "s"} still unanswered — go back and
              finish them to see your level.
            </p>
          )}
        </div>
      )}

      <div className="flex items-center justify-between gap-2 border-t border-border pt-4">
        <Button variant="outline" disabled={stepIndex === 0} onClick={() => go(stepIndex - 1)}>
          ← Previous
        </Button>
        {isLast ? (
          <Button
            disabled={remaining > 0 || submitting}
            onClick={() => onSubmit(answers, writing)}
          >
            {submitting ? "Scoring…" : "See my level"}
          </Button>
        ) : (
          <Button onClick={() => go(stepIndex + 1)}>Next →</Button>
        )}
      </div>
    </div>
  )
}

function Question({
  q,
  index,
  chosen,
  onPick,
}: {
  q: PlacementQuestion
  index: number
  chosen: string | undefined
  onPick: (id: string, option: string) => void
}) {
  return (
    <div>
      <p className="text-sm font-medium">
        {index}. {q.prompt}
      </p>
      <div className="mt-2 flex flex-wrap gap-2">
        {q.options.map((opt) => (
          <button
            key={opt}
            onClick={() => onPick(q.id, opt)}
            className={cn(
              "rounded-lg border px-3 py-1.5 text-sm transition-colors",
              chosen === opt
                ? "border-accent bg-accent text-accent-foreground"
                : "border-border bg-background hover:border-accent",
            )}
          >
            {opt}
          </button>
        ))}
      </div>
    </div>
  )
}
