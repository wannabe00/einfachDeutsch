import { useState } from "react"
import { Link, useNavigate, useParams } from "react-router-dom"
import { useQuery, useQueryClient } from "@tanstack/react-query"
import { Check, Crown, RotateCcw, Zap } from "lucide-react"

import { answerItem, completeLesson, fetchLesson, restartLesson } from "@/api/curriculum"
import type {
  AnswerResult,
  CompleteResult,
  ExerciseContent,
  GrammarContent,
  LessonDetail,
  LessonItemDTO,
  ReviewContent,
} from "@/types"
import { resolveAccent } from "@/lib/sections"
import { Button } from "@/components/ui/button"
import { Card } from "@/components/ui/card"
import { SessionBar } from "@/components/ui/SessionBar"
import { Markdown } from "@/components/ui/Markdown"
import { AnswerFeedback } from "@/components/exercises/AnswerFeedback"
import { ExerciseInput } from "@/components/exercises/ExerciseInput"
import { isAnswered } from "@/lib/exercises"

/*
 * The lesson player: one item at a time with immediate feedback. Each answer is
 * graded by the server, which returns whether it was right and the solution
 * (the solution is never sent beforehand). On finish the server re-grades
 * everything, awards XP and a crown, and spends energy only on a first pass.
 *
 * Every checked answer is also saved on the server, so a lesson that's left
 * halfway opens where it stopped.
 */
export default function LessonPlayerPage() {
  const { unitId, lessonId } = useParams()
  const id = Number(lessonId)

  const { data, isLoading, error } = useQuery({
    queryKey: ["lesson", id],
    queryFn: () => fetchLesson(id),
    enabled: Number.isFinite(id),
    retry: false,
    // Never start from a cached copy: the saved position may have moved.
    gcTime: 0,
  })

  if (isLoading) return <Centered>Loading lesson…</Centered>
  if (error) return <OutOfEnergy unitId={unitId} />
  if (!data) return <Centered>Couldn’t load this lesson.</Centered>
  return <Player lesson={data} unitId={unitId} />
}

function Player({ lesson, unitId }: { lesson: LessonDetail; unitId?: string }) {
  const navigate = useNavigate()
  const qc = useQueryClient()
  const resumeAt = Math.max(0, Math.min(lesson.saved?.step ?? 0, lesson.items.length - 1))
  const [step, setStep] = useState(resumeAt)
  const [resumed, setResumed] = useState(resumeAt > 0)
  // Answers given in this sitting; earlier ones are already on the server.
  const [answers, setAnswers] = useState<{ item_id: number; answer: unknown }[]>([])
  const [result, setResult] = useState<CompleteResult | null>(null)
  const accent = resolveAccent(lesson.accent_color, 0)

  async function startOver() {
    await restartLesson(lesson.id)
    setAnswers([])
    setStep(0)
    setResumed(false)
  }

  if (result) {
    return <Summary result={result} accent={accent} unitId={unitId} lessonTitle={lesson.title} />
  }

  const item = lesson.items[step]
  const progress = (step / lesson.items.length) * 100

  async function handleNext(answer?: unknown) {
    const next = answer === undefined ? answers : [...answers, { item_id: item.id, answer }]
    if (answer !== undefined) setAnswers(next)

    if (step + 1 < lesson.items.length) {
      setStep(step + 1)
      return
    }
    const res = await completeLesson(lesson.id, next)
    setResult(res)
    // The path/unit pages now show new states, energy, crowns.
    qc.invalidateQueries({ queryKey: ["path"] })
    qc.invalidateQueries({ queryKey: ["unit"] })
    qc.invalidateQueries({ queryKey: ["energy"] })
    qc.invalidateQueries({ queryKey: ["checks"] })
  }

  return (
    <div className="mx-auto flex min-h-[calc(100svh-3rem)] max-w-2xl flex-col gap-6">
      <SessionBar
        onClose={() => navigate(`/path/${unitId}`)}
        closeLabel="Quit lesson"
        progress={progress}
        counter={`${step + 1}/${lesson.items.length}`}
      />

      {resumed && (
        <p className="flex items-center justify-center gap-2 text-sm text-muted-foreground">
          Picked up where you left off.
          <button
            onClick={startOver}
            className="inline-flex min-h-[36px] items-center gap-1 rounded-full bg-surface-2 px-3 font-medium text-foreground"
          >
            <RotateCcw className="size-3.5" aria-hidden="true" /> Start over
          </button>
        </p>
      )}

      <div className="flex flex-1 flex-col justify-center">
        <ItemStep key={item.id} item={item} lessonId={lesson.id} onNext={handleNext} />
      </div>

      <p className="text-center text-xs text-muted-foreground">
        Your answers are saved, so you can stop and come back. Energy is only spent when you
        finish.
      </p>
    </div>
  )
}

