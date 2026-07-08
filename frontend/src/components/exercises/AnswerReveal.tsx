import { Sparkles } from "lucide-react"

import type { AttemptResult } from "@/types"
import { cn } from "@/lib/utils"

/** Renders one correct-answer value (string, list, or matching map) as text. */
function renderReveal(value: AttemptResult["correct_answer"]): string {
  if (typeof value === "string") return value
  if (Array.isArray(value)) return value.join(" · ")
  return Object.entries(value)
    .map(([l, r]) => `${l} → ${r}`)
    .join(", ")
}

/** The post-submit feedback block: correct/incorrect verdict, the correct
    answer (when wrong), the explanation, and optional AI tutor feedback. */
export function AnswerReveal({
  result,
  aiFeedback,
  aiPending,
}: {
  result: AttemptResult
  aiFeedback: string
  aiPending: boolean
}) {
  return (
    <div className="mt-4 flex flex-col gap-1.5">
      <p
        className={cn(
          "text-sm font-medium",
          result.is_correct ? "text-[hsl(var(--success))]" : "text-[hsl(var(--danger))]",
        )}
      >
        {result.is_correct ? "✓ Correct!" : "✗ Not quite."}
      </p>
      {!result.is_correct && (
        <p className="text-sm text-foreground">
          Answer:{" "}
          <span className="font-semibold">{renderReveal(result.correct_answer)}</span>
        </p>
      )}
      {result.explanation && (
        <p className="text-sm text-muted-foreground">{result.explanation}</p>
      )}

      {aiPending && (
        <p className="mt-1 flex items-center gap-1.5 text-sm text-muted-foreground">
          <Sparkles className="size-3.5 animate-pulse" /> AI feedback…
        </p>
      )}
      {aiFeedback && (
        <div className="mt-2 rounded-lg border border-accent/30 bg-accent/5 px-3 py-2">
          <p className="mb-1 flex items-center gap-1.5 text-xs font-medium text-accent">
            <Sparkles className="size-3.5" /> AI tutor
          </p>
          <p className="text-sm text-foreground">{aiFeedback}</p>
        </div>
      )}
    </div>
  )
}
