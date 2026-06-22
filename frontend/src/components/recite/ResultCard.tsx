import { Check, RotateCcw, X } from "lucide-react"

import type { RecitationResult } from "@/types"
import { Button } from "@/components/ui/button"

/** Step 3 — the graded feedback card (coverage, covered/missed, grammar,
    pronunciation, transcript) + "Try another". */
export function ResultCard({
  result,
  onReset,
}: {
  result: RecitationResult
  onReset: () => void
}) {
  return (
    <div className="mt-6 flex flex-col gap-4">
      <div className="rounded-xl border border-border bg-surface p-5">
        <div className="flex items-center justify-between">
          <h2 className="text-base font-semibold">Your feedback</h2>
          {result.coverage_score !== null && (
            <span className="text-2xl font-bold text-accent">{result.coverage_score}%</span>
          )}
        </div>
        {result.summary && (
          <p className="mt-2 text-sm text-muted-foreground">{result.summary}</p>
        )}
      </div>

      {result.covered.length > 0 && (
        <FeedbackList title="Covered" items={result.covered} tone="success" />
      )}
      {result.missed.length > 0 && (
        <FeedbackList title="Missed" items={result.missed} tone="danger" />
      )}

      {result.grammar_errors.length > 0 && (
        <div className="rounded-xl border border-border bg-surface p-5">
          <h3 className="mb-3 text-sm font-semibold">Grammar</h3>
          <ul className="flex flex-col gap-2">
            {result.grammar_errors.map((g, i) => (
              <li key={i} className="text-sm">
                <span className="rounded bg-muted px-1.5 py-0.5 text-xs text-muted-foreground">
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

      <details className="rounded-xl border border-border bg-surface p-5">
        <summary className="cursor-pointer text-sm font-medium">
          What we heard (transcript)
        </summary>
        <p className="mt-2 whitespace-pre-wrap text-sm text-muted-foreground">
          {result.transcript || "—"}
        </p>
      </details>

      <Button variant="secondary" className="self-start" onClick={onReset}>
        <RotateCcw className="mr-2 size-4" /> Try another
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
    <div className="rounded-xl border border-border bg-surface p-5">
      <h3 className="mb-3 text-sm font-semibold">{title}</h3>
      <ul className="flex flex-col gap-1.5">
        {items.map((it, i) => (
          <li key={i} className="flex items-start gap-2 text-sm">
            {Icon && <Icon className={`mt-0.5 size-4 shrink-0 ${color}`} />}
            <span>{it}</span>
          </li>
        ))}
      </ul>
    </div>
  )
}
