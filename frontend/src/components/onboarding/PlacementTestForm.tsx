import { useEffect, useState } from "react"

import type { PlacementQuestion, PlacementTest } from "@/types"
import { Button } from "@/components/ui/button"
import { cn } from "@/lib/utils"

const mmss = (s: number) => `${Math.floor(s / 60)}:${String(s % 60).padStart(2, "0")}`

/**
 * The placement test: shuffled grammar MCQs + reading passages (each with its
 * own MCQs) + one short free-write. Soft timer (counts up, never auto-submits).
 * Submit is enabled once every multiple-choice question is answered (the
 * free-write is optional). Answers are reported as a single id→choice map.
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
  const [answers, setAnswers] = useState<Record<string, string>>({})
  const [writing, setWriting] = useState("")
  const [elapsed, setElapsed] = useState(0)

  useEffect(() => {
    const id = window.setInterval(() => setElapsed((e) => e + 1), 1000)
    return () => window.clearInterval(id)
  }, [])

  const mcqIds = [
    ...test.grammar.map((q) => q.id),
    ...test.reading.flatMap((p) => p.questions.map((q) => q.id)),
  ]
  const answered = mcqIds.filter((id) => answers[id] !== undefined).length
  const allAnswered = answered === mcqIds.length

  function pick(id: string, option: string) {
    setAnswers((a) => ({ ...a, [id]: option }))
  }

  return (
    <div className="mt-8 flex flex-col gap-6 rounded-xl border border-border bg-surface p-6">
      <div className="flex flex-wrap items-center justify-between gap-2">
        <div>
          <h2 className="text-lg font-semibold">Placement test</h2>
          <p className="text-sm text-muted-foreground">
            About 12–15 minutes. Pick the best answer; skip nothing.
          </p>
        </div>
        <div className="text-right text-xs text-muted-foreground tabular-nums">
          <div>⏱ {mmss(elapsed)}</div>
          <div>
            {answered}/{mcqIds.length} answered
          </div>
        </div>
      </div>

      {/* Grammar & vocabulary */}
      <div className="flex flex-col gap-5">
        <h3 className="text-xs font-semibold uppercase tracking-wide text-muted-foreground">
          Grammar & vocabulary
        </h3>
        {test.grammar.map((q, i) => (
          <Question key={q.id} q={q} index={i + 1} chosen={answers[q.id]} onPick={pick} />
        ))}
      </div>

      {/* Reading passages */}
      {test.reading.map((passage) => (
        <div key={passage.id} className="flex flex-col gap-4 border-t border-border pt-5">
          <div>
            <h3 className="text-xs font-semibold uppercase tracking-wide text-muted-foreground">
              Lesen — {passage.title}
            </h3>
            <p className="mt-2 whitespace-pre-wrap rounded-lg bg-background p-3 text-sm leading-relaxed">
              {passage.text}
            </p>
          </div>
          {passage.questions.map((q, i) => (
            <Question key={q.id} q={q} index={i + 1} chosen={answers[q.id]} onPick={pick} />
          ))}
        </div>
      ))}

      {/* Free-write */}
      <div className="flex flex-col gap-2 border-t border-border pt-5">
        <h3 className="text-xs font-semibold uppercase tracking-wide text-muted-foreground">
          Schreiben
        </h3>
        <label className="text-sm" htmlFor="placement-writing">
          {test.writing.prompt}
        </label>
        <textarea
          id="placement-writing"
          value={writing}
          onChange={(e) => setWriting(e.target.value)}
          rows={3}
          placeholder="Auf Deutsch…"
          className="w-full rounded-lg border border-border bg-background p-3 text-sm"
        />
      </div>

      <Button
        disabled={!allAnswered || submitting}
        onClick={() => onSubmit(answers, writing)}
      >
        {submitting ? "Scoring…" : "See my level"}
      </Button>
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
