import { useState, type FormEvent } from "react"
import { useMutation } from "@tanstack/react-query"

import { attemptExercise, type UserAnswer } from "@/api/exercises"
import { aiCheckAnswer } from "@/api/ai"
import { useGuestLimit } from "@/contexts/GuestLimitContext"
import type { Exercise, AttemptResult } from "@/types"
import { exerciseTypeLabel } from "@/lib/labels"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { cn } from "@/lib/utils"
import { Sparkles } from "lucide-react"
import {
  MultipleChoiceInput,
  SentenceOrderInput,
  MatchingInput,
  WordBankInput,
} from "./InteractiveInputs"

interface ExerciseCardProps {
  exercise: Exercise
}

const SIMPLE_TYPES = ["translation", "fill_blank", "article", "conjugation", "free_text"]

function answerReady(type: string, ans: UserAnswer): boolean {
  if (typeof ans === "string") return ans.trim().length > 0
  if (Array.isArray(ans)) return ans.length > 0
  return Object.keys(ans).length > 0
}

function renderReveal(value: AttemptResult["correct_answer"]): string {
  if (typeof value === "string") return value
  if (Array.isArray(value)) return value.join(" · ")
  return Object.entries(value)
    .map(([l, r]) => `${l} → ${r}`)
    .join(", ")
}

export function ExerciseCard({ exercise }: ExerciseCardProps) {
  const isSimple = SIMPLE_TYPES.includes(exercise.exercise_type)

  // One state holds whichever answer shape this type needs.
  const [text, setText] = useState("")
  const [list, setList] = useState<string[]>([])
  const [map, setMap] = useState<Record<string, string>>({})
  const [selectedLeft, setSelectedLeft] = useState<string | null>(null)
  const [result, setResult] = useState<AttemptResult | null>(null)
  const [aiFeedback, setAiFeedback] = useState("")
  const { guard } = useGuestLimit()

  function currentAnswer(): UserAnswer {
    switch (exercise.exercise_type) {
      case "sentence_order":
      case "word_bank":
        return list
      case "matching":
        return map
      case "multiple_choice":
        return text
      default:
        return text
    }
  }

  const aiMutation = useMutation({
    mutationFn: (correctAnswer: string) =>
      aiCheckAnswer(exercise.prompt, correctAnswer, text || JSON.stringify(currentAnswer())),
    onSuccess: (t) => setAiFeedback(t),
  })

  const mutation = useMutation({
    mutationFn: () => attemptExercise(exercise.id, currentAnswer()),
    onSuccess: (data) => {
      setResult(data)
      // Only ask the AI tutor for simple, text-based exercises.
      if (isSimple && typeof data.correct_answer === "string") {
        aiMutation.mutate(data.correct_answer)
      }
    },
  })

  function handleSubmit(e?: FormEvent) {
    e?.preventDefault()
    if (result || !answerReady(exercise.exercise_type, currentAnswer())) return
    if (!guard()) return // guests: blocked once the daily free cap is hit
    mutation.mutate()
  }

  const disabled = !!result
  const borderClass = result
    ? result.is_correct
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

      {exercise.hint && !result && (
        <p className="mb-3 text-sm text-muted-foreground">Hint: {exercise.hint}</p>
      )}

      {/* Type-specific input */}
      {isSimple ? (
        <form onSubmit={handleSubmit} className="flex flex-wrap gap-2">
          <Input
            value={text}
            onChange={(e) => setText(e.target.value)}
            placeholder="Your answer in German…"
            aria-label="Your answer"
            disabled={disabled}
            className="w-72"
          />
          {!result && (
            <Button type="submit" disabled={mutation.isPending}>
              {mutation.isPending ? "Checking…" : "Submit"}
            </Button>
          )}
        </form>
      ) : (
        <div className="flex flex-col gap-3">
          {exercise.exercise_type === "multiple_choice" && (
            <MultipleChoiceInput
              payload={exercise.payload}
              value={text}
              onChange={setText}
              disabled={disabled}
            />
          )}
          {exercise.exercise_type === "sentence_order" && (
            <SentenceOrderInput
              payload={exercise.payload}
              value={list}
              onChange={setList}
              disabled={disabled}
            />
          )}
          {exercise.exercise_type === "word_bank" && (
            <WordBankInput
              payload={exercise.payload}
              value={list}
              onChange={setList}
              disabled={disabled}
            />
          )}
          {exercise.exercise_type === "matching" && (
            <MatchingInput
              payload={exercise.payload}
              value={map}
              onChange={setMap}
              disabled={disabled}
              selectedLeft={selectedLeft}
              setSelectedLeft={setSelectedLeft}
            />
          )}
          {!result && (
            <div>
              <Button onClick={() => handleSubmit()} disabled={mutation.isPending}>
                {mutation.isPending ? "Checking…" : "Submit"}
              </Button>
            </div>
          )}
        </div>
      )}

      {result && (
        <div className="mt-4 flex flex-col gap-1.5">
          <p
            className={cn(
              "text-sm font-medium",
              result.is_correct
                ? "text-[hsl(var(--success))]"
                : "text-[hsl(var(--danger))]",
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

          {aiMutation.isPending && (
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
      )}
    </article>
  )
}
