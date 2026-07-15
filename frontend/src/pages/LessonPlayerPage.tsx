import { useState } from "react"
import { Link, useNavigate, useParams } from "react-router-dom"
import { useQuery, useQueryClient } from "@tanstack/react-query"
import ReactMarkdown from "react-markdown"
import { Check, Crown, X, Zap } from "lucide-react"

import { answerItem, completeLesson, fetchLesson } from "@/api/curriculum"
import type {
  AnswerResult,
  CompleteResult,
  ExerciseContent,
  GrammarContent,
  LessonItemDTO,
  ReviewContent,
} from "@/types"
import { resolveAccent } from "@/lib/sections"
import { cn } from "@/lib/utils"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { SectionCard } from "@/components/ui/SectionCard"

/*
 * The lesson player (Phase 23.5) — one item at a time, immediate feedback.
 * Grading is server-side and deterministic: we submit an answer and get back
 * correctness + the solution (which is never in the payload beforehand). On
 * finish the server re-grades everything authoritatively and awards XP/crown,
 * spending energy only on a successful first completion.
 */
export default function LessonPlayerPage() {
  const { unitId, lessonId } = useParams()
  const id = Number(lessonId)
  const navigate = useNavigate()
  const qc = useQueryClient()

  const { data, isLoading, error } = useQuery({
    queryKey: ["lesson", id],
    queryFn: () => fetchLesson(id),
    enabled: Number.isFinite(id),
    retry: false,
  })

  const [step, setStep] = useState(0)
  const [answers, setAnswers] = useState<{ item_id: number; answer: unknown }[]>([])
  const [result, setResult] = useState<CompleteResult | null>(null)

  if (isLoading) return <Centered>Loading lesson…</Centered>
  if (error) return <OutOfEnergy unitId={unitId} />
  if (!data) return <Centered>Couldn’t load this lesson.</Centered>

  // Bind after the guard — TS won't carry the narrowing into the closures below.
  const lesson = data
  const accent = resolveAccent(lesson.accent_color, 0)

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
  }

  return (
    <div className="mx-auto flex max-w-2xl flex-col gap-6">
      <div className="flex items-center gap-4">
        <button
          onClick={() => navigate(`/path/${unitId}`)}
          aria-label="Quit lesson"
          className="text-muted-foreground transition-colors hover:text-foreground"
        >
          <X className="size-5" />
        </button>
        <div className="h-2 flex-1 overflow-hidden rounded-full bg-border">
          <div
            className="h-2 rounded-full transition-all duration-300"
            style={{ width: `${progress}%`, background: accent }}
          />
        </div>
        <span className="text-xs tabular-nums text-muted-foreground">
          {step + 1}/{lesson.items.length}
        </span>
      </div>

      <ItemStep key={item.id} item={item} lessonId={lesson.id} accent={accent} onNext={handleNext} />

      <p className="text-center text-xs text-muted-foreground">
        Quitting is free — energy is only spent when you finish.
      </p>
    </div>
  )
}

function ItemStep({
  item,
  lessonId,
  accent,
  onNext,
}: {
  item: LessonItemDTO
  lessonId: number
  accent: string
  onNext: (answer?: unknown) => void
}) {
  if (item.kind === "review") {
    const c = item.content as ReviewContent
    return (
      <SectionCard accent={accent}>
        <div className="p-8 text-center">
          <p className="text-xs font-semibold uppercase tracking-wider text-muted-foreground">
            New word
          </p>
          <p className="mt-3 text-3xl font-bold">{c.german}</p>
          <p className="mt-1 text-muted-foreground">{c.english}</p>
          <Button className="mt-6" onClick={() => onNext()}>
            Got it
          </Button>
        </div>
      </SectionCard>
    )
  }

  if (item.kind === "grammar") {
    const c = item.content as GrammarContent
    return (
      <SectionCard accent={accent} glow>
        <div className="p-6">
          <p className="text-xs font-semibold uppercase tracking-wider text-muted-foreground">
            Grammar
          </p>
          <h2 className="mt-1 text-xl font-bold">{c.title}</h2>
          <div className="mt-3 space-y-1 text-sm text-muted-foreground [&_strong]:text-foreground">
            <ReactMarkdown>{c.content}</ReactMarkdown>
          </div>
          {c.example_sentences && (
            <ul className="mt-3 space-y-1 border-t border-border pt-3 text-sm">
              {c.example_sentences.split("\n").filter(Boolean).map((ex) => (
                <li key={ex}>{ex}</li>
              ))}
            </ul>
          )}
          <Button className="mt-6" onClick={() => onNext()}>
            Continue
          </Button>
        </div>
      </SectionCard>
    )
  }

  return (
    <ExerciseStep
      content={item.content as ExerciseContent}
      itemId={item.id}
      lessonId={lessonId}
      accent={accent}
      onNext={onNext}
    />
  )
}

