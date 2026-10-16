import { useQuery } from "@tanstack/react-query"

import type { LesenSet } from "@/types"
import { QUIZ_SKILLS, type QuizSkill } from "@/lib/examSkills"
import { ExamSetCard } from "@/components/exam/ExamSetCard"
import { PageHeader } from "@/components/layout/PageHeader"

/*
 * Lesen and Hören: exam-style sets, one per Modul (A1 like Start Deutsch 1, A2
 * like Goethe A2). A set opens once its three Lektionen are finished; lower
 * levels are open for review.
 */
export default function QuizSetsPage({ skill }: { skill: QuizSkill }) {
  const def = QUIZ_SKILLS[skill]
  const { data, isLoading, isError } = useQuery({ queryKey: [skill], queryFn: def.fetchSets })
  const levels = [...new Set((data ?? []).map((s) => s.cefr_level))]

  return (
    <div className="flex flex-col gap-8">
      <PageHeader title={def.title} subtitle={def.subtitle} />
      {isLoading && <p className="text-muted-foreground">Loading…</p>}
      {isError && <p className="text-muted-foreground">Couldn’t load the {def.label} sets.</p>}
      {data?.length === 0 && <p className="text-muted-foreground">No {def.label} sets yet. They’re on the way.</p>}
      {levels.map((level) => (
        <section key={level}>
          <h2 className="mb-3 px-1 text-[22px] font-bold">{level}</h2>
          <ul className="grid grid-cols-2 gap-3 sm:grid-cols-4">
            {data!
              .filter((s) => s.cefr_level === level)
              .map((s) => (
                <li key={s.modul}>
                  <SetCard set={s} skill={skill} />
                </li>
              ))}
          </ul>
        </section>
      ))}
    </div>
  )
}

function SetCard({ set, skill }: { set: LesenSet; skill: QuizSkill }) {
  const def = QUIZ_SKILLS[skill]
  const status =
    set.best === null
      ? `${set.questions} questions`
      : `Best ${set.best}/${set.questions}${set.passed ? " · Bestanden" : ""}`
  return (
    <ExamSetCard
      to={`${def.path}/${set.cefr_level}/${set.modul}`}
      icon={def.icon}
      label={def.label}
      modul={set.modul}
      first={set.first}
      last={set.last}
      locked={set.locked}
      status={status}
    />
  )
}
