import { useQuery } from "@tanstack/react-query"
import { FileText } from "lucide-react"

import { fetchLesenSets } from "@/api/curriculum"
import type { LesenSet } from "@/types"
import { ExamSetCard } from "@/components/exam/ExamSetCard"
import { PageHeader } from "@/components/layout/PageHeader"

/*
 * Lesen: exam-style reading, one set per Modul (A1 like Start Deutsch 1, A2
 * like Goethe A2). A set opens once its three Lektionen are finished; lower
 * levels are open for review.
 */
export default function LesenPage() {
  const { data, isLoading, isError } = useQuery({ queryKey: ["lesen"], queryFn: fetchLesenSets })
  const levels = [...new Set((data ?? []).map((s) => s.cefr_level))]

  return (
    <div className="flex flex-col gap-8">
      <PageHeader
        title="Lesen"
        subtitle="Reading like the Goethe exam: one set after every Modul. 60 % passes."
      />
      {isLoading && <p className="text-muted-foreground">Loading…</p>}
      {isError && <p className="text-muted-foreground">Couldn’t load the reading sets.</p>}
      {levels.map((level) => (
        <section key={level}>
          <h2 className="mb-3 px-1 text-[22px] font-bold">{level}</h2>
          <ul className="grid grid-cols-2 gap-3 sm:grid-cols-4">
            {data!
              .filter((s) => s.cefr_level === level)
              .map((s) => (
                <li key={s.modul}>
                  <SetCard set={s} />
                </li>
              ))}
          </ul>
        </section>
      ))}
    </div>
  )
}

function SetCard({ set }: { set: LesenSet }) {
  const status =
    set.best === null
      ? `${set.questions} questions`
      : `Best ${set.best}/${set.questions}${set.passed ? " · Bestanden" : ""}`
  return (
    <ExamSetCard
      to={`/lesen/${set.cefr_level}/${set.modul}`}
      icon={FileText}
      label="reading"
      modul={set.modul}
      first={set.first}
      last={set.last}
      locked={set.locked}
      status={status}
    />
  )
}
