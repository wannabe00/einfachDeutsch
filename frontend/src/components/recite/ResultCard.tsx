import { Check, RotateCcw, X } from "lucide-react"

import type { RecitationResult } from "@/types"
import { Button } from "@/components/ui/button"
import { ProgressRing } from "@/components/lektion/ProgressRing"

/** Step 3: the feedback (coverage, covered and missed points, grammar,
    pronunciation, transcript) and a "Try another" button. */
export function ResultCard({
  result,
  onReset,
}: {
  result: RecitationResult
  onReset: () => void
}) {
  return (
    <div className="flex flex-col gap-4">
      <div className="flex flex-col gap-5 rounded-[24px] bg-surface p-6 shadow-card sm:flex-row sm:items-center sm:p-7">
        {result.coverage_score !== null && (
          <div className="relative flex size-24 shrink-0 items-center justify-center">
            <ProgressRing
              pct={result.coverage_score / 100}
              color="hsl(var(--primary))"
              size={96}
              stroke={9}
              label={`${result.coverage_score}% covered`}
            />
            <span className="absolute font-grotesk text-2xl font-extrabold tabular-nums">
              {result.coverage_score}%
            </span>
          </div>
        )}
        <div className="min-w-0">
          <h2 className="text-2xl font-extrabold">Your feedback</h2>
          {result.summary && <p className="mt-1 text-muted-foreground">{result.summary}</p>}
        </div>
      </div>

      {result.covered.length > 0 && (
        <FeedbackList title="Covered" items={result.covered} tone="success" />
      )}
      {result.missed.length > 0 && (
        <FeedbackList title="Missed" items={result.missed} tone="danger" />
      )}

      {result.grammar_errors.length > 0 && (
        <div className="rounded-[24px] bg-surface p-6 shadow-card">
          <h3 className="mb-3 text-lg font-bold">Grammar</h3>
          <ul className="flex flex-col gap-2.5">
            {result.grammar_errors.map((g, i) => (
              <li key={i} className="text-[15px]">
                <span className="rounded-full bg-surface-2 px-2.5 py-0.5 text-xs font-semibold text-muted-foreground">
                  {g.type}
                </span>{" "}
                <span className="text-[hsl(var(--danger))] line-through">{g.error}</span> →{" "}
                <span className="text-[hsl(var(--success))]">{g.correction}</span>
              </li>
            ))}
          </ul>
        </div>
      )}

      {result.pronunciation_notes.length > 0 && (
        <FeedbackList title="Pronunciation to watch" items={result.pronunciation_notes} tone="muted" />
      )}

      <details className="rounded-[24px] bg-surface p-6 shadow-card">
        <summary className="cursor-pointer font-semibold">
          What we heard (transcript)
        </summary>
        <p className="mt-3 whitespace-pre-wrap leading-relaxed text-muted-foreground">
          {result.transcript || "No speech was picked up."}
        </p>
      </details>

      <Button size="lg" className="self-start" onClick={onReset}>
        <RotateCcw /> Try another
      </Button>
    </div>
  )
}

function FeedbackList({
  title,
  items,
  tone,
}: {
  title: string
  items: string[]
  tone: "success" | "danger" | "muted"
}) {
  const Icon = tone === "success" ? Check : tone === "danger" ? X : null
  const color =
    tone === "success"
      ? "text-[hsl(var(--success))]"
      : tone === "danger"
        ? "text-[hsl(var(--danger))]"
        : "text-muted-foreground"
  return (
    <div className="rounded-[24px] bg-surface p-6 shadow-card">
      <h3 className="mb-3 text-lg font-bold">{title}</h3>
      <ul className="flex flex-col gap-2">
        {items.map((it, i) => (
          <li key={i} className="flex items-start gap-2.5 text-[15px]">
            {Icon && <Icon className={`mt-0.5 size-4 shrink-0 ${color}`} />}
            <span>{it}</span>
          </li>
        ))}
      </ul>
    </div>
  )
}
