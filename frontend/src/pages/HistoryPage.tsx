import { useState } from "react"
import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query"
import { ArrowLeft, Check, Landmark } from "lucide-react"

import {
  completeHistoryLesson,
  fetchHistoryLesson,
  fetchHistoryLessons,
} from "@/api/history"
import { useAuth } from "@/contexts/AuthContext"
import type { CEFRLevel, HistoryCompleteResult } from "@/types"
import { Button } from "@/components/ui/button"
import { cn } from "@/lib/utils"

// English is shown alongside German through A2; German-only from B1.
const ENGLISH_LEVELS: CEFRLevel[] = ["A1", "A2"]

export default function HistoryPage() {
  const [selectedId, setSelectedId] = useState<number | null>(null)
  const { data: lessons } = useQuery({
    queryKey: ["history"],
    queryFn: fetchHistoryLessons,
  })

  if (selectedId !== null) {
    return <LessonView id={selectedId} onBack={() => setSelectedId(null)} />
  }

  // Group lessons by era, preserving order.
  const eras: string[] = []
  for (const l of lessons ?? []) if (!eras.includes(l.era)) eras.push(l.era)

  return (
    <div>
      <h1 className="text-2xl font-semibold tracking-tight">German history</h1>
      <p className="mt-1 text-sm text-muted-foreground">
        Short lessons on German history — read, then take a quick quiz. Available
        any day (no schedule).
      </p>

      <div className="mt-6 flex flex-col gap-8">
        {eras.map((era) => (
          <section key={era}>
            <h2 className="mb-3 text-xs font-semibold uppercase tracking-wide text-muted-foreground">
              {era}
            </h2>
            <div className="grid gap-4 sm:grid-cols-2">
              {(lessons ?? [])
                .filter((l) => l.era === era)
                .map((l) => (
                  <button
                    key={l.id}
                    onClick={() => setSelectedId(l.id)}
                    className="group flex items-center justify-between gap-3 rounded-xl border border-border bg-surface p-5 text-left shadow-sm transition-all hover:border-accent hover:shadow-md"
                  >
                    <div className="flex items-center gap-3">
                      <div className="flex size-9 items-center justify-center rounded-lg bg-accent/10 text-accent">
                        <Landmark className="size-5" />
                      </div>
                      <span className="font-semibold text-foreground">{l.title}</span>
                    </div>
                    {l.completed && (
                      <Check className="size-5 shrink-0 text-[hsl(var(--success))]" />
                    )}
                  </button>
                ))}
            </div>
          </section>
        ))}
      </div>
    </div>
  )
}

function LessonView({ id, onBack }: { id: number; onBack: () => void }) {
  const { user } = useAuth()
  const qc = useQueryClient()
  const [answers, setAnswers] = useState<Record<string, string>>({})
  const [result, setResult] = useState<HistoryCompleteResult | null>(null)

  const { data: lesson, isLoading } = useQuery({
    queryKey: ["history", id],
    queryFn: () => fetchHistoryLesson(id),
  })

  const submit = useMutation({
    mutationFn: () => completeHistoryLesson(id, answers),
    onSuccess: (r) => {
      setResult(r)
      qc.invalidateQueries({ queryKey: ["history"] })
    },
  })

  const showEnglish = !!user && ENGLISH_LEVELS.includes(user.cefr_level)
  const allAnswered =
    !!lesson && lesson.quiz.every((q) => answers[String(q.id)] !== undefined)

  function resultFor(qid: number) {
    return result?.results.find((r) => r.id === qid)
  }

  return (
    <div>
      <button
        onClick={onBack}
        className="inline-flex items-center gap-1.5 text-sm text-muted-foreground hover:text-accent"
      >
        <ArrowLeft className="size-4" /> All lessons
      </button>

      {isLoading || !lesson ? (
        <p className="mt-6 text-sm text-muted-foreground">Loading…</p>
      ) : (
        <>
          <h1 className="mt-4 text-2xl font-semibold tracking-tight">
            {lesson.title}
          </h1>
          <p className="mt-1 text-xs font-semibold uppercase tracking-wide text-muted-foreground">
            {lesson.era}
          </p>

          {/* German always; English alongside through A2 */}
          <div className="mt-5 rounded-xl border border-border bg-surface p-5">
            <p className="whitespace-pre-wrap leading-relaxed">{lesson.body_de}</p>
            {showEnglish && lesson.body_en && (
              <div className="mt-4 border-t border-border pt-4">
                <p className="mb-1 text-xs font-medium uppercase tracking-wide text-muted-foreground">
                  English (shown through A2)
                </p>
                <p className="whitespace-pre-wrap leading-relaxed text-muted-foreground">
                  {lesson.body_en}
                </p>
              </div>
            )}
          </div>

          {/* Quiz */}
          {lesson.quiz.length > 0 && (
            <div className="mt-6">
              <h2 className="text-base font-semibold">Quick quiz</h2>
              <div className="mt-3 flex flex-col gap-5">
                {lesson.quiz.map((q, idx) => {
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
                              onClick={() =>
                                setAnswers((a) => ({ ...a, [String(q.id)]: opt }))
                              }
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
                  You scored{" "}
                  <span className="font-semibold text-accent">{result.score}%</span>{" "}
                  ({result.correct}/{result.total}).{" "}
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
          )}
        </>
      )}
    </div>
  )
}
