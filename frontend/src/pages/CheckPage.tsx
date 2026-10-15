import { useState } from "react"
import { Link, useNavigate, useParams } from "react-router-dom"
import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query"
import { BookOpen, Ear, FileText, Puzzle } from "lucide-react"

import { answerCheck, fetchCheck, finishCheck } from "@/api/curriculum"
import type { AnswerResult, CheckData, CheckSkill, CheckTask } from "@/types"
import { errorText } from "@/lib/apiError"
import { isAnswered } from "@/lib/exercises"
import { AnswerFeedback } from "@/components/exercises/AnswerFeedback"
import { ExerciseInput } from "@/components/exercises/ExerciseInput"
import { Button } from "@/components/ui/button"
import { Card } from "@/components/ui/card"
import { SessionBar } from "@/components/ui/SessionBar"

/*
 * A check: the review of a finished Lektion (a third of its words in batches
 * of five, then gaps and a translation) or a Modul test (everything so far,
 * scored per skill). The server picks the tasks, grades each answer and keeps
 * them, so leaving and coming back resumes where you stopped.
 */
export default function CheckPage() {
  const id = Number(useParams().checkId)
  const { data, isLoading, isError } = useQuery({
    queryKey: ["check", id],
    queryFn: () => fetchCheck(id),
    enabled: Number.isFinite(id),
  })

  if (isLoading) return <Centered>Loading…</Centered>
  if (isError || !data) return <Centered>Couldn’t load this check.</Centered>
  if (data.completed) return <Results check={data} />
  return <Player key={data.id} check={data} />
}

function Player({ check }: { check: CheckData }) {
  const navigate = useNavigate()
  const queryClient = useQueryClient()
  const [results, setResults] = useState<Record<string, AnswerResult>>(check.results)
  const step = check.tasks.findIndex((t) => !(t.task_id in results))
  const done = step === -1

  const finish = useMutation({
    mutationFn: () => finishCheck(check.id),
    onSuccess: (finished) => {
      queryClient.setQueryData(["check", check.id], finished)
      for (const key of ["checks", "due-words", "due-counts", "stats", "activity", "streak"]) {
        queryClient.invalidateQueries({ queryKey: [key] })
      }
    },
  })

  const position = done ? check.tasks.length : step
  return (
    <div className="mx-auto flex max-w-2xl flex-col gap-8">
      <SessionBar
        onClose={() => navigate(-1)}
        closeLabel="Leave (your answers are saved)"
        title={check.title}
        progress={(position / check.tasks.length) * 100}
        counter={`${Math.min(position + 1, check.tasks.length)}/${check.tasks.length}`}
      />
      {done ? (
        <Card>
          <div className="p-8 text-center">
            <h1 className="text-2xl font-extrabold">All answered</h1>
            <p className="mt-2 text-muted-foreground">See how you did, skill by skill.</p>
            <Button size="lg" className="mt-6 w-full" disabled={finish.isPending} onClick={() => finish.mutate()}>
              {finish.isPending ? "Scoring…" : "See results"}
            </Button>
            {finish.isError && <p className="mt-3 text-sm text-[hsl(var(--danger))]">{errorText(finish.error)}</p>}
          </div>
        </Card>
      ) : (
        <TaskStep
          key={check.tasks[step].task_id}
          checkId={check.id}
          task={check.tasks[step]}
          onNext={(result) => setResults((r) => ({ ...r, [check.tasks[step].task_id]: result }))}
        />
      )}
    </div>
  )
}

