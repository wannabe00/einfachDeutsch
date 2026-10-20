import { useRef, useState } from "react"
import { Link, useNavigate, useParams } from "react-router-dom"
import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query"
import { Check, ChevronDown, Crown, Sparkles, X } from "lucide-react"

import {
  aiGradeWriting,
  answerSchreibenForm,
  fetchSchreibenSet,
  fetchWritingAttempts,
  selfCheckWriting,
  writeSchreiben,
} from "@/api/curriculum"
import type { FormResult, PointGrade, SchreibenSetDetail, SchreibenTeil, WriteResult, WritingAttempt } from "@/types"
import { useAuth } from "@/contexts/AuthContext"
import { errorText } from "@/lib/apiError"
import { isAnswered } from "@/lib/exercises"
import { cn } from "@/lib/utils"
import { AnswerFeedback } from "@/components/exercises/AnswerFeedback"
import { ExerciseInput } from "@/components/exercises/ExerciseInput"
import { UmlautBar } from "@/components/vocabulary/UmlautBar"
import { Button } from "@/components/ui/button"
import { Card } from "@/components/ui/card"
import { SessionBar } from "@/components/ui/SessionBar"

/*
 * One Schreiben set, Teil by Teil. The A1 form is graded on the server like
 * any exercise. A written text is saved first; then the learner sees the
 * checks (length, greeting, sign-off) and a model answer, and either rates the
 * three points themselves or, with Premium, has the AI grade it on the exam's
 * criteria. The server always computes the score.
 */

type Score = { score: number; out_of: number; selfChecked: boolean }

