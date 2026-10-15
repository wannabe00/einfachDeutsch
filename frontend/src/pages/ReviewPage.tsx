import { useQuery } from "@tanstack/react-query"
import { Link, useLocation } from "react-router-dom"
import { ArrowRight, CheckCircle2, GraduationCap, RotateCcw } from "lucide-react"

import { fetchDueCounts, type DueCounts } from "@/api/vocabulary"
import { fetchBooks } from "@/api/books"
import { fetchStats } from "@/api/stats"
import { useAuth } from "@/contexts/AuthContext"
import { LockedFeature } from "@/components/auth/LockedFeature"
import { useReviewSession } from "@/hooks/useReviewSession"
import type { Book, Chapter, Word } from "@/types"
import { FlashCard } from "@/components/vocabulary/FlashCard"
import { ChapterButtons } from "@/components/layout/ChapterButtons"
import { PageHeader } from "@/components/layout/PageHeader"
import { Button } from "@/components/ui/button"
import { Card } from "@/components/ui/card"
import { SessionBar } from "@/components/ui/SessionBar"

/*
 * Flashcard review of learned words, scheduled by SM-2. Pick a chapter or
 * everything, or the Word Bank can send its own selection of words. (The
 * Dashboard's review of the last Lektion is a check: see CheckPage.) It needs an account and at least one finished
 * lesson: until then there is nothing to review and no choices are shown.
 */
export default function ReviewPage() {
  const { user } = useAuth()
  const { data: stats } = useQuery({ queryKey: ["stats"], queryFn: fetchStats, enabled: !!user })
  const picked = (useLocation().state as { words?: Word[] } | null)?.words
  const session = useReviewSession(picked?.length ? { words: picked } : null)
  const { data: books } = useQuery({ queryKey: ["books"], queryFn: fetchBooks })
  const { data: counts } = useQuery({
    queryKey: ["due-counts"],
    queryFn: fetchDueCounts,
    staleTime: 0,
  })

  const allChapters: Chapter[] = books?.flatMap((b) => b.chapters) ?? []
  const chapterTitle = (id: number) =>
    allChapters.find((c) => c.id === id)?.title ?? "Unknown chapter"

  if (!user) {
    return (
      <LockedFeature
        title="Review needs an account"
        description="Review brings back the words from the lessons you've finished, so it needs your progress. Accounts are free."
      />
    )
  }

  if (!session.started) {
    if (!stats) return <Centered>Loading…</Centered>
    if (stats.words_learned === 0) {
      return (
        <div className="flex flex-col gap-6">
          <PageHeader title="Review" />
          <EmptyState
            title="Nothing to review yet"
            body="Review brings back the words from lessons you've finished. Finish your first lesson and its words show up here."
            action={
              <Button size="lg" asChild>
                <Link to="/path">
                  Start your first lesson <ArrowRight />
                </Link>
              </Button>
            }
          />
        </div>
      )
    }
    return <StartScreen books={books} counts={counts} onSelect={session.setSelection} />
  }

  if (session.isLoading) return <Centered>Loading…</Centered>

  if (!session.dueWords?.length) {
    return (
      <EmptyState
        title="Nothing due here"
        body="Every word in this selection is scheduled for later."
        action={
          <Button size="lg" variant="secondary" onClick={session.restart}>
            Choose another chapter
          </Button>
        }
      />
    )
  }

  if (session.done) return <SessionComplete stats={session.stats} onRestart={session.restart} />

  const current = session.current
  if (!current) return <Centered>Loading…</Centered>

  const sessionLabel =
    session.selection === "all"
      ? "All chapters"
      : typeof session.selection === "object"
        ? "Your Word Bank selection"
        : chapterTitle(session.selection as number)

  return (
    <div className="mx-auto flex max-w-xl flex-col gap-8">
      {/* Progress by answered, not position (skips don't advance it). */}
      <SessionBar
        onClose={session.restart}
        closeLabel="End review"
        title={`Review · ${sessionLabel}`}
        progress={(session.stats.answered / session.total) * 100}
        counter={`${session.stats.answered}/${session.total}`}
      />

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

function EmptyState({ title, body, action }: { title: string; body: string; action: React.ReactNode }) {
  return (
    <Card className="mx-auto flex max-w-md flex-col items-center gap-3 px-6 py-12 text-center">
      <span className="flex size-16 items-center justify-center rounded-full bg-[hsl(var(--success-bg))] text-[hsl(var(--success))]">
        <CheckCircle2 className="size-8" aria-hidden="true" />
      </span>
      <h2 className="mt-2 text-2xl font-extrabold">{title}</h2>
      <p className="text-muted-foreground">{body}</p>
      <div className="mt-3">{action}</div>
    </Card>
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
    <div className="flex flex-col gap-6">
      <PageHeader title="Review" subtitle="Flashcards for the words you've learned, timed so they come back just before you forget them." />

      {total === 0 ? (
        <EmptyState
          title="All caught up"
          body="Review covers the words from lessons you've finished. Come back tomorrow, or continue your path to learn more."
          action={
            <Button size="lg" asChild>
              <Link to="/path">
                Continue your path <ArrowRight />
              </Link>
            </Button>
          }
        />
      ) : (
        <>
          <Card className="flex flex-col gap-5 p-6 sm:flex-row sm:items-center sm:p-7">
            <span className="flex size-14 shrink-0 items-center justify-center rounded-2xl bg-primary/10 text-primary">
              <GraduationCap className="size-7" aria-hidden="true" />
            </span>
            <div className="min-w-0 flex-1">
              <p className="font-grotesk text-4xl font-extrabold tabular-nums tracking-tight">
                {total} <span className="text-xl font-bold text-muted-foreground">{total === 1 ? "word" : "words"} due</span>
              </p>
              <p className="mt-1 text-muted-foreground">About {Math.max(1, Math.round(total / 4))} min. Type each one in German.</p>
            </div>
            <Button size="lg" onClick={() => onSelect("all")}>
              Review all <ArrowRight />
            </Button>
          </Card>

          <section>
            <h2 className="mb-3 px-1 text-[22px] font-bold">Or pick a Lektion</h2>
            <ChapterButtons
              books={dueBooks}
              selected={-1}
              onSelect={onSelect}
              includeAll={false}
              badge={(id) => counts?.per_chapter[id]}
            />
          </section>
        </>
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
    <div className="mx-auto max-w-md py-8">
      <Card className="p-8 text-center">
        <span className="mx-auto flex size-24 items-center justify-center rounded-full bg-[hsl(var(--success-bg))] text-[hsl(var(--success))] animate-in zoom-in-50 fade-in-0 duration-500">
          <CheckCircle2 className="size-12" strokeWidth={2.25} aria-hidden="true" />
        </span>
        <h2 className="mt-6 text-3xl font-extrabold">Session complete</h2>
        <div className="mt-6 grid grid-cols-3 gap-2 rounded-2xl bg-surface-2/70 p-4">
          {cells.map(({ label, value }) => (
            <div key={label} className="flex flex-col items-center">
              <span className="font-grotesk text-2xl font-extrabold tabular-nums">{value}</span>
              <span className="mt-0.5 text-xs text-muted-foreground">{label}</span>
            </div>
          ))}
        </div>
        <div className="mt-7 flex flex-col gap-2.5">
          <Button size="lg" onClick={onRestart}>
            <RotateCcw /> Review more
          </Button>
          <Button size="lg" variant="secondary" asChild>
            <Link to="/">Back to Home</Link>
          </Button>
        </div>
      </Card>
    </div>
  )
}
