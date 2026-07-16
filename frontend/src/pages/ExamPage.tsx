import { useState } from "react"
import { Link, useNavigate } from "react-router-dom"
import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query"
import { ArrowLeft, ArrowRight, GraduationCap, Lock, PartyPopper, RotateCcw } from "lucide-react"

import { fetchExamStatus, startExam, submitExam } from "@/api/curriculum"
import type { ExamResult, ExerciseContent } from "@/types"
import { useAuth } from "@/contexts/AuthContext"
import { Button } from "@/components/ui/button"
import { SectionCard } from "@/components/ui/SectionCard"
import { PageHeader } from "@/components/layout/PageHeader"
import { ExerciseInput } from "@/components/exercises/ExerciseInput"
import { isAnswered } from "@/lib/exercises"

/*
 * Level checkpoint exam (Phase 23.14) — the Goethe-style gate between levels.
 * Unlocks once you've essentially finished your level's path; passing promotes
 * you, failing sends you back to review and you may retry.
 *
 * Everything that matters is server-side: the questions are sampled and frozen
 * on the attempt, grading is deterministic, and promotion happens on submit.
 * Unlike a lesson, there's no per-question feedback — it's an exam.
 */
const BRAND = "hsl(var(--brand))"

export default function ExamPage() {
  const qc = useQueryClient()
  const navigate = useNavigate()
  const { refreshUser } = useAuth()

  const { data: status, isLoading } = useQuery({ queryKey: ["exam"], queryFn: fetchExamStatus })
  const [questions, setQuestions] = useState<ExerciseContent[] | null>(null)
  const [attemptId, setAttemptId] = useState<number | null>(null)
  const [answers, setAnswers] = useState<Record<number, unknown>>({})
  const [step, setStep] = useState(0)
  const [result, setResult] = useState<ExamResult | null>(null)

  const begin = useMutation({
    mutationFn: startExam,
    onSuccess: (d) => {
      setAttemptId(d.attempt_id)
      setQuestions(d.questions)
      setAnswers({})
      setStep(0)
    },
  })

  const finish = useMutation({
    mutationFn: () => submitExam(attemptId!, answers),
    onSuccess: async (res) => {
      setResult(res)
      setQuestions(null)
      // A pass changes the user's level, which re-gates the whole app.
      if (res.promoted_to) await refreshUser()
      qc.invalidateQueries({ queryKey: ["exam"] })
      qc.invalidateQueries({ queryKey: ["path"] })
    },
  })

  if (isLoading || !status) return <Centered>Loading…</Centered>
  if (result) return <Result result={result} onRetry={() => setResult(null)} navigate={navigate} />

  // ---- Taking the exam ---------------------------------------------------
  if (questions && questions.length > 0) {
    const q = questions[step]
    // Count only *complete* answers — a half-built sentence isn't answered.
    const answered = questions.filter((x) => isAnswered(x, answers[x.exercise_id])).length
    const last = step === questions.length - 1
    return (
      <div className="mx-auto flex max-w-2xl flex-col gap-6">
        <div className="flex items-center gap-4">
          <div className="h-2 flex-1 overflow-hidden rounded-full bg-border">
            <div
              className="h-2 rounded-full transition-all"
              style={{ width: `${(answered / questions.length) * 100}%`, background: BRAND }}
            />
          </div>
          <span className="text-xs tabular-nums text-muted-foreground">
            {step + 1}/{questions.length}
          </span>
        </div>

        <SectionCard accent={BRAND}>
          <div className="p-6">
            <p className="text-xs font-semibold uppercase tracking-wider text-muted-foreground">
              {status.level} exam · question {step + 1}
            </p>
            <p className="mt-2 text-lg font-semibold">{q.prompt}</p>
            <ExerciseInput
              content={q}
              value={answers[q.exercise_id] ?? (q.type === "sentence_order" ? [] : "")}
              onChange={(v) => setAnswers((a) => ({ ...a, [q.exercise_id]: v }))}
              accent={BRAND}
              autoFocus
              onSubmit={() => !last && setStep(step + 1)}
            />
          </div>
        </SectionCard>

        <div className="flex items-center justify-between">
          <Button variant="secondary" disabled={step === 0} onClick={() => setStep(step - 1)}>
            <ArrowLeft className="mr-2 size-4" /> Back
          </Button>
          {last ? (
            <Button disabled={finish.isPending} onClick={() => finish.mutate()}>
              {finish.isPending ? "Grading…" : `Submit exam (${answered}/${questions.length})`}
            </Button>
          ) : (
            <Button onClick={() => setStep(step + 1)}>
              Next <ArrowRight className="ml-2 size-4" />
            </Button>
          )}
        </div>
        <p className="text-center text-xs text-muted-foreground">
          You can go back and change answers. Nothing is graded until you submit.
        </p>
      </div>
    )
  }

  // ---- Intro / locked ----------------------------------------------------
  const pct = Math.round(status.progress * 100)
  return (
    <div className="mx-auto flex max-w-xl flex-col gap-6">
      <PageHeader title={`${status.level} checkpoint exam`} />
      <SectionCard accent={BRAND} glow={status.unlocked}>
        <div className="p-8 text-center">
          <span
            className="mx-auto flex size-14 items-center justify-center rounded-2xl"
            style={{ background: "hsl(var(--brand)/0.15)", color: BRAND }}
          >
            {status.unlocked ? <GraduationCap className="size-7" /> : <Lock className="size-6" />}
          </span>

          {status.unlocked ? (
            <>
              <h2 className="mt-4 text-2xl font-bold">Ready for {status.next_level ?? "the exam"}?</h2>
              <p className="mt-2 text-sm text-muted-foreground">
                {status.question_count} questions drawn from everything you've learned at{" "}
                {status.level}. Score {Math.round(status.pass_threshold * 100)}% or more to be
                promoted{status.next_level ? ` to ${status.next_level}` : ""}. Fail and you keep
                your level — review and try again.
              </p>
              <Button className="mt-6" disabled={begin.isPending} onClick={() => begin.mutate()}>
                {begin.isPending ? "Preparing…" : "Start exam"}
              </Button>
            </>
          ) : (
            <>
              <h2 className="mt-4 text-2xl font-bold">Finish your path first</h2>
              <p className="mt-2 text-sm text-muted-foreground">
                The {status.level} checkpoint unlocks once you've completed{" "}
                {Math.round(status.unlock_ratio * 100)}% of your path.
              </p>
              <div className="mt-5 h-2 overflow-hidden rounded-full bg-border">
                <div
                  className="h-2 rounded-full transition-all"
                  style={{ width: `${pct}%`, background: BRAND }}
                />
              </div>
              <p className="mt-2 text-xs text-muted-foreground">
                {status.completed_lessons}/{status.total_lessons} lessons · {pct}%
              </p>
              <Button variant="secondary" className="mt-6" asChild>
                <Link to="/path">Back to your path</Link>
              </Button>
            </>
          )}

          {status.last_attempt && (
            <p className="mt-5 border-t border-border pt-4 text-xs text-muted-foreground">
              Last attempt: {Math.round(status.last_attempt.score * 100)}% —{" "}
              {status.last_attempt.passed ? "passed" : "not passed"}
            </p>
          )}
        </div>
      </SectionCard>
    </div>
  )
}

