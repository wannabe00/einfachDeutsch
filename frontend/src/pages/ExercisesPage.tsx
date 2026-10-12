import { useState } from "react"
import { useQuery } from "@tanstack/react-query"

import { fetchExercises } from "@/api/exercises"
import { fetchBooks } from "@/api/books"
import type { Chapter, ExerciseType } from "@/types"
import { EXERCISE_TYPES } from "@/lib/labels"
import { ChapterButtons } from "@/components/layout/ChapterButtons"
import { ExerciseCard } from "@/components/exercises/ExerciseCard"
import { ExerciseForm } from "@/components/exercises/ExerciseForm"
import { PageHeader } from "@/components/layout/PageHeader"
import { Button } from "@/components/ui/button"
import { useAIPanel } from "@/contexts/AIPanelContext"
import { Sparkles } from "lucide-react"

export default function ExercisesPage() {
  // Exercises are always shown for one chapter; there's no "all chapters" view.
  const [chapterId, setChapterId] = useState<number | undefined>()
  const [type, setType] = useState<ExerciseType | undefined>()
  const [showForm, setShowForm] = useState(false)

  const { openPanel } = useAIPanel()
  const { data: books } = useQuery({ queryKey: ["books"], queryFn: fetchBooks })
  const { data: exercises, isLoading } = useQuery({
    queryKey: ["exercises", chapterId, type],
    queryFn: () => fetchExercises(chapterId, type),
    enabled: chapterId !== undefined,
  })

  const allChapters: Chapter[] = books?.flatMap((b) => b.chapters) ?? []
  const chapterTitle = (id: number) =>
    allChapters.find((c) => c.id === id)?.title ?? "Unknown chapter"

  // --- Chapter chooser: shown until a chapter is selected -----------------
  if (chapterId === undefined) {
    return (
      <div className="flex flex-col gap-6">
        <PageHeader title="Exercises" subtitle="Choose a chapter to practice." />

        {books && (
          <ChapterButtons
            books={books}
            selected={-1}
            onSelect={(v) => {
              if (v !== "all") setChapterId(v)
            }}
            includeAll={false}
          />
        )}
      </div>
    )
  }

  const selectClass =
    "rounded-lg border border-border bg-surface px-3 py-1.5 text-sm focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring"

  return (
    <div className="flex flex-col gap-6">
      <PageHeader
        title="Exercises"
        subtitle={
          <button
            onClick={() => {
              setChapterId(undefined)
              setType(undefined)
            }}
            className="hover:text-primary"
          >
            {chapterTitle(chapterId)} · change
          </button>
        }
        actions={
          <>
            <Button
              variant="secondary"
              onClick={() =>
                openPanel(
                  "AI · Generate exercises",
                  `Generate 5 practice exercises for chapter: ${chapterTitle(chapterId)}`,
                )
              }
            >
              <Sparkles className="mr-2 size-4" /> Generate Exercises
            </Button>
            <Button onClick={() => setShowForm((v) => !v)}>
              {showForm ? "Cancel" : "Add Exercise"}
            </Button>
          </>
        }
      />

      {showForm && allChapters.length > 0 && (
        <div className="rounded-xl border border-border bg-surface p-4">
          <ExerciseForm
            chapters={allChapters}
            defaultChapterId={chapterId}
            onDone={() => setShowForm(false)}
          />
        </div>
      )}

      <div className="flex flex-wrap items-center gap-3">
        <select
          value={type ?? ""}
          onChange={(e) =>
            setType((e.target.value || undefined) as ExerciseType | undefined)
          }
          className={selectClass}
        >
          <option value="">All types</option>
          {EXERCISE_TYPES.map((t) => (
            <option key={t.value} value={t.value}>
              {t.label}
            </option>
          ))}
        </select>
      </div>

      <div className="flex flex-col gap-4">
        {isLoading ? (
          <p className="text-sm text-muted-foreground">Loading…</p>
        ) : !exercises?.length ? (
          <p className="text-sm text-muted-foreground">
            No exercises in this chapter yet. Add one above.
          </p>
        ) : (
          exercises.map((ex) => <ExerciseCard key={ex.id} exercise={ex} />)
        )}
      </div>
    </div>
  )
}
