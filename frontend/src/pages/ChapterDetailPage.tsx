import { useState } from "react"
import { useQuery } from "@tanstack/react-query"
import { Link, useParams } from "react-router-dom"
import { ArrowLeft, ChevronDown } from "lucide-react"

import { fetchBooks } from "@/api/books"
import { fetchWords } from "@/api/vocabulary"
import { fetchGrammarRules } from "@/api/grammar"
import type { GrammarRule, Word } from "@/types"
import { Card } from "@/components/ui/card"
import { Button } from "@/components/ui/button"
import { ArticleBadge } from "@/components/vocabulary/ArticleBadge"
import { GrammarCard } from "@/components/grammar/GrammarCard"

/*
 * One chapter of a book: its words (the first ten, then "Show all") and its
 * grammar topics. Like the Word Bank and Grammar pages, only what you've
 * learned is listed; the API leaves the rest out.
 */
const FIRST_WORDS = 10

export default function ChapterDetailPage() {
  const { chapterId } = useParams<{ chapterId: string }>()
  const id = Number(chapterId)

  const { data: books } = useQuery({ queryKey: ["books"], queryFn: fetchBooks })
  const { data: words } = useQuery({
    queryKey: ["words", id],
    queryFn: () => fetchWords(id),
  })
  const { data: grammar } = useQuery({
    queryKey: ["grammar", id, undefined],
    queryFn: () => fetchGrammarRules(id),
  })

  const book = books?.find((b) => b.chapters.some((c) => c.id === id))
  const chapter = book?.chapters.find((c) => c.id === id)
  const empty = words?.length === 0 && grammar?.length === 0

  return (
    <div className="flex flex-col gap-6">
      <div>
        <Link
          to="/books"
          className="inline-flex items-center gap-1.5 text-sm text-muted-foreground hover:text-foreground"
        >
          <ArrowLeft className="size-4" /> Books
        </Link>
        <h1 className="mt-3 text-2xl font-bold tracking-tight">
          {chapter ? `Chapter ${chapter.number}: ${chapter.title}` : "Chapter"}
        </h1>
        {book && <p className="mt-1 text-sm text-muted-foreground">{book.title}</p>}
        {chapter?.description && (
          <p className="mt-2 text-sm text-muted-foreground">{chapter.description}</p>
        )}
      </div>

      {empty ? (
        <Card>
          <div className="p-6 text-center">
            <p className="font-medium">Nothing learned from this chapter yet.</p>
            <p className="mt-1 text-sm text-muted-foreground">
              Its words and grammar show up here as you finish its lessons on your path.
            </p>
            <Button asChild variant="secondary" className="mt-5">
              <Link to="/path">Go to your path</Link>
            </Button>
          </div>
        </Card>
      ) : (
        <>
          {!!words?.length && <WordList words={words} />}
          {!!grammar?.length && <GrammarList rules={grammar} />}
        </>
      )}
    </div>
  )
}

function WordList({ words }: { words: Word[] }) {
  const [showAll, setShowAll] = useState(false)
  const shown = showAll ? words : words.slice(0, FIRST_WORDS)

  return (
    <section>
      <h2 className="mb-3 text-sm font-semibold uppercase tracking-wide text-muted-foreground">
        Words ({words.length})
      </h2>
      <Card>
        <ul className="divide-y divide-border">
          {shown.map((w) => (
            <li key={w.id} className="flex items-center justify-between gap-3 px-4 py-2.5">
              <span className="flex min-w-0 items-center gap-2 font-medium">
                <ArticleBadge german={w.german} />
                <span className="truncate">{w.german}</span>
                {w.plural && (
                  <span className="hidden text-xs text-muted-foreground sm:inline">
                    Pl. {w.plural}
                  </span>
                )}
              </span>
              <span className="shrink-0 text-sm text-muted-foreground">{w.english}</span>
            </li>
          ))}
        </ul>
      </Card>
      {words.length > FIRST_WORDS && (
        <Button variant="secondary" className="mt-3" onClick={() => setShowAll((v) => !v)}>
          {showAll ? "Show fewer" : `Show all ${words.length} words`}
        </Button>
      )}
    </section>
  )
}

function GrammarList({ rules }: { rules: GrammarRule[] }) {
  const [openId, setOpenId] = useState<number | null>(null)

  return (
    <section>
      <h2 className="mb-3 text-sm font-semibold uppercase tracking-wide text-muted-foreground">
        Grammar ({rules.length})
      </h2>
      <div className="flex flex-col gap-2">
        {rules.map((rule) =>
          openId === rule.id ? (
            <div key={rule.id}>
              <GrammarCard rule={rule} />
              <button
                onClick={() => setOpenId(null)}
                className="mt-2 text-sm text-muted-foreground underline hover:text-foreground"
              >
                Close
              </button>
            </div>
          ) : (
            <button
              key={rule.id}
              onClick={() => setOpenId(rule.id)}
              className="flex items-center justify-between rounded-xl border border-border bg-surface px-4 py-3 text-left font-medium transition-colors hover:bg-surface-2"
            >
              {rule.title}
              <ChevronDown className="size-4 text-muted-foreground" />
            </button>
          ),
        )}
      </div>
    </section>
  )
}
