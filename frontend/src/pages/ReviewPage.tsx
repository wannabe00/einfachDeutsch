import { useState } from "react"
import { useQuery, useMutation, useQueryClient } from "@tanstack/react-query"
import { Link } from "react-router-dom"

import { fetchDueWords, fetchDueCounts, reviewWord } from "@/api/vocabulary"
import { fetchBooks } from "@/api/books"
import type { ReviewQuality, Chapter, Book, Word } from "@/types"
import { FlashCard } from "@/components/vocabulary/FlashCard"
import { Button } from "@/components/ui/button"

// `null` = choosing; "all" = every chapter; number = a specific chapter id.
type Selection = number | "all" | null

export default function ReviewPage() {
  const qc = useQueryClient()
  const [selection, setSelection] = useState<Selection>(null)
  const [queue, setQueue] = useState<Word[]>([])
  const [total, setTotal] = useState(0)
  const [stats, setStats] = useState({ answered: 0, correct: 0, again: 0 })
  const [done, setDone] = useState(false)

  const { data: books } = useQuery({ queryKey: ["books"], queryFn: fetchBooks })
  const { data: counts } = useQuery({
    queryKey: ["due-counts"],
    queryFn: fetchDueCounts,
    staleTime: 0,
  })

  const started = selection !== null
  const { data: dueWords, isLoading } = useQuery({
    queryKey: ["due-words", selection],
    queryFn: () => fetchDueWords(selection === "all" ? undefined : (selection as number)),
    enabled: started,
    staleTime: 0,
  })

  const allChapters: Chapter[] = books?.flatMap((b) => b.chapters) ?? []
  const chapterTitle = (id: number) =>
    allChapters.find((c) => c.id === id)?.title ?? "—"

  // Seed the working queue when a new set of due words arrives (render-time,
  // keyed on the query result's identity so it only re-seeds on a new session).
  const [seededFrom, setSeededFrom] = useState<Word[] | null>(null)
  if (dueWords && dueWords !== seededFrom) {
    setSeededFrom(dueWords)
    setQueue(dueWords)
    setTotal(dueWords.length)
  }

  const mutation = useMutation({
    mutationFn: ({ id, quality }: { id: number; quality: ReviewQuality }) =>
      reviewWord(id, quality),
  })

  function restart() {
    setSelection(null)
    setQueue([])
    setTotal(0)
    setStats({ answered: 0, correct: 0, again: 0 })
    setDone(false)
    qc.invalidateQueries({ queryKey: ["due-counts"] })
  }

  function finishIfEmpty(remaining: Word[]) {
    if (remaining.length === 0) {
      qc.invalidateQueries({ queryKey: ["due-words"] })
      qc.invalidateQueries({ queryKey: ["words"] })
      qc.invalidateQueries({ queryKey: ["stats"] })
      qc.invalidateQueries({ queryKey: ["due-counts"] })
      setDone(true)
    }
  }

  function handleRate(quality: ReviewQuality) {
    const word = queue[0]
    if (!word) return
    mutation.mutate(
      { id: word.id, quality },
      {
        onSuccess: () => {
          setStats((s) => ({
            answered: s.answered + 1,
            correct: quality >= 4 ? s.correct + 1 : s.correct,
            again: quality === 0 ? s.again + 1 : s.again,
          }))
          setQueue((q) => {
            const next = q.slice(1)
            finishIfEmpty(next)
            return next
          })
        },
      },
    )
  }

  // Skip: move the current word to the end of the queue (no review recorded).
  function handleSkip() {
    setQueue((q) => (q.length <= 1 ? q : [...q.slice(1), q[0]]))
  }

  // --- Start screen: choose a chapter -------------------------------------
  if (!started) {
    const total = counts?.total ?? 0
    return (
      <div>
        <h1 className="text-2xl font-semibold tracking-tight">Review</h1>
        <p className="mt-1 text-sm text-muted-foreground">
          Choose what to review.
        </p>

        {total === 0 ? (
          <div className="mt-10 flex flex-col items-center gap-4 py-16 text-center">
            <p className="text-lg font-medium text-foreground">Nothing due today.</p>
            <p className="text-sm text-muted-foreground">
              Come back tomorrow, or add more words.
            </p>
            <Button variant="secondary" asChild>
              <Link to="/words">Go to Word Bank</Link>
            </Button>
          </div>
        ) : (
          <div className="mt-6 flex flex-col gap-6">
            <button
              onClick={() => setSelection("all")}
              className="flex items-center justify-between rounded-xl border border-border bg-surface px-5 py-4 text-left shadow-sm transition-shadow hover:shadow-md"
            >
              <span className="font-medium text-foreground">All chapters</span>
              <span className="rounded-full bg-accent px-2.5 py-0.5 text-xs font-semibold text-accent-foreground">
                {total} due
              </span>
            </button>

            {books?.map((book: Book) => {
              const chaptersWithDue = book.chapters.filter(
                (c) => (counts?.per_chapter[c.id] ?? 0) > 0,
              )
              if (chaptersWithDue.length === 0) return null
              return (
                <div key={book.id}>
                  <h2 className="mb-2 text-xs font-semibold uppercase tracking-wide text-muted-foreground">
                    {book.title}
                  </h2>
                  <div className="flex flex-col gap-2">
                    {chaptersWithDue.map((c) => (
                      <button
                        key={c.id}
                        onClick={() => setSelection(c.id)}
                        className="flex items-center justify-between rounded-lg border border-border bg-surface px-4 py-3 text-left transition-colors hover:border-accent"
                      >
                        <span className="text-sm text-foreground">{c.title}</span>
                        <span className="rounded-full bg-muted px-2 py-0.5 text-xs font-medium text-muted-foreground">
                          {counts?.per_chapter[c.id]} due
                        </span>
                      </button>
                    ))}
                  </div>
                </div>
              )
            })}
          </div>
        )}
      </div>
    )
  }

  // --- Loading the chosen session -----------------------------------------
  if (isLoading) {
    return (
      <div className="flex h-64 items-center justify-center">
        <p className="text-sm text-muted-foreground">Loading…</p>
      </div>
    )
  }

  if (!dueWords?.length) {
    return (
      <div className="flex flex-col items-center gap-4 py-24 text-center">
        <p className="text-lg font-medium text-foreground">Nothing due here.</p>
        <Button variant="secondary" onClick={restart}>
          Choose another chapter
        </Button>
      </div>
    )
  }

  if (done) {
    return (
      <div className="flex flex-col items-center gap-6 py-24 text-center">
        <h2 className="text-2xl font-semibold tracking-tight">Session complete</h2>
        <div className="grid grid-cols-3 gap-6">
          {[
            { label: "Answered", value: stats.answered },
            { label: "Correct", value: stats.correct },
            { label: "Due again", value: stats.again },
          ].map(({ label, value }) => (
            <div key={label} className="flex flex-col items-center">
              <span className="text-3xl font-bold text-foreground">{value}</span>
              <span className="mt-1 text-sm text-muted-foreground">{label}</span>
            </div>
          ))}
        </div>
        <div className="flex gap-3">
          <Button variant="secondary" onClick={restart}>
            Review more
          </Button>
          <Button variant="ghost" asChild>
            <Link to="/">Back to Dashboard</Link>
          </Button>
        </div>
      </div>
    )
  }

  const currentWord = queue[0]
  if (!currentWord) {
    return (
      <div className="flex h-64 items-center justify-center">
        <p className="text-sm text-muted-foreground">Loading…</p>
      </div>
    )
  }
  const sessionLabel =
    selection === "all" ? "All chapters" : chapterTitle(selection as number)

  return (
    <div>
      <div className="mb-6 flex items-center justify-between">
        <div>
          <h1 className="text-2xl font-semibold tracking-tight">Review</h1>
          <button
            onClick={restart}
            className="mt-0.5 text-sm text-muted-foreground hover:text-accent"
          >
            {sessionLabel} · change
          </button>
        </div>
        <span className="text-sm text-muted-foreground">
          {stats.answered} / {total}
        </span>
      </div>

      {/* Progress bar — by answered, not position (skips don't advance it) */}
      <div className="mb-8 h-1 w-full rounded-full bg-border">
        <div
          className="h-1 rounded-full bg-accent transition-all duration-300"
          style={{ width: `${(stats.answered / total) * 100}%` }}
        />
      </div>

      <FlashCard
        key={currentWord.id}
        word={currentWord}
        chapterTitle={chapterTitle(currentWord.chapter)}
        onRate={handleRate}
        onSkip={handleSkip}
      />
    </div>
  )
}
