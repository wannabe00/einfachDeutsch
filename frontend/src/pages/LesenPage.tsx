import { Link } from "react-router-dom"
import { useQuery } from "@tanstack/react-query"
import { FileText, Lock } from "lucide-react"

import { fetchLesenSets } from "@/api/curriculum"
import type { LesenSet } from "@/types"
import { PageHeader } from "@/components/layout/PageHeader"
import { cn } from "@/lib/utils"

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
  const status = set.locked
    ? `After Lektion ${set.last}`
    : set.best === null
      ? `${set.questions} questions`
      : `Best ${set.best}/${set.questions}${set.passed ? " · Bestanden" : ""}`
  const body = (
    <>
      <span
        className={cn(
          "mb-1 flex size-10 items-center justify-center rounded-xl",
          set.locked ? "bg-surface-2 text-muted-foreground" : "bg-primary text-primary-foreground",
        )}
      >
        {set.locked ? <Lock className="size-5" aria-hidden="true" /> : <FileText className="size-5" aria-hidden="true" />}
      </span>
      <span className="font-semibold">Modul {set.modul}</span>
      <span className="text-sm text-muted-foreground">
        Lektionen {set.first}–{set.last}
      </span>
      <span className={cn("mt-1 text-sm font-semibold", set.locked ? "text-muted-foreground" : "text-foreground")}>
        {status}
      </span>
    </>
  )
  const card = "flex h-full w-full flex-col items-start gap-1 rounded-[20px] bg-surface p-4 text-left shadow-card"
  if (set.locked) {
    return (
      <div className={cn(card, "opacity-70")} aria-label={`Modul ${set.modul} reading, locked until Lektion ${set.last}`}>
        {body}
      </div>
    )
  }
  return (
    <Link to={`/lesen/${set.cefr_level}/${set.modul}`} className={cn(card, "transition-colors hover:bg-surface-2")}>
      {body}
    </Link>
  )
}
