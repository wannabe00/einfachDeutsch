import { Check, X } from "lucide-react"

import type { AnswerResult, PartContent, PartSolution } from "@/types"
import { cn } from "@/lib/utils"

/*
 * The verdict after checking an exercise, shared by the lesson player and
 * practice sets: right or wrong, how many parts were right, and the answer to
 * each part that wasn't.
 */
function formatSolution(solution: PartSolution, type: string): string {
  if (!Array.isArray(solution)) return solution
  if (solution.some(Array.isArray)) {
    return (solution as [string, string][]).map(([l, r]) => `${l} = ${r}`).join(", ")
  }
  // Word-bank answers are separate gap fillers; sentence order is one sentence.
  return (solution as string[]).join(type === "word_bank" ? ", " : " ")
}

/** "Answer: …" lines for what was wrong: the whole answer for a single
    exercise, or one line per wrong part of a group. */
function wrongAnswers(feedback: AnswerResult, content: PartContent): string[] {
  if (content.type !== "group") {
    return [formatSolution(feedback.solution as PartSolution, content.type)]
  }
  const parts = content.payload.parts ?? []
  const solutions = feedback.solution as PartSolution[]
  return parts.flatMap((part, i) =>
    feedback.parts[i] ? [] : [`${i + 1}. ${formatSolution(solutions[i], part.type)}`],
  )
}

export function AnswerFeedback({ feedback, content }: { feedback: AnswerResult; content: PartContent }) {
  const right = feedback.parts.filter(Boolean).length
  const verdict = feedback.correct
    ? "Richtig!"
    : feedback.parts.length > 1
      ? `${right} of ${feedback.parts.length} right`
      : "Not quite"
  return (
    <div
      className={cn(
        "mt-5 rounded-2xl p-4 animate-in fade-in-0 slide-in-from-bottom-1 duration-200",
        feedback.correct
          ? "bg-[hsl(var(--success)/0.12)] text-[hsl(var(--success))]"
          : "bg-[hsl(var(--danger)/0.12)] text-[hsl(var(--danger))]",
      )}
    >
      <p className="flex items-center gap-2 font-semibold">
        {feedback.correct ? <Check className="size-4" /> : <X className="size-4" />}
        {verdict}
      </p>
      {!feedback.correct &&
        wrongAnswers(feedback, content).map((line) => (
          <p key={line} className="mt-1 text-sm text-foreground">
            Answer: <span className="font-semibold">{line}</span>
          </p>
        ))}
      {feedback.explanation && (
        <p className="mt-1 text-sm text-muted-foreground">{feedback.explanation}</p>
      )}
    </div>
  )
}
