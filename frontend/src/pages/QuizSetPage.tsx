import { useState } from "react"
import { Link, useNavigate, useParams } from "react-router-dom"
import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query"

import type { LesenAnswerResult, LesenSetDetail, LesenTeil } from "@/types"
import { QUIZ_SKILLS, type QuizSkill } from "@/lib/examSkills"
import { errorText } from "@/lib/apiError"
import { isAnswered } from "@/lib/exercises"
import { AnswerFeedback } from "@/components/exercises/AnswerFeedback"
import { ExerciseInput } from "@/components/exercises/ExerciseInput"
import { Button } from "@/components/ui/button"
import { Card } from "@/components/ui/card"
import { SessionBar } from "@/components/ui/SessionBar"

/*
 * One Lesen or Hören set, Teil by Teil: read or listen, answer every question,
 * check, then the next Teil. The server grades each Teil and keeps the best
 * result; the score screen shows this run, passed at 60 % as in the exam.
 * Hören also shows the transcripts after checking.
 */
export default function QuizSetPage({ skill }: { skill: QuizSkill }) {
  const def = QUIZ_SKILLS[skill]
  const { level = "", modul = "" } = useParams()
  const { data, isLoading, isError, error } = useQuery({
    queryKey: [skill, level, Number(modul)],
    queryFn: () => def.fetchSet(level, Number(modul)),
    retry: false,
  })

  if (isLoading) return <Centered>Loading…</Centered>
  if (isError || !data) return <Centered>{isError ? errorText(error) : `Couldn’t load this ${def.label} set.`}</Centered>
  return <Player key={`${data.cefr_level}-${data.modul}`} set={data} skill={skill} />
}

function Player({ set, skill }: { set: LesenSetDetail; skill: QuizSkill }) {
  const def = QUIZ_SKILLS[skill]
  const navigate = useNavigate()
  const queryClient = useQueryClient()
  const [results, setResults] = useState<LesenAnswerResult[]>([])
  const [run, setRun] = useState(0)
  const step = results.length
  const title = `${def.title} · ${set.cefr_level} Modul ${set.modul}`

  if (step >= set.teile.length) {
    return (
      <Score
        set={set}
        skill={skill}
        results={results}
        onAgain={() => {
          setResults([])
          setRun((r) => r + 1)
        }}
      />
    )
  }

  return (
    <div className="mx-auto flex max-w-2xl flex-col gap-8">
      <SessionBar
        onClose={() => navigate(def.path)}
        closeLabel={`Back to ${def.title}`}
        title={title}
        progress={(step / set.teile.length) * 100}
        counter={`Teil ${step + 1}/${set.teile.length}`}
      />
      <TeilStep
        key={`${run}-${step}`}
        teil={set.teile[step]}
        answer={def.answer}
        onNext={(result) => {
          setResults((r) => [...r, result])
          if (step + 1 >= set.teile.length) queryClient.invalidateQueries({ queryKey: [skill] })
        }}
      />
    </div>
  )
}

function TeilStep({
  teil,
  answer: send,
  onNext,
}: {
  teil: LesenTeil
  answer: (exerciseId: number, answer: unknown) => Promise<LesenAnswerResult>
  onNext: (result: LesenAnswerResult) => void
}) {
  const [answer, setAnswer] = useState<unknown>([])
  const [feedback, setFeedback] = useState<LesenAnswerResult | null>(null)
  const check = useMutation({
    mutationFn: () => send(teil.exercise_id, answer),
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
        {feedback?.transcripts && <Transcripts transcripts={feedback.transcripts} />}
        {check.isError && <p className="mt-4 text-sm text-[hsl(var(--danger))]">{errorText(check.error)}</p>}
        <div className="mt-8">
          {feedback ? (
            <Button size="lg" className="w-full" onClick={() => onNext(feedback)}>
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

function Transcripts({ transcripts }: { transcripts: string[] }) {
  const numbered = transcripts.length > 1
  return (
    <details className="mt-5 rounded-2xl bg-surface-2/70 p-4 text-[15px]">
      <summary className="cursor-pointer font-semibold">Transcript</summary>
      <ol className="mt-3 flex flex-col gap-3">
        {transcripts.map((t, i) =>
          t ? (
            <li key={i} className="whitespace-pre-line leading-relaxed">
              {numbered && <span className="mr-1.5 font-semibold tabular-nums">{i + 1}.</span>}
              {t}
            </li>
          ) : null,
        )}
      </ol>
    </details>
  )
}

function Score({
  set,
  skill,
  results,
  onAgain,
}: {
  set: LesenSetDetail
  skill: QuizSkill
  results: LesenAnswerResult[]
  onAgain: () => void
}) {
  const def = QUIZ_SKILLS[skill]
  const right = results.reduce((n, r) => n + r.right, 0)
  const total = results.reduce((n, r) => n + r.total, 0)
  const passed = right >= set.pass_share * total

  return (
    <div className="mx-auto max-w-md py-8">
      <Card>
        <div className="p-8">
          <div className="text-center">
            <span className="mx-auto flex size-24 items-center justify-center rounded-full bg-primary/10 font-grotesk text-3xl font-extrabold tabular-nums text-primary animate-in zoom-in-50 fade-in-0 duration-500">
              {right}/{total}
            </span>
            <h1 className="mt-6 text-2xl font-extrabold">{passed ? "Bestanden!" : "Nicht bestanden"}</h1>
            <p className="mt-1 text-muted-foreground">
              {passed
                ? "You'd pass this part of the exam."
                : `You need ${Math.ceil(set.pass_share * total)} right to pass. ${def.retry}`}
            </p>
          </div>
          <ul className="mt-7 flex flex-col gap-2">
            {results.map((r, i) => (
              <li key={i} className="flex justify-between rounded-2xl bg-surface-2/70 px-4 py-3 text-sm">
                <span className="font-semibold">Teil {set.teile[i].teil}</span>
                <span className="tabular-nums text-muted-foreground">
                  {r.right}/{r.total}
                </span>
              </li>
            ))}
          </ul>
          <div className="mt-7 flex flex-col gap-2.5">
            <Button size="lg" onClick={onAgain}>
              Try again
            </Button>
            <Button asChild size="lg" variant="secondary">
              <Link to={def.path}>All {def.label} sets</Link>
            </Button>
          </div>
        </div>
      </Card>
    </div>
  )
}

function Centered({ children }: { children: React.ReactNode }) {
  return (
    <div className="flex h-64 items-center justify-center">
      <p className="text-muted-foreground">{children}</p>
    </div>
  )
}