function ItemStep({
  item,
  lessonId,
  onNext,
}: {
  item: LessonItemDTO
  lessonId: number
  onNext: (answer?: unknown) => void
}) {
  if (item.kind === "review") {
    const c = item.content as ReviewContent
    return (
      <Card>
        <div className="p-8 text-center sm:p-10">
          <p className={KICKER}>New word</p>
          <p className="mt-4 font-grotesk text-3xl font-extrabold tracking-tight [overflow-wrap:anywhere] sm:text-5xl">{c.german}</p>
          <p className="mt-2 text-lg text-muted-foreground">{c.english}</p>
          <Button size="lg" className="mt-8 w-full" onClick={() => onNext()}>
            Got it
          </Button>
        </div>
      </Card>
    )
  }

  if (item.kind === "grammar") {
    const c = item.content as GrammarContent
    return (
      <Card>
        <div className="p-6 sm:p-8">
          <p className={KICKER}>Grammar</p>
          <h2 className="mt-1 text-2xl font-bold">{c.title}</h2>
          <Markdown className="mt-3 text-muted-foreground">{c.content}</Markdown>
          {c.example_sentences && (
            <ul className="mt-4 space-y-1.5 rounded-xl bg-surface-2/70 p-4 text-[15px]">
              {c.example_sentences.split("\n").filter(Boolean).map((ex) => (
                <li key={ex}>{ex}</li>
              ))}
            </ul>
          )}
          <Button size="lg" className="mt-8 w-full" onClick={() => onNext()}>
            Continue
          </Button>
        </div>
      </Card>
    )
  }

  return (
    <ExerciseStep
      content={item.content as ExerciseContent}
      itemId={item.id}
      lessonId={lessonId}
      onNext={onNext}
    />
  )
}

function ExerciseStep({
  content,
  itemId,
  lessonId,
  onNext,
}: {
  content: ExerciseContent
  itemId: number
  lessonId: number
  onNext: (answer: unknown) => void
}) {
  const [answer, setAnswer] = useState<unknown>(
    content.type === "sentence_order" || content.type === "group" ? [] : "",
  )
  const [feedback, setFeedback] = useState<AnswerResult | null>(null)
  const ready = isAnswered(content, answer)

  async function check() {
    if (!ready || feedback) return
    setFeedback(await answerItem(lessonId, itemId, answer))
  }

  return (
    <Card>
      <div className="p-6 sm:p-8">
        <p className={KICKER}>
          {content.type === "sentence_order" ? "Build the sentence" : "Exercise"}
        </p>
        <p className="mt-2 text-xl font-bold leading-snug sm:text-2xl">{content.prompt}</p>

        <div className="mt-5">
          <ExerciseInput
            content={content}
            value={answer}
            onChange={setAnswer}
            disabled={!!feedback}
            autoFocus
            onSubmit={check}
            results={feedback?.parts}
            solution={feedback?.solution}
          />
        </div>

        {content.hint && !feedback && (
          <p className="mt-4 text-sm text-muted-foreground">Hint: {content.hint}</p>
        )}

        {feedback && <AnswerFeedback feedback={feedback} content={content} />}

        <div className="mt-8">
          {feedback ? (
            <Button size="lg" className="w-full" onClick={() => onNext(answer)}>
              Continue
            </Button>
          ) : (
            <Button size="lg" className="w-full" disabled={!ready} onClick={check}>
              Check
            </Button>
          )}
        </div>
      </div>
    </Card>
  )
}

