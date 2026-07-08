import { ArrowLeft } from "lucide-react"
import { useQuery } from "@tanstack/react-query"

import { fetchHistoryLesson } from "@/api/history"
import { useAuth } from "@/contexts/AuthContext"
import type { CEFRLevel } from "@/types"
import { LessonQuiz } from "./LessonQuiz"

// English is shown alongside German through A2; German-only from B1.
const ENGLISH_LEVELS: CEFRLevel[] = ["A1", "A2"]

/** Reads one history lesson: German body always, English alongside through A2,
    then the quiz. */
export function LessonReader({ id, onBack }: { id: number; onBack: () => void }) {
  const { user } = useAuth()
  const { data: lesson, isLoading } = useQuery({
    queryKey: ["history", id],
    queryFn: () => fetchHistoryLesson(id),
  })

  const showEnglish = !!user && ENGLISH_LEVELS.includes(user.cefr_level)

  return (
    <div>
      <button
        onClick={onBack}
        className="inline-flex items-center gap-1.5 text-sm text-muted-foreground hover:text-accent"
      >
        <ArrowLeft className="size-4" /> All lessons
      </button>

      {isLoading || !lesson ? (
        <p className="mt-6 text-sm text-muted-foreground">Loading…</p>
      ) : (
        <>
          <h1 className="mt-4 text-2xl font-semibold tracking-tight">{lesson.title}</h1>
          <p className="mt-1 text-xs font-semibold uppercase tracking-wide text-muted-foreground">
            {lesson.era}
          </p>

          <div className="mt-5 rounded-xl border border-border bg-surface p-5">
            <p className="whitespace-pre-wrap leading-relaxed">{lesson.body_de}</p>
            {showEnglish && lesson.body_en && (
              <div className="mt-4 border-t border-border pt-4">
                <p className="mb-1 text-xs font-medium uppercase tracking-wide text-muted-foreground">
                  English (shown through A2)
                </p>
                <p className="whitespace-pre-wrap leading-relaxed text-muted-foreground">
                  {lesson.body_en}
                </p>
              </div>
            )}
          </div>

          {lesson.quiz.length > 0 && <LessonQuiz lessonId={lesson.id} quiz={lesson.quiz} />}
        </>
      )}
    </div>
  )
}
