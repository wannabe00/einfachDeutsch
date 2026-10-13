import { useState } from "react"
import { useMutation, useQueryClient } from "@tanstack/react-query"

import type { HistoryCompleteResult, HistoryQuizQuestion } from "@/types"
import { Button } from "@/components/ui/button"
import { cn } from "@/lib/utils"

/** Multiple-choice quiz for a history lesson: collects answers, submits them
    with `onSubmit` for server grading, then reveals right/wrong per option and
    the score. */
export function LessonQuiz({
  quiz,
  onSubmit,
}: {
  quiz: HistoryQuizQuestion[]
  onSubmit: (answers: Record<string, string>) => Promise<HistoryCompleteResult>
}) {
  const qc = useQueryClient()
  const [answers, setAnswers] = useState<Record<string, string>>({})
  const [result, setResult] = useState<HistoryCompleteResult | null>(null)

  const submit = useMutation({
    mutationFn: () => onSubmit(answers),
    onSuccess: (r) => {
      setResult(r)
      qc.invalidateQueries({ queryKey: ["history"] })
    },
  })

  const allAnswered = quiz.every((q) => answers[String(q.id)] !== undefined)
  const resultFor = (qid: number) => result?.results.find((r) => r.id === qid)

  return (
    <div className="mx-auto mt-10 max-w-2xl rounded-[24px] bg-surface p-6 shadow-card sm:p-7">
      <h2 className="text-2xl font-extrabold">Quick quiz</h2>
      <div className="mt-5 flex flex-col gap-6">
        {quiz.map((q, idx) => {
          const res = resultFor(q.id)
          return (
            <div key={q.id}>
              <p className="font-semibold">
                {idx + 1}. {q.prompt}
              </p>
              <div className="mt-3 flex flex-wrap gap-2">
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
                        "min-h-[44px] rounded-xl border-2 px-4 py-2 text-[15px] font-medium transition-colors disabled:cursor-default",
                        isAnswer
                          ? "border-[hsl(var(--success))] bg-[hsl(var(--success-bg))] text-[hsl(var(--success))]"
                          : isWrongPick
                            ? "border-[hsl(var(--danger))] bg-[hsl(var(--danger-bg))] text-[hsl(var(--danger))]"
                            : picked
                              ? "border-primary bg-primary text-primary-foreground"
                              : "border-transparent bg-surface-2 hover:bg-border",
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
        <p className="mt-6 rounded-2xl bg-surface-2/70 p-4 text-[15px]">
          You scored <span className="font-bold text-primary">{result.score}%</span> (
          {result.correct}/{result.total}).{" "}
          {result.score === 100 ? "All correct." : "Lesson marked complete."}
        </p>
      ) : (
        <Button
          size="lg"
          className="mt-6 w-full sm:w-auto"
          disabled={!allAnswered || submit.isPending}
          onClick={() => submit.mutate()}
        >
          {submit.isPending ? "Checking…" : "Submit answers"}
        </Button>
      )}
    </div>
  )
}
