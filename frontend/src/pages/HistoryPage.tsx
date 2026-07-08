import { useState } from "react"
import { useQuery } from "@tanstack/react-query"

import { fetchHistoryLessons } from "@/api/history"
import { LessonList } from "@/components/history/LessonList"
import { LessonReader } from "@/components/history/LessonReader"

export default function HistoryPage() {
  const [selectedId, setSelectedId] = useState<number | null>(null)
  const { data: lessons } = useQuery({
    queryKey: ["history"],
    queryFn: fetchHistoryLessons,
  })

  if (selectedId !== null) {
    return <LessonReader id={selectedId} onBack={() => setSelectedId(null)} />
  }

  return (
    <div>
      <h1 className="text-2xl font-semibold tracking-tight">German history</h1>
      <p className="mt-1 text-sm text-muted-foreground">
        Short lessons on German history — read, then take a quick quiz. Available
        any day (no schedule).
      </p>
      <LessonList lessons={lessons ?? []} onOpen={setSelectedId} />
    </div>
  )
}
