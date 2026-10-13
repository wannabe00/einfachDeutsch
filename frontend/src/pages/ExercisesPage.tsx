import { useState } from "react"
import { Link } from "react-router-dom"
import { useMutation, useQuery } from "@tanstack/react-query"

import { answerPractice, fetchPracticeOptions, startPractice } from "@/api/curriculum"
import type { AnswerResult, PracticeOptions, PracticeTask } from "@/types"
import { useAuth } from "@/contexts/AuthContext"
import { AnswerFeedback } from "@/components/exercises/AnswerFeedback"
import { ExerciseInput } from "@/components/exercises/ExerciseInput"
import { LockedFeature } from "@/components/auth/LockedFeature"
import { PageHeader } from "@/components/layout/PageHeader"
import { Button } from "@/components/ui/button"
import { Card } from "@/components/ui/card"
import { isAnswered } from "@/lib/exercises"

/*
 * Practice: short sets of about ten tasks from lessons you've finished, mixed
 * across units. A bit harder than the lessons: no hints, mostly typing and word
 * order, and what you got wrong comes back more often. The server picks the
 * tasks and grades each one.
 */
export default function ExercisesPage() {
  const { user } = useAuth()
  const [tasks, setTasks] = useState<PracticeTask[] | null>(null)
  const { data: options } = useQuery({
    queryKey: ["practice-options"],
    queryFn: fetchPracticeOptions,
    enabled: !!user,
  })

  if (!user) {
    return (
      <LockedFeature
        title="Practice needs an account"
        description="Practice sets are built from the lessons you've finished, so they need your progress."
      />
    )
  }

  if (tasks) return <PracticeSet tasks={tasks} onDone={() => setTasks(null)} />
  return <StartScreen options={options} onStart={setTasks} />
}

function StartScreen({
  options,
  onStart,
}: {
  options?: PracticeOptions
  onStart: (tasks: PracticeTask[]) => void
}) {
  const [unit, setUnit] = useState<number | undefined>()
  const [topic, setTopic] = useState<number | undefined>()
  const start = useMutation({
    mutationFn: () => startPractice({ unit, topic }),
    onSuccess: (tasks) => {
      if (tasks.length > 0) onStart(tasks)
    },
  })

  const selectClass =
    "rounded-lg border border-border bg-surface px-3 py-2 text-sm focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring"

  return (
    <div className="mx-auto flex max-w-xl flex-col gap-6">
      <PageHeader
        title="Practice"
        subtitle="Short sets from what you've finished. No hints, more typing."
      />

      {options && options.units.length === 0 ? (
        <Card>
          <div className="p-6 text-center">
            <p className="font-medium">Nothing to practise yet.</p>
            <p className="mt-1 text-sm text-muted-foreground">
              Practice uses the lessons you've finished. Finish your first lesson to start.
            </p>
            <Button asChild className="mt-5">
              <Link to="/path">Go to your path</Link>
            </Button>
          </div>
        </Card>
      ) : (
        <Card>
          <div className="flex flex-col gap-4 p-6">
            <label className="flex flex-col gap-1.5 text-sm font-medium">
              Unit
              <select
                className={selectClass}
                value={unit ?? ""}
                onChange={(e) => setUnit(e.target.value ? Number(e.target.value) : undefined)}
              >
                <option value="">All finished units</option>
                {options?.units.map((u) => (
                  <option key={u.id} value={u.id}>
                    Lektion {u.order}: {u.title}
                  </option>
                ))}
              </select>
            </label>
            {!!options?.topics.length && (
              <label className="flex flex-col gap-1.5 text-sm font-medium">
                Grammar topic
                <select
                  className={selectClass}
                  value={topic ?? ""}
                  onChange={(e) => setTopic(e.target.value ? Number(e.target.value) : undefined)}
                >
                  <option value="">Any topic</option>
                  {options.topics.map((t) => (
                    <option key={t.id} value={t.id}>
                      {t.title}
                    </option>
                  ))}
                </select>
              </label>
            )}
            <Button disabled={!options || start.isPending} onClick={() => start.mutate()}>
              {start.isPending ? "Building your set…" : "Start a set"}
            </Button>
            {start.data?.length === 0 && (
              <p className="text-sm text-muted-foreground">
                Nothing matches that unit and topic together. Try a wider choice.
              </p>
            )}
          </div>
        </Card>
      )}
    </div>
  )
}

function PracticeSet({ tasks, onDone }: { tasks: PracticeTask[]; onDone: () => void }) {
  const [step, setStep] = useState(0)
  const [score, setScore] = useState({ right: 0, total: 0 })

  if (step >= tasks.length) {
    return (
      <div className="mx-auto max-w-md">
        <Card>
          <div className="p-8 text-center">
            <h1 className="text-2xl font-bold">Set done</h1>
            <p className="mt-2 text-muted-foreground">
              {score.right}/{score.total} right
            </p>
            <p className="mt-1 text-sm text-muted-foreground">
              What you got wrong will come up more often in your next sets.
            </p>
            <Button className="mt-6" onClick={onDone}>
              Another set
            </Button>
          </div>
        </Card>
      </div>
    )
  }

  return (
    <div className="mx-auto flex max-w-2xl flex-col gap-6">
      <div className="flex items-center gap-4">
        <div className="h-2 flex-1 overflow-hidden rounded-full bg-border">
          <div
            className="h-2 rounded-full bg-primary transition-all duration-300"
            style={{ width: `${(step / tasks.length) * 100}%` }}
          />
        </div>
        <span className="text-xs tabular-nums text-muted-foreground">
          {step + 1}/{tasks.length}
        </span>
      </div>
      <TaskStep
        key={tasks[step].task_id}
        task={tasks[step]}
        onNext={(result) => {
          setScore((s) => ({
            right: s.right + result.parts.filter(Boolean).length,
            total: s.total + result.parts.length,
          }))
          setStep(step + 1)
        }}
      />
      <button onClick={onDone} className="text-center text-xs text-muted-foreground underline">
        End this set
      </button>
    </div>
  )
}

function TaskStep({
  task,
  onNext,
}: {
  task: PracticeTask
  onNext: (result: AnswerResult) => void
}) {
  const [answer, setAnswer] = useState<unknown>(
    task.type === "sentence_order" || task.type === "group" ? [] : "",
  )
  const [feedback, setFeedback] = useState<AnswerResult | null>(null)
  const ready = isAnswered(task, answer)

  async function check() {
    if (!ready || feedback) return
    setFeedback(await answerPractice(task.task_id, answer))
  }

  return (
    <Card>
      <div className="p-6">
        <p className="text-lg font-semibold">{task.prompt}</p>
        <div className="mt-5">
          <ExerciseInput
            content={task}
            value={answer}
            onChange={setAnswer}
            disabled={!!feedback}
            autoFocus
            onSubmit={check}
            results={task.type === "group" ? feedback?.parts : undefined}
          />
        </div>
        {feedback && <AnswerFeedback feedback={feedback} content={task} />}
        <div className="mt-6">
          {feedback ? (
            <Button onClick={() => onNext(feedback)}>Continue</Button>
          ) : (
            <Button disabled={!ready} onClick={check}>
              Check
            </Button>
          )}
        </div>
      </div>
    </Card>
  )
}
