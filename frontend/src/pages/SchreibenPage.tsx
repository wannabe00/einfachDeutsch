import { useQuery } from "@tanstack/react-query"
import { PenLine } from "lucide-react"

import { fetchSchreibenSets } from "@/api/curriculum"
import type { SchreibenSet } from "@/types"
import { ExamSetCard } from "@/components/exam/ExamSetCard"
import { PageHeader } from "@/components/layout/PageHeader"

/*
 * Schreiben: exam-style writing, one set per Modul (A1 like Start Deutsch 1:
 * a form and a short message; A2 like Goethe A2: an SMS and an e-mail).
 * Unlocks like Lesen.
 */
export default function SchreibenPage() {
  const { data, isLoading, isError } = useQuery({ queryKey: ["schreiben"], queryFn: fetchSchreibenSets })
  const levels = [...new Set((data ?? []).map((s) => s.cefr_level))]

  return (
    <div className="flex flex-col gap-8">
      <PageHeader
        title="Schreiben"
        subtitle="Writing like the Goethe exam: one set after every Modul. Check yourself against a model answer, or let the AI grade you (Premium)."
      />
      {isLoading && <p className="text-muted-foreground">Loading…</p>}
      {isError && <p className="text-muted-foreground">Couldn’t load the writing sets.</p>}
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

function SetCard({ set }: { set: SchreibenSet }) {
  const status =
    set.best === null ? `${set.teile.length} Teile` : `Best ${set.best}/${set.out_of}${set.passed ? " · Bestanden" : ""}`
  return (
    <ExamSetCard
      to={`/schreiben/${set.cefr_level}/${set.modul}`}
      icon={PenLine}
      label="writing"
      modul={set.modul}
      first={set.first}
      last={set.last}
      locked={set.locked}
      status={status}
    />
  )
}
