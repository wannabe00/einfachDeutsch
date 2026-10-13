import { Check } from "lucide-react"

import type { HistoryCard } from "@/types"
import { cn } from "@/lib/utils"
import { Card } from "@/components/ui/card"
import { EraArt } from "./EraArt"

/*
 * History lessons as one continuous grid of article cards in era order, each
 * labelled with its era, so an era with a single story never leaves half a row
 * empty. With an odd number of stories the first one is featured across the
 * full width, so the grid always ends on a full row.
 */
export function LessonList({
  lessons,
  onOpen,
}: {
  lessons: HistoryCard[]
  onOpen: (id: number) => void
}) {
  const featureFirst = lessons.length % 2 === 1

  return (
    <div className="grid gap-5 sm:grid-cols-2">
      {lessons.map((lesson, i) => (
        <ArticleCard
          key={lesson.id}
          lesson={lesson}
          onOpen={onOpen}
          featured={featureFirst && i === 0}
        />
      ))}
    </div>
  )
}

function ArticleCard({
  lesson,
  onOpen,
  featured,
}: {
  lesson: HistoryCard
  onOpen: (id: number) => void
  featured: boolean
}) {
  return (
    <button
      onClick={() => onOpen(lesson.id)}
      className={cn("lift block h-full rounded-[24px] text-left", featured && "sm:col-span-2")}
    >
      <Card className="h-full overflow-hidden rounded-[24px]">
        <div className={cn("flex h-full flex-col", featured && "sm:flex-row")}>
          <div
            className={cn(
              "relative h-44 w-full shrink-0 overflow-hidden",
              featured && "sm:h-auto sm:min-h-[260px] sm:w-1/2",
            )}
          >
            <EraArt era={lesson.era} imageUrl={lesson.image_url || undefined} title={lesson.title} />
            {lesson.completed && (
              <span className="absolute right-3 top-3 inline-flex items-center gap-1 rounded-full bg-black/55 px-2.5 py-1 text-xs font-semibold text-white backdrop-blur-md">
                <Check className="size-3.5" aria-hidden="true" /> Read
              </span>
            )}
          </div>
          <div className={cn("flex flex-1 flex-col p-5", featured && "sm:justify-center sm:p-8")}>
            {lesson.era && (
              <span className="text-xs font-semibold uppercase tracking-[0.04em] text-muted-foreground">
                {lesson.era}
              </span>
            )}
            <h3 className={cn("mt-1 font-bold leading-snug", featured ? "text-2xl sm:text-3xl" : "text-lg")}>
              {lesson.title}
            </h3>
            {lesson.excerpt && (
              <p
                className={cn(
                  "mt-1.5 text-[15px] text-muted-foreground",
                  featured ? "line-clamp-4 sm:text-base" : "line-clamp-3",
                )}
              >
                {lesson.excerpt}
              </p>
            )}
            <span className="mt-auto flex items-center gap-2 pt-4 text-sm">
              <span className="rounded-full bg-surface-2 px-2.5 py-0.5 text-xs font-semibold text-muted-foreground">
                {lesson.cefr_level}
              </span>
              <span className="font-semibold text-primary">{lesson.completed ? "Read again" : "Read"}</span>
            </span>
          </div>
        </div>
      </Card>
    </button>
  )
}