const CHOSEN = "border-[hsl(var(--choice))] bg-[hsl(var(--choice-bg))]"
const GRADE_LABEL: Record<PointGrade, string> = { full: "Yes", partial: "Partly", missing: "No" }
const WORD = /[0-9A-Za-zÄÖÜäöüß]+(?:[-'][0-9A-Za-zÄÖÜäöüß]+)*/g

function countWords(text: string) {
  return (text.match(WORD) ?? []).length
}

export default function SchreibenSetPage() {
  const { level = "", modul = "" } = useParams()
  const { data, isLoading, isError, error } = useQuery({
    queryKey: ["schreiben", level, Number(modul)],
    queryFn: () => fetchSchreibenSet(level, Number(modul)),
    retry: false,
  })

  if (isLoading) return <Centered>Loading…</Centered>
  if (isError || !data) return <Centered>{isError ? errorText(error) : "Couldn’t load this writing set."}</Centered>
  return <Player key={`${data.cefr_level}-${data.modul}`} set={data} />
}

function Player({ set }: { set: SchreibenSetDetail }) {
  const navigate = useNavigate()
  const queryClient = useQueryClient()
  const [scores, setScores] = useState<Score[]>([])
  const [run, setRun] = useState(0)
  const step = scores.length

  if (step >= set.teile.length) {
    return (
      <Results
        set={set}
        scores={scores}
        onAgain={() => {
          setScores([])
          setRun((r) => r + 1)
        }}
      />
    )
  }

  const teil = set.teile[step]
  function next(score: Score) {
    setScores((s) => [...s, score])
    queryClient.invalidateQueries({ queryKey: ["schreiben"] })
  }

  return (
    <div className="mx-auto flex max-w-2xl flex-col gap-8">
      <SessionBar
        onClose={() => navigate("/schreiben")}
        closeLabel="Back to Schreiben"
        title={`Schreiben · ${set.cefr_level} Modul ${set.modul}`}
        progress={(step / set.teile.length) * 100}
        counter={`Teil ${step + 1}/${set.teile.length}`}
      />
      {teil.type === "group" ? (
        <FormTeil key={`${run}-${step}`} teil={teil} onNext={next} />
      ) : (
        <WriteTeil key={`${run}-${step}`} teil={teil} level={set.cefr_level} onNext={next} />
      )}
    </div>
  )
}

function FormTeil({ teil, onNext }: { teil: SchreibenTeil; onNext: (s: Score) => void }) {
  const [answer, setAnswer] = useState<unknown>([])
  const [feedback, setFeedback] = useState<FormResult | null>(null)
  const check = useMutation({
    mutationFn: () => answerSchreibenForm(teil.exercise_id, answer),
    onSuccess: setFeedback,
  })
  const ready = isAnswered(teil, answer)

  return (
    <Card>
      <div className="p-6 sm:p-8">
        <p className="text-xl font-bold leading-snug sm:text-2xl">{teil.prompt}</p>
        <div className="mt-5">
          <ExerciseInput
            content={teil}
            value={answer}
            onChange={setAnswer}
            disabled={!!feedback}
            results={feedback?.parts}
            solution={feedback?.solution}
          />
        </div>
        {feedback && <AnswerFeedback feedback={feedback} content={teil} />}
        {check.isError && <ErrorLine error={check.error} />}
        <div className="mt-8">
          {feedback ? (
            <Button
              size="lg"
              className="w-full"
              onClick={() =>
                onNext({ score: feedback.attempt.score ?? 0, out_of: feedback.attempt.max_score, selfChecked: false })
              }
            >
              Continue
            </Button>
          ) : (
            <Button size="lg" className="w-full" disabled={!ready || check.isPending} onClick={() => check.mutate()}>
              Check
            </Button>
          )}
        </div>
      </div>
    </Card>
  )
}

function WriteTeil({ teil, level, onNext }: { teil: SchreibenTeil; level: string; onNext: (s: Score) => void }) {
  const task = teil.payload
  const textRef = useRef<HTMLTextAreaElement>(null)
  const [text, setText] = useState("")
  const [written, setWritten] = useState<WriteResult | null>(null)
  const [attempt, setAttempt] = useState<WritingAttempt | null>(null)
  const queryClient = useQueryClient()
  const words = countWords(text)

  const write = useMutation({
    mutationFn: () => writeSchreiben(teil.exercise_id, text),
    onSuccess: (res) => {
      setWritten(res)
      setAttempt(res.attempt)
      queryClient.invalidateQueries({ queryKey: ["writing-attempts", teil.exercise_id] })
    },
  })

  function graded(a: WritingAttempt) {
    setAttempt(a)
    queryClient.invalidateQueries({ queryKey: ["writing-attempts", teil.exercise_id] })
  }

  return (
    <div className="flex flex-col gap-4">
      <Card>
        <div className="p-6 sm:p-8">
          <p className="text-xl font-bold leading-snug sm:text-2xl">{teil.prompt}</p>
          <p className="mt-4 whitespace-pre-line rounded-2xl bg-surface-2/70 p-4 text-[15px] leading-relaxed">
            {task.situation}
          </p>
          <p className="mt-4 text-sm font-semibold">Write about all three points:</p>
          <ul className="mt-2 flex flex-col gap-1.5 text-[15px]">
            {(task.points ?? []).map((p, i) => (
              <li key={i} className="flex gap-2">
                <span className="tabular-nums text-muted-foreground">{i + 1}.</span>
                {p}
              </li>
            ))}
          </ul>
          <p className="mt-3 text-sm text-muted-foreground">
            {task.min_words}–{task.max_words} words ·{" "}
            {task.forum
              ? "a forum post: give your opinion, no greeting needed."
              : `${task.formal ? "formal (Sie)" : "informal (du)"} · start with a greeting and end with a sign-off.`}
          </p>

          <textarea
            ref={textRef}
            value={text}
            onChange={(e) => setText(e.target.value)}
            disabled={!!written}
            rows={7}
            maxLength={2000}
            aria-label="Your text"
            placeholder={task.forum ? "Ich finde …" : task.formal ? "Sehr geehrte …" : "Hallo …"}
            className="mt-5 w-full rounded-2xl border border-transparent bg-surface-2 px-4 py-3 text-base leading-relaxed placeholder:text-muted-foreground focus-visible:border-ring focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring disabled:opacity-80"
          />
          <p
            className={cn(
              "mt-1.5 text-right text-sm tabular-nums",
              words >= (task.min_words ?? 0) && words <= (task.max_words ?? Infinity)
                ? "text-foreground"
                : "text-muted-foreground",
            )}
          >
            {words} words
          </p>
          {!written && (
            <>
              <div className="mt-3">
                <UmlautBar inputRef={textRef} value={text} onChange={setText} />
              </div>
              {write.isError && <ErrorLine error={write.error} />}
              <Button
                size="lg"
                className="mt-6 w-full"
                disabled={!text.trim() || write.isPending}
                onClick={() => write.mutate()}
              >
                {write.isPending ? "Saving…" : "Done writing"}
              </Button>
            </>
          )}
        </div>
      </Card>

      {written && attempt && (
        <Grading
          level={level}
          written={written}
          attempt={attempt}
          onGraded={graded}
          onNext={() =>
            onNext({ score: attempt.score ?? 0, out_of: attempt.max_score, selfChecked: attempt.graded_by === "self" })
          }
        />
      )}
      <PastAttempts exerciseId={teil.exercise_id} />
    </div>
  )
}

function Grading({
  level,
  written,
  attempt,
  onGraded,
  onNext,
}: {
  level: string
  written: WriteResult
  attempt: WritingAttempt
  onGraded: (a: WritingAttempt) => void
  onNext: () => void
}) {
  const { user } = useAuth()
  const [grades, setGrades] = useState<(PointGrade | null)[]>([null, null, null])
  const self = useMutation({
    mutationFn: () => selfCheckWriting(attempt.id, grades as PointGrade[]),
    onSuccess: onGraded,
  })
  const ai = useMutation({ mutationFn: () => aiGradeWriting(attempt.id), onSuccess: onGraded })
  const checks = attempt.feedback.checks
  const done = attempt.score !== null

  return (
    <Card>
      <div className="flex flex-col gap-5 p-6 sm:p-8">
        {checks && (
          <ul className="flex flex-wrap gap-2 text-sm">
            <CheckChip ok={checks.in_range}>
              {checks.words} words ({checks.min_words}–{checks.max_words})
            </CheckChip>
            {!checks.forum && <CheckChip ok={checks.greeting}>Greeting</CheckChip>}
            {!checks.forum && <CheckChip ok={checks.closing}>Sign-off</CheckChip>}
          </ul>
        )}
        {checks?.too_short && (
          <p className="text-[15px]">
            In the exam a text under half the minimum length gets 0 points. Write a bit more next time.
          </p>
        )}

        <div>
          <p className="text-sm font-semibold">A model answer</p>
          <p className="mt-2 whitespace-pre-line rounded-2xl bg-surface-2/70 p-4 text-[15px] leading-relaxed">
            {written.model}
          </p>
        </div>

        {done ? (
          <Graded level={level} attempt={attempt} points={written.points} />
        ) : (
          <>
            <div>
              <p className="text-sm font-semibold">Check yourself: did your text cover each point?</p>
              <ul className="mt-3 flex flex-col gap-3">
                {written.points.map((p, i) => (
                  <li key={i}>
                    <p className="text-[15px]">
                      {i + 1}. {p}
                    </p>
                    <div className="mt-1.5 grid grid-cols-3 gap-2" role="radiogroup" aria-label={p}>
                      {(Object.keys(GRADE_LABEL) as PointGrade[]).map((g) => (
                        <button
                          key={g}
                          type="button"
                          role="radio"
                          aria-checked={grades[i] === g}
                          onClick={() => setGrades((gs) => gs.map((x, j) => (j === i ? g : x)))}
                          className={cn(
                            "min-h-[44px] rounded-xl border-2 text-sm font-semibold transition-colors",
                            grades[i] === g ? CHOSEN : "border-transparent bg-surface-2 hover:bg-border",
                          )}
                        >
                          {GRADE_LABEL[g]}
                        </button>
                      ))}
                    </div>
                  </li>
                ))}
              </ul>
              {self.isError && <ErrorLine error={self.error} />}
              <Button
                size="lg"
                variant="secondary"
                className="mt-4 w-full"
                disabled={grades.includes(null) || self.isPending || ai.isPending}
                onClick={() => self.mutate()}
              >
                Score my text
              </Button>
            </div>

            {user?.has_premium ? (
              <div>
                {ai.isError && <ErrorLine error={ai.error} />}
                <Button
                  size="lg"
                  className="w-full"
                  disabled={ai.isPending || self.isPending}
                  onClick={() => ai.mutate()}
                >
                  <Sparkles className="size-4" aria-hidden="true" />
                  {ai.isPending ? "Grading…" : "Grade with AI instead"}
                </Button>
              </div>
            ) : (
              <p className="flex items-start gap-2.5 rounded-2xl bg-surface-2/70 p-4 text-sm">
                <Crown className="mt-0.5 size-4 shrink-0 text-primary" aria-hidden="true" />
                <span>
                  With Premium, the AI grades your text like an examiner, corrects it and gives tips.{" "}
                  <Link to="/ai" className="font-semibold text-primary hover:underline">
                    See Premium
                  </Link>
                </span>
              </p>
            )}
          </>
        )}

        {done && (
          <Button size="lg" className="w-full" onClick={onNext}>
            Continue
          </Button>
        )}
      </div>
    </Card>
  )
}

function Graded({ level, attempt, points }: { level: string; attempt: WritingAttempt; points: string[] }) {
  const fb = attempt.feedback
  const byAI = attempt.graded_by === "ai"
  return (
    <div className="flex flex-col gap-4">
      <div className="flex items-baseline justify-between">
        <p className="text-lg font-bold">
          {attempt.score}/{attempt.max_score} points
        </p>
        <span className="text-sm text-muted-foreground">
          {byAI ? "Graded by AI" : attempt.graded_by === "self" ? "Self-check" : "Checked automatically"}
        </span>
      </div>
      {level !== "A1" && fb.grades?.task && (
        <p className="text-sm text-muted-foreground">
          Task: {fb.grades.task}
          {fb.grades.language ? ` · Language: ${fb.grades.language}` : " · Language isn’t scored in a self-check"}
        </p>
      )}
      {level === "A1" && fb.grades?.communication !== undefined && (
        <p className="text-sm text-muted-foreground">Greeting and sign-off: {fb.grades.communication}/1</p>
      )}
      {byAI && (
        <>
          <ul className="flex flex-col gap-2">
            {points.map((p, i) => (
              <li key={i} className="rounded-2xl bg-surface-2/70 p-3 text-sm">
                <p className="font-semibold">
                  {i + 1}. {p}: {GRADE_LABEL[attempt.points[i]] ?? "–"}
                </p>
                {fb.comments?.[i] && <p className="mt-1 text-muted-foreground">{fb.comments[i]}</p>}
              </li>
            ))}
          </ul>
          {fb.corrected && (
            <div>
              <p className="text-sm font-semibold">Your text, corrected</p>
              <p className="mt-2 whitespace-pre-line rounded-2xl bg-surface-2/70 p-4 text-[15px] leading-relaxed">
                {fb.corrected}
              </p>
            </div>
          )}
          {!!fb.tips?.length && (
            <ul className="list-disc pl-5 text-sm">
              {fb.tips.map((t, i) => (
                <li key={i}>{t}</li>
              ))}
            </ul>
          )}
        </>
      )}
    </div>
  )
}

function PastAttempts({ exerciseId }: { exerciseId: number }) {
  const [open, setOpen] = useState(false)
  const { data } = useQuery({
    queryKey: ["writing-attempts", exerciseId],
    queryFn: () => fetchWritingAttempts(exerciseId),
  })
  if (!data?.length) return null
  return (
    <Card>
      <div className="p-5 sm:p-6">
        <button
          type="button"
          onClick={() => setOpen((o) => !o)}
          aria-expanded={open}
          className="flex w-full items-center justify-between text-left font-semibold"
        >
          Your texts so far ({data.length})
          <ChevronDown className={cn("size-5 transition-transform", open && "rotate-180")} aria-hidden="true" />
        </button>
        {open && (
          <ul className="mt-4 flex flex-col gap-3">
            {data.map((a) => (
              <li key={a.id} className="rounded-2xl bg-surface-2/70 p-4 text-[15px]">
                <p className="mb-2 flex justify-between text-sm text-muted-foreground">
                  <span>{new Date(a.created_at).toLocaleDateString()}</span>
                  <span>{a.score === null ? "Not graded" : `${a.score}/${a.max_score}`}</span>
                </p>
                <p className="whitespace-pre-line">{typeof a.answer === "string" ? a.answer : a.answer.join(" · ")}</p>
                {a.feedback.corrected && (
                  <p className="mt-2 whitespace-pre-line text-sm text-muted-foreground">
                    Corrected: {a.feedback.corrected}
                  </p>
                )}
              </li>
            ))}
          </ul>
        )}
      </div>
    </Card>
  )
}

function Results({ set, scores, onAgain }: { set: SchreibenSetDetail; scores: Score[]; onAgain: () => void }) {
  const got = scores.reduce((n, s) => n + s.score, 0)
  const outOf = scores.reduce((n, s) => n + s.out_of, 0)
  const passed = got >= set.pass_share * outOf
  const selfChecked = set.cefr_level !== "A1" && scores.some((s) => s.selfChecked)

  return (
    <div className="mx-auto max-w-md py-8">
      <Card>
        <div className="p-8">
          <div className="text-center">
            <span className="mx-auto flex size-24 items-center justify-center rounded-full bg-primary/10 font-grotesk text-3xl font-extrabold tabular-nums text-primary animate-in zoom-in-50 fade-in-0 duration-500">
              {got}/{outOf}
            </span>
            <h1 className="mt-6 text-2xl font-extrabold">{passed ? "Bestanden!" : "Nicht bestanden"}</h1>
            <p className="mt-1 text-muted-foreground">
              {passed
                ? "You'd pass this part of the exam."
                : `You need ${Math.ceil(set.pass_share * outOf * 2) / 2} points to pass. Try again with the model answers in mind.`}
            </p>
            {selfChecked && (
              <p className="mt-2 text-sm text-muted-foreground">
                Self-checked texts score content only; language is graded by the AI (Premium).
              </p>
            )}
          </div>
          <ul className="mt-7 flex flex-col gap-2">
            {scores.map((s, i) => (
              <li key={i} className="flex justify-between rounded-2xl bg-surface-2/70 px-4 py-3 text-sm">
                <span className="font-semibold">Teil {set.teile[i].teil}</span>
                <span className="tabular-nums text-muted-foreground">
                  {s.score}/{s.out_of}
                </span>
              </li>
            ))}
          </ul>
          <div className="mt-7 flex flex-col gap-2.5">
            <Button size="lg" onClick={onAgain}>
              Try again
            </Button>
            <Button asChild size="lg" variant="secondary">
              <Link to="/schreiben">All writing sets</Link>
            </Button>
          </div>
        </div>
      </Card>
    </div>
  )
}

function CheckChip({ ok, children }: { ok: boolean; children: React.ReactNode }) {
  return (
    <li
      className={cn(
        "inline-flex items-center gap-1.5 rounded-full px-3 py-1 font-semibold",
        ok ? "bg-[hsl(var(--success-bg))] text-[hsl(var(--success))]" : "bg-surface-2 text-muted-foreground",
      )}
    >
      {ok ? <Check className="size-4" aria-hidden="true" /> : <X className="size-4" aria-hidden="true" />}
      {children}
    </li>
  )
}

function ErrorLine({ error }: { error: unknown }) {
  return <p className="mt-3 text-sm text-[hsl(var(--danger))]">{errorText(error)}</p>
}

function Centered({ children }: { children: React.ReactNode }) {
  return (
    <div className="flex h-64 items-center justify-center">
      <p className="text-muted-foreground">{children}</p>
    </div>
  )
}
