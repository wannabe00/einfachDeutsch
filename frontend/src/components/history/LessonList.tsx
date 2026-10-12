import { Check } from "lucide-react"

import type { HistoryLessonSummary } from "@/types"
import { Card } from "@/components/ui/Card"
import { EraArt } from "./EraArt"

/*
 * History lessons as article cards grouped by era: a picture and an excerpt,
 * opening the full read. The API only returns lessons at or below your level.
 */
export function LessonList({
  lessons,
  onOpen,
}: {
  lessons: HistoryLessonSummary[]
  onOpen: (id: number) => void
}) {
  const eras: string[] = []
  for (const l of lessons) if (!eras.includes(l.era)) eras.push(l.era)

  return (
    <div className="flex flex-col gap-8">
      {eras.map((era) => {
        const items = lessons.filter((l) => l.era === era)
        return (
          <section key={era}>
            <div className="mb-3 flex items-baseline gap-3">
              <h2 className="text-xl font-bold">
                {era || "Weitere"}
              </h2>
              <span className="text-sm text-muted-foreground">
                {items.length} {items.length === 1 ? "article" : "articles"}
              </span>
            </div>
            <div className="grid gap-4 sm:grid-cols-2">
              {items.map((lesson) => (
                <ArticleCard key={lesson.id} lesson={lesson} onOpen={onOpen} />
              ))}
            </div>
          </section>
        )
      })}
    </div>
  )
}

function ArticleCard({
  lesson,
  onOpen,
}: {
  lesson: HistoryLessonSummary
  onOpen: (id: number) => void
}) {
  return (
    <button
      onClick={() => onOpen(lesson.id)}
      className="group block h-full text-left"
    >
      <Card className="h-full transition-colors group-hover:border-muted-foreground/50">
        <div className="flex h-full flex-col">
          <div className="h-32 w-full overflow-hidden">
            <EraArt era={lesson.era} imageUrl={lesson.image_url || undefined} title={lesson.title} />
          </div>
          <div className="flex flex-1 flex-col p-4">
            <div className="flex items-start justify-between gap-2">
              <h3 className="font-bold leading-snug">{lesson.title}</h3>
              {lesson.completed && (
                <Check className="mt-0.5 size-4 shrink-0 text-[hsl(var(--success))]" />
              )}
            </div>
            {lesson.excerpt && (
              <p className="mt-1.5 line-clamp-3 text-sm text-muted-foreground">{lesson.excerpt}</p>
            )}
            <span className="mt-3 text-xs font-semibold uppercase tracking-wider text-muted-foreground">
              {lesson.cefr_level} · Read
            </span>
          </div>
        </div>
      </Card>
    </button>
  )
}
