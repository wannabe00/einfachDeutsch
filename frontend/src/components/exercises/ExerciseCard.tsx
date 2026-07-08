import { type FormEvent } from "react"

import type { Exercise } from "@/types"
import { exerciseTypeLabel } from "@/lib/labels"
import { useExerciseAttempt } from "@/hooks/useExerciseAttempt"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { cn } from "@/lib/utils"
import {
  MatchingInput,
  MultipleChoiceInput,
  SentenceOrderInput,
  WordBankInput,
} from "./inputs"
import { AnswerReveal } from "./AnswerReveal"

/** One exercise: renders the type-specific input, grades it via
    `useExerciseAttempt`, then shows the reveal. Answer logic lives in the hook;
    the per-type inputs live in `./inputs`. */
export function ExerciseCard({ exercise }: { exercise: Exercise }) {
  const a = useExerciseAttempt(exercise)
  const disabled = !!a.result

  function handleSubmit(e?: FormEvent) {
    e?.preventDefault()
    a.submit()
  }

  const borderClass = a.result
    ? a.result.is_correct
      ? "border-success"
      : "border-danger"
    : "border-border"

  return (
    <article
      className={cn(
        "rounded-xl border-2 bg-surface p-5 shadow-sm transition-colors",
        borderClass,
      )}
    >
      <div className="mb-3 flex items-start justify-between gap-3">
        <p className="text-base font-medium text-foreground">{exercise.prompt}</p>
        <span className="shrink-0 rounded-full bg-muted px-2.5 py-0.5 text-xs font-medium text-muted-foreground">
          {exerciseTypeLabel(exercise.exercise_type)}
        </span>
      </div>

      {exercise.hint && !a.result && (
        <p className="mb-3 text-sm text-muted-foreground">Hint: {exercise.hint}</p>
      )}

      {a.isSimple ? (
        <form onSubmit={handleSubmit} className="flex flex-wrap gap-2">
          <Input
            value={a.text}
            onChange={(e) => a.setText(e.target.value)}
            placeholder="Your answer in German…"
            aria-label="Your answer"
            disabled={disabled}
            className="w-72"
          />
          {!a.result && (
            <Button type="submit" disabled={a.submitting}>
              {a.submitting ? "Checking…" : "Submit"}
            </Button>
          )}
        </form>
      ) : (
        <div className="flex flex-col gap-3">
          {exercise.exercise_type === "multiple_choice" && (
            <MultipleChoiceInput
              payload={exercise.payload}
              value={a.text}
              onChange={a.setText}
              disabled={disabled}
            />
          )}
          {exercise.exercise_type === "sentence_order" && (
            <SentenceOrderInput
              payload={exercise.payload}
              value={a.list}
              onChange={a.setList}
              disabled={disabled}
            />
          )}
          {exercise.exercise_type === "word_bank" && (
            <WordBankInput
              payload={exercise.payload}
              value={a.list}
              onChange={a.setList}
              disabled={disabled}
            />
          )}
          {exercise.exercise_type === "matching" && (
            <MatchingInput
              payload={exercise.payload}
              value={a.map}
              onChange={a.setMap}
              disabled={disabled}
              selectedLeft={a.selectedLeft}
              setSelectedLeft={a.setSelectedLeft}
            />
          )}
          {!a.result && (
            <div>
              <Button onClick={() => handleSubmit()} disabled={a.submitting}>
                {a.submitting ? "Checking…" : "Submit"}
              </Button>
            </div>
          )}
        </div>
      )}

      {a.result && (
        <AnswerReveal result={a.result} aiFeedback={a.aiFeedback} aiPending={a.aiPending} />
      )}
    </article>
  )
}
