import { useState } from "react"
import { useQuery } from "@tanstack/react-query"

import { fetchHistoryLessons } from "@/api/history"
import { PageHeader } from "@/components/layout/PageHeader"
import { LessonList } from "@/components/history/LessonList"
import { LessonReader } from "@/components/history/LessonReader"

/*
 * History v2 (Phase 23.12) — a feed of article cards (hero + excerpt) that open
 * the full read + quiz. Level-gated server-side (23.8): only lessons at or below
 * your level are returned.
 */
export default function HistoryPage() {
  const [selectedId, setSelectedId] = useState<number | null>(null)
  const { data: lessons, isLoading } = useQuery({
    queryKey: ["history"],
    queryFn: fetchHistoryLessons,
  })

  if (selectedId !== null) {
    return <LessonReader id={selectedId} onBack={() => setSelectedId(null)} />
  }

  return (
    <div className="flex flex-col gap-6">
      <PageHeader
        title="German history"
        subtitle="Short reads on German history — then a quick quiz. Available any day."
      />
      {isLoading ? (
        <p className="text-sm text-muted-foreground">Loading…</p>
      ) : (lessons ?? []).length === 0 ? (
        <p className="py-10 text-center text-sm text-muted-foreground">
          No history lessons for your level yet.
        </p>
      ) : (
        <LessonList lessons={lessons ?? []} onOpen={setSelectedId} />
      )}
    </div>
  )
}