function TaskStep({
  checkId,
  task,
  onNext,
}: {
  checkId: number
  task: CheckTask
  onNext: (result: AnswerResult) => void
}) {
  const [answer, setAnswer] = useState<unknown>(
    task.type === "sentence_order" || task.type === "group" ? [] : task.type === "matching" ? {} : "",
  )
  const [feedback, setFeedback] = useState<AnswerResult | null>(null)
  const check = useMutation({
    mutationFn: () => answerCheck(checkId, task.task_id, answer),
    onSuccess: setFeedback,
  })
  const ready = isAnswered(task, answer)

  function submit() {
    if (ready && !feedback && !check.isPending) check.mutate()
  }

  return (
    <Card>
      <div className="p-6 sm:p-8">
        <p className="text-xl font-bold leading-snug sm:text-2xl">{task.prompt}</p>
        {task.hint && <p className="mt-1 text-muted-foreground">{task.hint}</p>}
        <div className="mt-5">
          <ExerciseInput
            content={task}
            value={answer}
            onChange={setAnswer}
            disabled={!!feedback}
            autoFocus
            onSubmit={submit}
            results={feedback?.parts}
            solution={feedback?.solution}
          />
        </div>
        {feedback && <AnswerFeedback feedback={feedback} content={task} />}
        {check.isError && <p className="mt-4 text-sm text-[hsl(var(--danger))]">{errorText(check.error)}</p>}
        <div className="mt-8">
          {feedback ? (
            <Button size="lg" className="w-full" onClick={() => onNext(feedback)}>
              Continue
            </Button>
          ) : (
            <Button size="lg" className="w-full" disabled={!ready || check.isPending} onClick={submit}>
              Check
            </Button>
          )}
        </div>
      </div>
    </Card>
  )
}

const SKILLS: Record<CheckSkill, { label: string; icon: typeof BookOpen; practise: { to: string; label: string } }> = {
  words: { label: "Words", icon: BookOpen, practise: { to: "/review", label: "Review your words" } },
  grammar: { label: "Grammar", icon: Puzzle, practise: { to: "/grammar", label: "Go over the grammar" } },
  listening: { label: "Listening", icon: Ear, practise: { to: "/drills", label: "Practise with drills" } },
  reading: { label: "Reading", icon: FileText, practise: { to: "/exercises", label: "Do a practice set" } },
}

function Results({ check }: { check: CheckData }) {
  const score = Math.round((check.score ?? 0) * 100)
  const skills = (Object.keys(SKILLS) as CheckSkill[]).filter((s) => check.skills[s])
  const weakest = skills
    .map((s) => ({ s, pct: check.skills[s]!.right / check.skills[s]!.total }))
    .sort((a, b) => a.pct - b.pct)[0]
  const tip = weakest && weakest.pct < 0.8 ? SKILLS[weakest.s] : null

  return (
    <div className="mx-auto max-w-md py-8">
      <Card>
        <div className="p-8">
          <div className="text-center">
            <span className="mx-auto flex size-24 items-center justify-center rounded-full bg-primary/10 font-grotesk text-3xl font-extrabold tabular-nums text-primary animate-in zoom-in-50 fade-in-0 duration-500">
              {score}%
            </span>
            <h1 className="mt-6 text-2xl font-extrabold">{check.title}</h1>
            <p className="mt-1 text-muted-foreground">{check.subtitle}</p>
          </div>

          <ul className="mt-7 flex flex-col gap-4">
            {skills.map((s) => {
              const { right, total } = check.skills[s]!
              const Icon = SKILLS[s].icon
              return (
                <li key={s}>
                  <div className="mb-1.5 flex items-center justify-between text-sm">
                    <span className="flex items-center gap-2 font-semibold">
                      <Icon className="size-4 text-muted-foreground" aria-hidden="true" />
                      {SKILLS[s].label}
                    </span>
                    <span className="tabular-nums text-muted-foreground">
                      {right}/{total}
                    </span>
                  </div>
                  <div
                    className="h-2.5 overflow-hidden rounded-full bg-surface-2"
                    role="progressbar"
                    aria-label={SKILLS[s].label}
                    aria-valuemin={0}
                    aria-valuemax={total}
                    aria-valuenow={right}
                  >
                    <div className="h-full rounded-full bg-primary" style={{ width: `${(right / total) * 100}%` }} />
                  </div>
                </li>
              )
            })}
          </ul>

          {tip && (
            <p className="mt-6 rounded-2xl bg-surface-2/70 p-4 text-sm">
              {SKILLS[weakest!.s].label} needs the most work.{" "}
              <Link to={tip.practise.to} className="font-semibold text-primary hover:underline">
                {tip.practise.label}
              </Link>
            </p>
          )}

          <div className="mt-7 flex flex-col gap-2.5">
            <Button asChild size="lg">
              <Link to="/path">Back to your path</Link>
            </Button>
            <Button asChild size="lg" variant="secondary">
              <Link to="/">Dashboard</Link>
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
