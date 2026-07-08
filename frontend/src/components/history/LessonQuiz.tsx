import { useState } from "react"
import { useMutation, useQueryClient } from "@tanstack/react-query"

import { completeHistoryLesson } from "@/api/history"
import type { HistoryCompleteResult, HistoryQuizQuestion } from "@/types"
import { Button } from "@/components/ui/button"
import { cn } from "@/lib/utils"

/** Multiple-choice quiz for a history lesson: collects answers, submits for
    server grading, then reveals correct/wrong per option + the score. */
export function LessonQuiz({
  lessonId,
  quiz,
}: {
  lessonId: number
  quiz: HistoryQuizQuestion[]
}) {
  const qc = useQueryClient()
  const [answers, setAnswers] = useState<Record<string, string>>({})
  const [result, setResult] = useState<HistoryCompleteResult | null>(null)

  const submit = useMutation({
    mutationFn: () => completeHistoryLesson(lessonId, answers),
    onSuccess: (r) => {
      setResult(r)
      qc.invalidateQueries({ queryKey: ["history"] })
    },
  })

  const allAnswered = quiz.every((q) => answers[String(q.id)] !== undefined)
  const resultFor = (qid: number) => result?.results.find((r) => r.id === qid)

  return (
    <div className="mt-6">
      <h2 className="text-base font-semibold">Quick quiz</h2>
      <div className="mt-3 flex flex-col gap-5">
        {quiz.map((q, idx) => {
          const res = resultFor(q.id)
          return (
            <div key={q.id}>
              <p className="text-sm font-medium">
                {idx + 1}. {q.prompt}
              </p>
              <div className="mt-2 flex flex-wrap gap-2">
                {q.options.map((opt) => {
                  const picked = answers[String(q.id)] === opt
                  const isAnswer = result && res?.answer === opt
                  const isWrongPick = result && picked && !res?.correct
                  return (
                    <button
                      key={opt}
                      disabled={!!result}
                      onClick={() => setAnswers((a) => ({ ...a, [String(q.id)]: opt }))}
                      className={cn(
                        "rounded-lg border px-3 py-1.5 text-sm transition-colors disabled:cursor-default",
                        isAnswer
                          ? "border-[hsl(var(--success))] bg-[hsl(var(--success-bg))] text-[hsl(var(--success))]"
                          : isWrongPick
                            ? "border-[hsl(var(--danger))] bg-[hsl(var(--danger-bg))] text-[hsl(var(--danger))]"
                            : picked
                              ? "border-accent bg-accent text-accent-foreground"
                              : "border-border bg-background hover:border-accent",
                      )}
                    >
                      {opt}
                    </button>
                  )
                })}
              </div>
            </div>
          )
        })}
      </div>

      {result ? (
        <p className="mt-5 text-sm">
          You scored <span className="font-semibold text-accent">{result.score}%</span> (
          {result.correct}/{result.total}).{" "}
          {result.score === 100 ? "Perfect!" : "Lesson marked complete."}
        </p>
      ) : (
        <Button
          className="mt-5"
          disabled={!allAnswered || submit.isPending}
          onClick={() => submit.mutate()}
        >
          {submit.isPending ? "Checking…" : "Submit answers"}
        </Button>
      )}
    </div>
  )
}
