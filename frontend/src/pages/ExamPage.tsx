import { useState } from "react"
import { Link, useNavigate } from "react-router-dom"
import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query"
import { ArrowLeft, ArrowRight, Award } from "lucide-react"

import { fetchExamStatus, startExam, submitExam } from "@/api/curriculum"
import type { ExamQuestion, ExamResult } from "@/types"
import { useAuth } from "@/contexts/AuthContext"
import { Button } from "@/components/ui/button"
import { Card } from "@/components/ui/card"
import { BackLink } from "@/components/ui/BackLink"
import { SessionBar } from "@/components/ui/SessionBar"
import { ProgressRing } from "@/components/lektion/ProgressRing"
import { cn } from "@/lib/utils"
import { ExerciseInput } from "@/components/exercises/ExerciseInput"
import { isAnswered } from "@/lib/exercises"

/*
 * The exam between levels. It unlocks once you've nearly finished your level's
 * path. Pass and you move up; fail and you can review and retry.
 *
 * The server picks and stores the questions when the attempt starts, grades
 * them, and promotes on submit. Unlike a lesson there's no feedback per
 * question.
 */
const BRAND = "hsl(var(--brand))"

export default function ExamPage() {
  const qc = useQueryClient()
  const navigate = useNavigate()
  const { refreshUser } = useAuth()

  const { data: status, isLoading } = useQuery({ queryKey: ["exam"], queryFn: fetchExamStatus })
  const [questions, setQuestions] = useState<ExamQuestion[] | null>(null)
  const [attemptId, setAttemptId] = useState<number | null>(null)
  const [answers, setAnswers] = useState<Record<string, unknown>>({})
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
      qc.invalidateQueries({ queryKey: ["checks"] })
    },
  })

  if (isLoading || !status) return <Centered>Loading…</Centered>
  if (result) return <Result result={result} onRetry={() => setResult(null)} navigate={navigate} />

  // ---- Taking the exam ---------------------------------------------------
  if (questions && questions.length > 0) {
    const q = questions[step]
    // Only complete answers count; a half-built sentence isn't answered yet.
    const isDone = (x: ExamQuestion) => isAnswered(x, answers[x.question_id])
    const answered = questions.filter(isDone).length
    const last = step === questions.length - 1
    return (
      <div className="mx-auto flex min-h-[calc(100svh-3rem)] max-w-2xl flex-col gap-6">
        <SessionBar
          title={`${status.level} checkpoint exam · ${answered} of ${questions.length} answered`}
          progress={(answered / questions.length) * 100}
          counter={`${step + 1}/${questions.length}`}
        />

        {/* Jump to any question; answered ones are filled. */}
        <nav aria-label="Questions" className="flex flex-wrap justify-center gap-1.5">
          {questions.map((x, i) => (
            <button
              key={x.question_id}
              onClick={() => setStep(i)}
              aria-label={`Question ${i + 1}${isDone(x) ? ", answered" : ""}`}
              aria-current={i === step ? "step" : undefined}
              className={cn(
                "flex size-8 items-center justify-center rounded-full text-xs font-bold tabular-nums transition-colors",
                i === step
                  ? "bg-foreground text-background"
                  : isDone(x)
                    ? "bg-primary/15 text-primary"
                    : "bg-surface-2 text-muted-foreground hover:bg-border",
              )}
            >
              {i + 1}
            </button>
          ))}
        </nav>

        <div className="flex flex-1 flex-col justify-center">
          <Card>
            <div className="p-6 sm:p-8">
              <p className={KICKER}>Question {step + 1}</p>
              <p className="mt-2 text-xl font-bold leading-snug sm:text-2xl">{q.prompt}</p>
              <div className="mt-6">
                <ExerciseInput
                  key={q.question_id}
                  content={q}
                  value={answers[q.question_id] ?? (q.type === "sentence_order" ? [] : "")}
                  onChange={(v) => setAnswers((a) => ({ ...a, [q.question_id]: v }))}
                  autoFocus
                  onSubmit={() => !last && setStep(step + 1)}
                />
              </div>
            </div>
          </Card>
        </div>

        <div className="flex items-center justify-between gap-3">
          <Button variant="secondary" size="lg" disabled={step === 0} onClick={() => setStep(step - 1)}>
            <ArrowLeft /> Back
          </Button>
          {last ? (
            <Button size="lg" disabled={finish.isPending} onClick={() => finish.mutate()}>
              {finish.isPending ? "Grading…" : `Submit (${answered}/${questions.length})`}
            </Button>
          ) : (
            <Button size="lg" onClick={() => setStep(step + 1)}>
              Next <ArrowRight />
            </Button>
          )}
        </div>
        <p className="text-center text-sm text-muted-foreground">
          You can go back and change answers. Nothing is graded until you submit.
        </p>
      </div>
    )
  }

  // ---- Intro / locked ----------------------------------------------------
  const pct = Math.round(status.progress * 100)
  return (
    <div className="mx-auto flex min-h-[calc(100svh-3rem)] max-w-xl flex-col gap-6">
      <BackLink to="/path" label="Path" />
      <div className="flex flex-1 flex-col justify-center">
        <Card className="rounded-[28px] p-7 text-center sm:p-9">
          {status.unlocked ? (
            <>
              <span className="mx-auto flex size-20 items-center justify-center rounded-3xl bg-primary text-primary-foreground">
                <Award className="size-10" aria-hidden="true" />
              </span>
              <p className={`mt-6 ${KICKER}`}>{status.level} checkpoint exam</p>
              <h1 className="mt-1 text-3xl font-extrabold sm:text-4xl">
                Ready for {status.next_level ?? "the exam"}?
              </h1>
              <p className="mt-2 text-muted-foreground">
                Questions drawn from everything you've learned at {status.level}.
              </p>
              <dl className="mt-6 grid grid-cols-3 gap-2 rounded-2xl bg-surface-2/70 p-4">
                <Fact label="questions" value={String(status.question_count)} />
                <Fact label="to pass" value={`${Math.round(status.pass_threshold * 100)}%`} />
                <Fact label="energy" value="0" />
              </dl>
              <p className="mt-4 text-sm text-muted-foreground">
                Pass and you move up{status.next_level ? ` to ${status.next_level}` : ""}. If you
                don't, you keep your level and can try again after some review.
              </p>
              <Button size="lg" className="mt-7 w-full" disabled={begin.isPending} onClick={() => begin.mutate()}>
                {begin.isPending ? "Preparing…" : "Start exam"}
              </Button>
            </>
          ) : (
            <>
              <div className="relative mx-auto flex size-32 items-center justify-center">
                <ProgressRing pct={status.progress} color={BRAND} size={128} stroke={11} label={`${pct}% of your path done`} />
                <span className="absolute font-grotesk text-3xl font-extrabold tabular-nums">{pct}%</span>
              </div>
              <p className={`mt-6 ${KICKER}`}>{status.level} checkpoint exam</p>
              <h1 className="mt-1 text-3xl font-extrabold">Finish your path first</h1>
              <p className="mt-2 text-muted-foreground">
                The exam unlocks at {Math.round(status.unlock_ratio * 100)}% of your path. You've
                done {status.completed_lessons} of {status.total_lessons} lessons.
              </p>
              <Button size="lg" className="mt-7 w-full" asChild>
                <Link to="/path">Continue your path</Link>
              </Button>
            </>
          )}

          {status.last_attempt && (
            <p className="mt-6 border-t border-border pt-4 text-sm text-muted-foreground">
              Last attempt: {Math.round(status.last_attempt.score * 100)}% (
              {status.last_attempt.passed ? "passed" : "not passed"})
            </p>
          )}
        </Card>
      </div>
    </div>
  )
}

