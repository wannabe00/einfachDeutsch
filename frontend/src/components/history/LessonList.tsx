import { Check } from "lucide-react"

import type { HistoryLessonSummary } from "@/types"
import { sectionColor } from "@/lib/sections"
import { SectionCard } from "@/components/ui/SectionCard"
import { EraArt } from "./EraArt"

/*
 * History v2 (Phase 23.12) — era-grouped **news-article cards**: hero image +
 * excerpt, opening the full read. Level-gating is server-side (23.8), so a B1
 * user never receives C1 lessons.
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
      {eras.map((era, i) => {
        const accent = sectionColor(i)
        const items = lessons.filter((l) => l.era === era)
        return (
          <section key={era}>
            <div className="mb-3 flex items-baseline gap-3">
              <h2 className="text-xl font-bold" style={{ color: accent }}>
                {era || "Weitere"}
              </h2>
              <span className="text-sm text-muted-foreground">
                {items.length} {items.length === 1 ? "article" : "articles"}
              </span>
            </div>
            <div className="grid gap-4 sm:grid-cols-2">
              {items.map((lesson) => (
                <ArticleCard key={lesson.id} lesson={lesson} accent={accent} onOpen={onOpen} />
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
  accent,
  onOpen,
}: {
  lesson: HistoryLessonSummary
  accent: string
  onOpen: (id: number) => void
}) {
  return (
    <button
      onClick={() => onOpen(lesson.id)}
      className="group block h-full text-left transition-transform hover:-translate-y-0.5"
    >
      <SectionCard accent={accent} className="h-full">
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
      </SectionCard>
    </button>
  )
}