function Summary({
  result,
  accent,
  unitId,
  lessonTitle,
}: {
  result: CompleteResult
  accent: string
  unitId?: string
  lessonTitle: string
}) {
  return (
    <div className="mx-auto flex min-h-[calc(100svh-3rem)] max-w-md flex-col justify-center">
      <Card>
        <div className="p-8 text-center">
          <span
            className={`mx-auto flex size-24 items-center justify-center rounded-full animate-in zoom-in-50 fade-in-0 duration-500 ${
              result.passed
                ? "bg-[hsl(var(--success-bg))] text-[hsl(var(--success))]"
                : "bg-surface-2 text-muted-foreground"
            }`}
          >
            {result.passed ? (
              <Check className="size-12" strokeWidth={2.5} aria-hidden="true" />
            ) : (
              <RotateCcw className="size-10" aria-hidden="true" />
            )}
          </span>
          <p className={`mt-6 ${KICKER}`}>{lessonTitle}</p>
          <h1 className="mt-2 text-3xl font-extrabold">
            {result.passed ? "Lektion geschafft!" : "Fast geschafft"}
          </h1>
          <p className="mt-1 text-muted-foreground">
            {result.correct}/{result.total} correct · {Math.round(result.score * 100)}%
          </p>

          <div className="mt-7 grid grid-cols-3 gap-2 rounded-2xl bg-surface-2/70 p-4">
            <Stat label="XP" value={`+${result.xp_earned}`} />
            <Stat
              label="Crown"
              value={
                <span className="inline-flex items-center gap-1">
                  <Crown className="size-4" style={{ color: accent }} /> {result.crown}
                </span>
              }
            />
            <Stat
              label="Energy"
              value={
                <span className="inline-flex items-center gap-1">
                  <Zap className="size-4" style={{ color: "hsl(var(--brand))" }} />
                  {result.energy.premium ? "∞" : result.energy.current}
                </span>
              }
            />
          </div>

          {!result.passed && (
            <p className="mt-5 text-sm text-muted-foreground">
              You need 60% to pass. No energy was spent, so try again.
            </p>
          )}

          <Button asChild size="lg" className="mt-7 w-full">
            <Link to={`/path/${unitId}`}>Back to Lektion</Link>
          </Button>
        </div>
      </Card>
    </div>
  )
}

function Stat({ label, value }: { label: string; value: React.ReactNode }) {
  return (
    <div className="flex flex-col items-center">
      <span className="font-grotesk text-2xl font-extrabold tabular-nums">{value}</span>
      <span className="mt-0.5 text-xs text-muted-foreground">{label}</span>
    </div>
  )
}

function OutOfEnergy({ unitId }: { unitId?: string }) {
  return (
    <div className="mx-auto max-w-md">
      <Card>
        <div className="p-8 text-center">
          <Zap className="mx-auto size-8" style={{ color: "hsl(var(--brand))" }} />
          <h1 className="mt-3 text-2xl font-bold">Out of energy</h1>
          <p className="mt-2 text-sm text-muted-foreground">
            New lessons cost 1 energy, which refills over time. Review, Word Bank, Grammar and
            redoing finished lessons are always free. Premium has no energy limit.
          </p>
          <Button asChild variant="secondary" size="lg" className="mt-6 w-full">
            <Link to={`/path/${unitId ?? ""}`}>Back to Lektion</Link>
          </Button>
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
