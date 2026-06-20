import { useState } from "react"
import { useQuery } from "@tanstack/react-query"

import { fetchExercises } from "@/api/exercises"
import { fetchBooks } from "@/api/books"
import type { Chapter, ExerciseType } from "@/types"
import { EXERCISE_TYPES } from "@/lib/labels"
import { ChapterButtons } from "@/components/layout/ChapterButtons"
import { ExerciseCard } from "@/components/exercises/ExerciseCard"
import { ExerciseForm } from "@/components/exercises/ExerciseForm"
import { Button } from "@/components/ui/button"
import { useAIPanel } from "@/contexts/AIPanelContext"
import { Sparkles } from "lucide-react"

export default function ExercisesPage() {
  // Exercises require a chosen chapter — no "all chapters" view.
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
    allChapters.find((c) => c.id === id)?.title ?? "—"

  // --- Chapter chooser: shown until a chapter is selected -----------------
  if (chapterId === undefined) {
    return (
      <div>
        <h1 className="text-2xl font-semibold tracking-tight">Exercises</h1>
        <p className="mt-1 text-sm text-muted-foreground">
          Choose a chapter to practice.
        </p>

        {books && (
          <div className="mt-6">
            <ChapterButtons
              books={books}
              selected={-1}
              onSelect={(v) => {
                if (v !== "all") setChapterId(v)
              }}
              includeAll={false}
            />
          </div>
        )}
      </div>
    )
  }

  const selectClass =
    "rounded-md border border-input bg-background px-3 py-1.5 text-sm"

  return (
    <div>
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-2xl font-semibold tracking-tight">Exercises</h1>
          <button
            onClick={() => {
              setChapterId(undefined)
              setType(undefined)
            }}
            className="mt-0.5 text-sm text-muted-foreground hover:text-accent"
          >
            {chapterTitle(chapterId)} · change
          </button>
        </div>
        <div className="flex gap-2">
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
        </div>
      </div>

      {showForm && allChapters.length > 0 && (
        <div className="mt-4 rounded-xl border border-border bg-surface p-4">
          <ExerciseForm
            chapters={allChapters}
            defaultChapterId={chapterId}
            onDone={() => setShowForm(false)}
          />
        </div>
      )}

      <div className="mt-6 flex flex-wrap items-center gap-3">
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

      <div className="mt-6 flex flex-col gap-4">
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
