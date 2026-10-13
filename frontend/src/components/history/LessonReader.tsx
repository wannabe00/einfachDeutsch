import { useState } from "react"
import { useQuery } from "@tanstack/react-query"

import { fetchHistoryLesson } from "@/api/history"
import { Button } from "@/components/ui/button"
import { BackLink } from "@/components/ui/BackLink"
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
      <BackLink onClick={onBack} label="History" />

      {isLoading || !lesson ? (
        <p className="mt-6 text-sm text-muted-foreground">Loading…</p>
      ) : (
        <article className="mt-4">
          <p className="text-[13px] font-semibold uppercase tracking-[0.04em] text-muted-foreground">
            {lesson.era}
          </p>
          <h1 className="mt-1 text-3xl font-extrabold sm:text-4xl">{lesson.title}</h1>

          <figure className="mt-5">
            <div className="aspect-[16/9] overflow-hidden rounded-[24px] bg-surface shadow-card">
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

          <div className="mx-auto mt-8 max-w-2xl space-y-5 text-lg leading-8">
            {lesson.body_de.split(/\n\s*\n/).map((p) => (
              <p key={p}>{p}</p>
            ))}
          </div>

          {lesson.body_en && (
            <div className="mx-auto mt-8 max-w-2xl">
              <Button variant="secondary" onClick={() => setShowEnglish((v) => !v)}>
                {showEnglish ? "Hide English" : "Show English"}
              </Button>
              {showEnglish && (
                <div className="mt-4 space-y-4 rounded-2xl bg-surface-2/70 p-5 leading-relaxed text-muted-foreground animate-in fade-in-0 duration-200">
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
