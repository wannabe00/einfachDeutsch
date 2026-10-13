import { useState } from "react"
import { useQuery } from "@tanstack/react-query"

import { fetchCustomLessons, fetchHistoryLessons } from "@/api/history"
import { useAuth } from "@/contexts/AuthContext"
import type { HistoryLessonSummary } from "@/types"
import { PageHeader } from "@/components/layout/PageHeader"
import { LessonBuilder } from "@/components/history/LessonBuilder"
import { LessonList } from "@/components/history/LessonList"
import { LessonReader } from "@/components/history/LessonReader"

/*
 * German history: lessons written for each level (the API returns your level
 * and below, grouped here by level), lessons the AI wrote for you on request
 * (premium), and the box to ask for a new one.
 */
export default function HistoryPage() {
  const { user } = useAuth()
  const [open, setOpen] = useState<{ id: number; custom: boolean } | null>(null)
  const { data: lessons, isLoading } = useQuery({
    queryKey: ["history", "built-in"],
    queryFn: fetchHistoryLessons,
  })
  const { data: mine } = useQuery({
    queryKey: ["history", "custom"],
    queryFn: fetchCustomLessons,
    enabled: !!user?.has_premium,
  })

  if (open) {
    return <LessonReader id={open.id} custom={open.custom} onBack={() => setOpen(null)} />
  }

  // Your own level first, then the easier ones below it.
  const byLevel = new Map<string, HistoryLessonSummary[]>()
  for (const lesson of lessons ?? []) {
    byLevel.set(lesson.cefr_level, [...(byLevel.get(lesson.cefr_level) ?? []), lesson])
  }
  const levels = [...byLevel.keys()].sort().reverse()

  return (
    <div className="flex flex-col gap-8">
      <PageHeader
        title="German history"
        subtitle="Lessons written for your level, each with a picture, an English translation and a quiz."
      />

      <LessonBuilder onCreated={(id) => setOpen({ id, custom: true })} />

      {!!mine?.length && (
        <section>
          <h2 className="mb-3 px-1 text-[22px] font-bold">Your lessons</h2>
          <LessonList lessons={mine} onOpen={(id) => setOpen({ id, custom: true })} />
        </section>
      )}

      {isLoading ? (
        <p className="text-sm text-muted-foreground">Loading…</p>
      ) : levels.length === 0 ? (
        <p className="py-10 text-center text-sm text-muted-foreground">
          No history lessons for your level yet.
        </p>
      ) : (
        levels.map((level) => (
          <section key={level}>
            <h2 className="mb-3 px-1 text-[22px] font-bold">Level {level}</h2>
            <LessonList
              lessons={byLevel.get(level)!}
              onOpen={(id) => setOpen({ id, custom: false })}
            />
          </section>
        ))
      )}
    </div>
  )
}
