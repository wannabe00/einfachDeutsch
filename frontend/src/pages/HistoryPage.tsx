import { useState } from "react"
import { useQuery } from "@tanstack/react-query"

import { fetchHistoryLessons } from "@/api/history"
import { PageHeader } from "@/components/layout/PageHeader"
import { LessonList } from "@/components/history/LessonList"
import { LessonReader } from "@/components/history/LessonReader"

/*
 * History lessons as article cards that open the full read and a quiz. The API
 * only returns lessons at or below your level.
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
        subtitle="Short reads on German history, each followed by a quick quiz."
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
