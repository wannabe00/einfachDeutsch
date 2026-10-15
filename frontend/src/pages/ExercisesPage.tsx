import { useState } from "react"
import { Link } from "react-router-dom"
import { useMutation, useQuery } from "@tanstack/react-query"
import { ArrowRight, BookOpenCheck, Keyboard, Layers, Repeat, Target } from "lucide-react"

import { answerPractice, fetchPracticeOptions, startPractice } from "@/api/curriculum"
import type { AnswerResult, PracticeOptions, PracticeTask } from "@/types"
import { useAuth } from "@/contexts/AuthContext"
import { AnswerFeedback } from "@/components/exercises/AnswerFeedback"
import { ExerciseInput } from "@/components/exercises/ExerciseInput"
import { LockedFeature } from "@/components/auth/LockedFeature"
import { PageHeader } from "@/components/layout/PageHeader"
import { Button } from "@/components/ui/button"
import { Card } from "@/components/ui/card"
import { Select, type SelectOption } from "@/components/ui/Select"
import { LektionCover } from "@/components/lektion/LektionCover"
import { SessionBar } from "@/components/ui/SessionBar"
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

const FACTS = [
  { icon: Target, title: "No hints", body: "A bit harder than the lessons." },
  { icon: Keyboard, title: "More typing", body: "Mostly writing and word order." },
  { icon: Repeat, title: "Mistakes return", body: "Wrong answers come back more often." },
]

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

  const unitOptions: SelectOption<number>[] = [
    {
      value: 0,
      label: "All finished units",
      leading: (
        <span className="flex h-9 w-7 shrink-0 items-center justify-center rounded-md bg-border/70 text-muted-foreground">
          <Layers className="size-4" aria-hidden="true" />
        </span>
      ),
    },
    ...(options?.units ?? []).map((u) => ({
      value: u.id,
      label: `Lektion ${u.order}: ${u.title}`,
      group: u.cefr_level,
      leading: <LektionCover order={u.order} level={u.cefr_level} size="sm" className="h-9 w-7 shrink-0 rounded-md" />,
    })),
  ]
  const topicOptions: SelectOption<number>[] = [
    { value: 0, label: "Any topic" },
    ...(options?.topics ?? []).map((t) => ({
      value: t.id,
      label: t.title,
      description: `${t.cefr_level} · Lektion ${t.lektion}`,
      group: t.cefr_level,
    })),
  ]

  return (
    <div className="mx-auto flex max-w-2xl flex-col gap-6">
      <PageHeader
        title="Practice"
        subtitle="Short sets of about ten tasks from the lessons you've finished."
      />

      <ul className="grid gap-3 sm:grid-cols-3">
        {FACTS.map(({ icon: Icon, title, body }, i) => (
          <li key={title} className="flex items-start gap-3 rounded-2xl bg-surface p-4 shadow-card sm:flex-col">
            <span
              className="flex size-10 shrink-0 items-center justify-center rounded-xl text-white"
              style={{ background: `hsl(var(--section-${i + 1}))` }}
            >
              <Icon className="size-5" aria-hidden="true" />
            </span>
            <span>
              <span className="block font-semibold">{title}</span>
              <span className="block text-sm text-muted-foreground">{body}</span>
            </span>
          </li>
        ))}
      </ul>

      {options && options.units.length === 0 ? (
        <Card>
          <div className="flex flex-col items-center gap-2 px-6 py-10 text-center">
            <span className="flex size-14 items-center justify-center rounded-2xl bg-surface-2 text-muted-foreground">
              <BookOpenCheck className="size-7" aria-hidden="true" />
            </span>
            <p className="mt-2 text-xl font-bold">Nothing to practise yet</p>
            <p className="text-muted-foreground">
              Practice uses the lessons you've finished. Finish your first lesson to start.
            </p>
            <Button asChild size="lg" className="mt-4">
              <Link to="/path">
                Go to your path <ArrowRight />
              </Link>
            </Button>
          </div>
        </Card>
      ) : (
        <Card>
          <div className="flex flex-col gap-5 p-6 sm:p-7">
            <h2 className="text-xl font-bold">Build a set</h2>
            <div className="flex flex-col gap-1.5">
              <span className="text-sm font-medium text-muted-foreground">Unit</span>
              <Select label="Unit" value={unit ?? 0} onChange={(v) => setUnit(v || undefined)} options={unitOptions} />
            </div>
            {!!options?.topics.length && (
              <div className="flex flex-col gap-1.5">
                <span className="text-sm font-medium text-muted-foreground">Grammar topic</span>
                <Select
                  label="Grammar topic"
                  value={topic ?? 0}
                  onChange={(v) => setTopic(v || undefined)}
                  options={topicOptions}
                />
              </div>
            )}
            <Button size="lg" className="mt-1" disabled={!options || start.isPending} onClick={() => start.mutate()}>
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
      <div className="mx-auto max-w-md py-8">
        <Card>
          <div className="p-8 text-center">
            <span className="mx-auto flex size-24 items-center justify-center rounded-full bg-primary/10 font-grotesk text-3xl font-extrabold tabular-nums text-primary animate-in zoom-in-50 fade-in-0 duration-500">
              {score.total > 0 ? Math.round((score.right / score.total) * 100) : 0}%
            </span>
            <h1 className="mt-6 text-3xl font-extrabold">Set done</h1>
            <p className="mt-2 text-muted-foreground">
              {score.right} of {score.total} right
            </p>
            <p className="mt-1 text-sm text-muted-foreground">
              What you got wrong will come up more often in your next sets.
            </p>
            <Button size="lg" className="mt-7 w-full" onClick={onDone}>
              Another set
            </Button>
          </div>
        </Card>
      </div>
    )
  }

  return (
    <div className="mx-auto flex max-w-2xl flex-col gap-8">
      <SessionBar
        onClose={onDone}
        closeLabel="End this set"
        title="Practice"
        progress={(step / tasks.length) * 100}
        counter={`${step + 1}/${tasks.length}`}
      />
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
      <div className="p-6 sm:p-8">
        <p className="text-xl font-bold leading-snug sm:text-2xl">{task.prompt}</p>
        <div className="mt-5">
          <ExerciseInput
            content={task}
            value={answer}
            onChange={setAnswer}
            disabled={!!feedback}
            autoFocus
            onSubmit={check}
            results={feedback?.parts}
            solution={feedback?.solution}
          />
        </div>
        {feedback && <AnswerFeedback feedback={feedback} content={task} />}
        <div className="mt-8">
          {feedback ? (
            <Button size="lg" className="w-full" onClick={() => onNext(feedback)}>
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