function ExerciseStep({
  content,
  itemId,
  lessonId,
  accent,
  onNext,
}: {
  content: ExerciseContent
  itemId: number
  lessonId: number
  accent: string
  onNext: (answer: unknown) => void
}) {
  const [text, setText] = useState("")
  const [picked, setPicked] = useState<string | null>(null)
  const [order, setOrder] = useState<string[]>([])
  const [feedback, setFeedback] = useState<AnswerResult | null>(null)

  const isMC = content.type === "multiple_choice"
  const isOrder = content.type === "sentence_order"
  const answer: unknown = isMC ? picked : isOrder ? order : text
  const ready = isMC ? !!picked : isOrder ? order.length === (content.payload.tokens?.length ?? 0) : text.trim().length > 0

  async function check() {
    setFeedback(await answerItem(lessonId, itemId, answer))
  }

  return (
    <SectionCard accent={accent}>
      <div className="p-6">
        <p className="text-xs font-semibold uppercase tracking-wider text-muted-foreground">
          {isOrder ? "Build the sentence" : "Exercise"}
        </p>
        <p className="mt-2 text-lg font-semibold">{content.prompt}</p>

        {isMC && (
          <div className="mt-5 grid gap-2">
            {(content.payload.options ?? []).map((o) => (
              <button
                key={o}
                disabled={!!feedback}
                onClick={() => setPicked(o)}
                className={cn(
                  "rounded-xl border-2 px-4 py-3 text-left font-medium transition-colors",
                  picked === o ? "border-transparent text-white" : "border-border hover:border-white/30",
                )}
                style={picked === o ? { background: accent } : undefined}
              >
                {o}
              </button>
            ))}
          </div>
        )}

        {isOrder && (
          <div className="mt-5">
            <div className="min-h-14 rounded-xl border-2 border-dashed border-border p-2">
              <div className="flex flex-wrap gap-2">
                {order.map((t, i) => (
                  <button
                    key={`${t}-${i}`}
                    disabled={!!feedback}
                    onClick={() => setOrder(order.filter((_, j) => j !== i))}
                    className="rounded-lg bg-surface-2 px-3 py-1.5 text-sm font-medium ring-1 ring-white/10"
                  >
                    {t}
                  </button>
                ))}
              </div>
            </div>
            <div className="mt-3 flex flex-wrap gap-2">
              {(content.payload.tokens ?? [])
                .filter((t) => order.filter((o) => o === t).length < (content.payload.tokens ?? []).filter((x) => x === t).length)
                .map((t, i) => (
                  <button
                    key={`${t}-pool-${i}`}
                    disabled={!!feedback}
                    onClick={() => setOrder([...order, t])}
                    className="rounded-lg border border-border px-3 py-1.5 text-sm font-medium transition-colors hover:border-white/30"
                  >
                    {t}
                  </button>
                ))}
            </div>
          </div>
        )}

        {!isMC && !isOrder && (
          <Input
            className="mt-5"
            autoFocus
            value={text}
            disabled={!!feedback}
            placeholder="Your answer…"
            onChange={(e) => setText(e.target.value)}
            onKeyDown={(e) => {
              if (e.key === "Enter" && ready && !feedback) check()
            }}
          />
        )}

        {content.hint && !feedback && (
          <p className="mt-3 text-xs text-muted-foreground">Hint: {content.hint}</p>
        )}

        {feedback && <Feedback feedback={feedback} />}

        <div className="mt-6">
          {feedback ? (
            <Button onClick={() => onNext(answer)}>Continue</Button>
          ) : (
            <Button disabled={!ready} onClick={check}>
              Check
            </Button>
          )}
        </div>
      </div>
    </SectionCard>
  )
}

function Feedback({ feedback }: { feedback: AnswerResult }) {
  const solution = Array.isArray(feedback.solution) ? feedback.solution.join(" ") : feedback.solution
  return (
    <div
      className={cn(
        "mt-5 rounded-xl p-4",
        feedback.correct
          ? "bg-[hsl(var(--success)/0.12)] text-[hsl(var(--success))]"
          : "bg-[hsl(var(--danger)/0.12)] text-[hsl(var(--danger))]",
      )}
    >
      <p className="flex items-center gap-2 font-semibold">
        {feedback.correct ? <Check className="size-4" /> : <X className="size-4" />}
        {feedback.correct ? "Richtig!" : "Not quite"}
      </p>
      {!feedback.correct && (
        <p className="mt-1 text-sm text-foreground">
          Answer: <span className="font-semibold">{solution}</span>
        </p>
      )}
      {feedback.explanation && (
        <p className="mt-1 text-sm text-muted-foreground">{feedback.explanation}</p>
      )}
    </div>
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
    <div className="mx-auto max-w-md">
      <SectionCard accent={accent} glow>
        <div className="p-8 text-center">
          <p className="text-xs font-semibold uppercase tracking-wider text-muted-foreground">
            {lessonTitle}
          </p>
          <h1 className="mt-2 text-3xl font-bold">
            {result.passed ? "Lektion geschafft!" : "Fast geschafft"}
          </h1>
          <p className="mt-1 text-muted-foreground">
            {result.correct}/{result.total} correct · {Math.round(result.score * 100)}%
          </p>

          <div className="mt-6 flex items-center justify-center gap-6">
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
              You need 60% to advance — no energy spent. Give it another go.
            </p>
          )}

          <Button asChild className="mt-7">
            <Link to={`/path/${unitId}`}>Back to unit</Link>
          </Button>
        </div>
      </SectionCard>
    </div>
  )
}

function Stat({ label, value }: { label: string; value: React.ReactNode }) {
  return (
    <div className="flex flex-col items-center">
      <span className="text-xl font-bold">{value}</span>
      <span className="mt-0.5 text-xs text-muted-foreground">{label}</span>
    </div>
  )
}

function OutOfEnergy({ unitId }: { unitId?: string }) {
  return (
    <div className="mx-auto max-w-md">
      <SectionCard accent="hsl(var(--brand))" glow>
        <div className="p-8 text-center">
          <Zap className="mx-auto size-8" style={{ color: "hsl(var(--brand))" }} />
          <h1 className="mt-3 text-2xl font-bold">Out of energy</h1>
          <p className="mt-2 text-sm text-muted-foreground">
            New lessons cost 1 energy, and it refills over time. Review, Word Bank, Grammar and
            redoing finished lessons are always free — or go Premium for unlimited energy.
          </p>
          <Button asChild variant="secondary" className="mt-6">
            <Link to={`/path/${unitId ?? ""}`}>Back to unit</Link>
          </Button>
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
