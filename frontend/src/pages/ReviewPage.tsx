import { useQuery } from "@tanstack/react-query"
import { Link } from "react-router-dom"

import { fetchDueCounts, type DueCounts } from "@/api/vocabulary"
import { fetchBooks } from "@/api/books"
import { useReviewSession } from "@/hooks/useReviewSession"
import type { Book, Chapter } from "@/types"
import { FlashCard } from "@/components/vocabulary/FlashCard"
import { ChapterButtons } from "@/components/layout/ChapterButtons"
import { PageHeader } from "@/components/layout/PageHeader"
import { Button } from "@/components/ui/button"

export default function ReviewPage() {
  const session = useReviewSession()
  const { data: books } = useQuery({ queryKey: ["books"], queryFn: fetchBooks })
  const { data: counts } = useQuery({
    queryKey: ["due-counts"],
    queryFn: fetchDueCounts,
    staleTime: 0,
  })

  const allChapters: Chapter[] = books?.flatMap((b) => b.chapters) ?? []
  const chapterTitle = (id: number) => allChapters.find((c) => c.id === id)?.title ?? "—"

  if (!session.started) {
    return <StartScreen books={books} counts={counts} onSelect={session.setSelection} />
  }

  if (session.isLoading) return <Centered>Loading…</Centered>

  if (!session.dueWords?.length) {
    return (
      <div className="flex flex-col items-center gap-4 py-24 text-center">
        <p className="text-lg font-medium text-foreground">Nothing due here.</p>
        <Button variant="secondary" onClick={session.restart}>
          Choose another chapter
        </Button>
      </div>
    )
  }

  if (session.done) return <SessionComplete stats={session.stats} onRestart={session.restart} />

  const current = session.current
  if (!current) return <Centered>Loading…</Centered>

  const sessionLabel =
    session.selection === "all" ? "All chapters" : chapterTitle(session.selection as number)

  return (
    <div>
      <div className="mb-6">
        <PageHeader
          title="Review"
          subtitle={
            <button
              onClick={session.restart}
              className="text-muted-foreground transition-colors hover:text-accent"
            >
              {sessionLabel} · change
            </button>
          }
          actions={
            <span className="self-center text-sm text-muted-foreground">
              {session.stats.answered} / {session.total}
            </span>
          }
        />
      </div>

      {/* Progress by answered, not position (skips don't advance it) */}
      <div className="mb-8 h-1 w-full rounded-full bg-border">
        <div
          className="h-1 rounded-full bg-accent transition-all duration-300"
          style={{ width: `${(session.stats.answered / session.total) * 100}%` }}
        />
      </div>

      <FlashCard
        key={current.id}
        word={current}
        chapterTitle={chapterTitle(current.chapter)}
        onRate={session.rate}
        onSkip={session.skip}
      />
    </div>
  )
}

function Centered({ children }: { children: React.ReactNode }) {
  return (
    <div className="flex h-64 items-center justify-center">
      <p className="text-sm text-muted-foreground">{children}</p>
    </div>
  )
}

function StartScreen({
  books,
  counts,
  onSelect,
}: {
  books: Book[] | undefined
  counts: DueCounts | undefined
  onSelect: (id: number | "all") => void
}) {
  const total = counts?.total ?? 0
  // Only offer chapters that actually have words due.
  const dueBooks = (books ?? [])
    .map((b) => ({
      ...b,
      chapters: b.chapters.filter((c) => (counts?.per_chapter[c.id] ?? 0) > 0),
    }))
    .filter((b) => b.chapters.length > 0)

  return (
    <div>
      <PageHeader title="Review" subtitle="Choose what to review." />

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
        <div className="mt-6">
          <ChapterButtons
            books={dueBooks}
            selected={-1}
            onSelect={onSelect}
            badge={(id) => counts?.per_chapter[id]}
          />
        </div>
      )}
    </div>
  )
}

function SessionComplete({
  stats,
  onRestart,
}: {
  stats: { answered: number; correct: number; again: number }
  onRestart: () => void
}) {
  const cells = [
    { label: "Answered", value: stats.answered },
    { label: "Correct", value: stats.correct },
    { label: "Due again", value: stats.again },
  ]
  return (
    <div className="flex flex-col items-center gap-6 py-24 text-center">
      <h2 className="text-2xl font-semibold tracking-tight">Session complete</h2>
      <div className="grid grid-cols-3 gap-6">
        {cells.map(({ label, value }) => (
          <div key={label} className="flex flex-col items-center">
            <span className="text-3xl font-bold text-foreground">{value}</span>
            <span className="mt-1 text-sm text-muted-foreground">{label}</span>
          </div>
        ))}
      </div>
      <div className="flex gap-3">
        <Button variant="secondary" onClick={onRestart}>
          Review more
        </Button>
        <Button variant="ghost" asChild>
          <Link to="/">Back to Dashboard</Link>
        </Button>
      </div>
    </div>
  )
}
