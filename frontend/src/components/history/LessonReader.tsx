import { useState } from "react"
import { ArrowLeft } from "lucide-react"
import { useQuery } from "@tanstack/react-query"

import { fetchHistoryLesson } from "@/api/history"
import { Button } from "@/components/ui/button"
import { EraArt } from "./EraArt"
import { LessonQuiz } from "./LessonQuiz"

/** Reads one history lesson: its picture, the German text with an English
    translation behind a button, then the quiz. */
export function LessonReader({ id, onBack }: { id: number; onBack: () => void }) {
  const [showEnglish, setShowEnglish] = useState(false)
  const { data: lesson, isLoading } = useQuery({
    queryKey: ["history", id],
    queryFn: () => fetchHistoryLesson(id),
  })

  return (
    <div className="mx-auto max-w-3xl">
      <button
        onClick={onBack}
        className="inline-flex items-center gap-1.5 text-sm text-muted-foreground hover:text-foreground"
      >
        <ArrowLeft className="size-4" /> All lessons
      </button>

      {isLoading || !lesson ? (
        <p className="mt-6 text-sm text-muted-foreground">Loading…</p>
      ) : (
        <article className="mt-4">
          <p className="text-xs font-semibold uppercase tracking-wide text-muted-foreground">
            {lesson.era}
          </p>
          <h1 className="mt-1 text-2xl font-bold tracking-tight sm:text-3xl">{lesson.title}</h1>

          <figure className="mt-5">
            <div className="aspect-[16/9] overflow-hidden rounded-xl border border-border bg-surface">
              <EraArt
                era={lesson.era}
                imageUrl={lesson.image_url || undefined}
                title={lesson.title}
                fit="contain"
              />
            </div>
            {lesson.image_credit && (
              <figcaption className="mt-1.5 text-xs text-muted-foreground">
                {lesson.image_credit}
              </figcaption>
            )}
          </figure>

          <div className="mt-6 space-y-4 text-[1.05rem] leading-relaxed">
            {lesson.body_de.split(/\n\s*\n/).map((p) => (
              <p key={p}>{p}</p>
            ))}
          </div>

          {lesson.body_en && (
            <div className="mt-6 border-t border-border pt-5">
              <Button variant="secondary" onClick={() => setShowEnglish((v) => !v)}>
                {showEnglish ? "Hide English" : "Show English"}
              </Button>
              {showEnglish && (
                <div className="mt-4 space-y-4 leading-relaxed text-muted-foreground">
                  {lesson.body_en.split(/\n\s*\n/).map((p) => (
                    <p key={p}>{p}</p>
                  ))}
                </div>
              )}
            </div>
          )}

          {lesson.quiz.length > 0 && <LessonQuiz lessonId={lesson.id} quiz={lesson.quiz} />}
        </article>
      )}
    </div>
  )
}