function Fact({ label, value }: { label: string; value: string }) {
  return (
    <div className="flex flex-col items-center">
      <dd className="font-grotesk text-2xl font-extrabold tabular-nums">{value}</dd>
      <dt className="text-xs text-muted-foreground">{label}</dt>
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
  const score = Math.round(result.score * 100)
  return (
    <div className="mx-auto flex min-h-[calc(100svh-3rem)] max-w-md flex-col justify-center">
      <Card className="rounded-[28px] p-8 text-center">
        <span
          className={cn(
            "mx-auto flex size-28 items-center justify-center rounded-full font-grotesk text-4xl font-extrabold tabular-nums animate-in zoom-in-50 fade-in-0 duration-500",
            result.passed
              ? "bg-[hsl(var(--success-bg))] text-[hsl(var(--success))]"
              : "bg-surface-2 text-muted-foreground",
          )}
        >
          {score}%
        </span>
        <h1 className="mt-6 text-3xl font-extrabold">
          {result.promoted_to
            ? `Willkommen bei ${result.promoted_to}!`
            : result.passed
              ? "Bestanden!"
              : "Nicht bestanden"}
        </h1>
        <p className="mt-2 text-muted-foreground">
          {result.correct} of {result.total} correct · you needed{" "}
          {Math.round(result.pass_threshold * 100)}%
        </p>

        {result.promoted_to ? (
          <p className="mt-4 text-muted-foreground">
            Your level is now <strong className="text-foreground">{result.promoted_to}</strong>.
            New Lektionen are open on your path.
          </p>
        ) : (
          <p className="mt-4 text-muted-foreground">
            You're still at <strong className="text-foreground">{result.level}</strong>. Review
            what you missed and retake it whenever you like. It doesn't cost energy.
          </p>
        )}

        <div className="mt-7 flex flex-col gap-2.5">
          <Button size="lg" onClick={() => navigate("/path")}>
            Go to path
          </Button>
          {!result.passed && (
            <Button size="lg" variant="secondary" onClick={onRetry}>
              Try again
            </Button>
          )}
        </div>
      </Card>
    </div>
  )
}

const KICKER = "text-[13px] font-semibold uppercase tracking-[0.04em] text-muted-foreground"

function Centered({ children }: { children: React.ReactNode }) {
  return (
    <div className="flex h-64 items-center justify-center">
      <p className="text-sm text-muted-foreground">{children}</p>
    </div>
  )
}