function Result({
  result,
  onRetry,
  navigate,
}: {
  result: ExamResult
  onRetry: () => void
  navigate: (to: string) => void
}) {
  return (
    <div className="mx-auto max-w-md">
      <SectionCard accent={BRAND} glow>
        <div className="p-8 text-center">
          <span
            className="mx-auto flex size-14 items-center justify-center rounded-2xl"
            style={{ background: "hsl(var(--brand)/0.15)", color: BRAND }}
          >
            {result.passed ? <PartyPopper className="size-7" /> : <RotateCcw className="size-6" />}
          </span>
          <h1 className="mt-4 text-3xl font-bold">
            {result.promoted_to
              ? `Willkommen bei ${result.promoted_to}!`
              : result.passed
                ? "Bestanden!"
                : "Nicht bestanden"}
          </h1>
          <p className="mt-2 text-muted-foreground">
            {result.correct}/{result.total} correct · {Math.round(result.score * 100)}% (need{" "}
            {Math.round(result.pass_threshold * 100)}%)
          </p>

          {result.promoted_to ? (
            <p className="mt-4 text-sm text-muted-foreground">
              Your level is now <strong className="text-foreground">{result.promoted_to}</strong> —
              new units are open on your path.
            </p>
          ) : (
            <p className="mt-4 text-sm text-muted-foreground">
              You're still at <strong className="text-foreground">{result.level}</strong>. Review
              what you missed and retake it whenever you're ready — no energy spent.
            </p>
          )}

          <div className="mt-7 flex justify-center gap-3">
            <Button onClick={() => navigate("/path")}>Go to path</Button>
            {!result.passed && (
              <Button variant="secondary" onClick={onRetry}>
                Try again
              </Button>
            )}
          </div>
        </div>
      </SectionCard>
    </div>
  )
}

function Centered({ children }: { children: React.ReactNode }) {
  return (
    <div className="flex h-64 items-center justify-center">
      <p className="text-sm text-muted-foreground">{children}</p>
    </div>
  )
}
