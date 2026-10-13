import { useState } from "react"
import { useQuery } from "@tanstack/react-query"
import { Link, useParams } from "react-router-dom"
import { BookOpenCheck, ChevronDown } from "lucide-react"

import { fetchBooks } from "@/api/books"
import { fetchWords } from "@/api/vocabulary"
import { fetchGrammarRules } from "@/api/grammar"
import type { GrammarRule, Word } from "@/types"
import { Card } from "@/components/ui/card"
import { Button } from "@/components/ui/button"
import { BackLink } from "@/components/ui/BackLink"
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
        <BackLink to="/books" label="Books" />
        {book && (
          <p className="mt-2 text-[13px] font-semibold uppercase tracking-[0.04em] text-muted-foreground">
            {book.title}
            {chapter && ` · Chapter ${chapter.number}`}
          </p>
        )}
        <h1 className="mt-1 text-3xl font-extrabold sm:text-4xl">{chapter ? chapter.title : "Chapter"}</h1>
        {chapter?.description && (
          <p className="mt-2 text-sm text-muted-foreground">{chapter.description}</p>
        )}
      </div>

      {empty ? (
        <Card>
          <div className="flex flex-col items-center gap-2 px-6 py-12 text-center">
            <span className="flex size-16 items-center justify-center rounded-2xl bg-surface-2 text-muted-foreground">
              <BookOpenCheck className="size-8" aria-hidden="true" />
            </span>
            <p className="mt-2 text-xl font-bold">Nothing learned from this chapter yet</p>
            <p className="text-muted-foreground">
              Its words and grammar show up here as you finish its lessons on your path.
            </p>
            <Button asChild size="lg" className="mt-4">
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
      <h2 className="mb-3 px-1 text-[22px] font-bold">
        Wortschatz <span className="text-muted-foreground">{words.length}</span>
      </h2>
      <Card className="overflow-hidden">
        <ul className="divide-y divide-border/70">
          {shown.map((w) => (
            <li key={w.id} className="flex min-h-[56px] items-center justify-between gap-3 px-5 py-2.5">
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
        <Button variant="secondary" className="mt-3 w-full sm:w-auto" onClick={() => setShowAll((v) => !v)}>
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
      <h2 className="mb-3 px-1 text-[22px] font-bold">
        Grammatik <span className="text-muted-foreground">{rules.length}</span>
      </h2>
      <div className="flex flex-col gap-3">
        {rules.map((rule) =>
          openId === rule.id ? (
            <div key={rule.id}>
              <GrammarCard rule={rule} />
              <Button variant="secondary" size="sm" className="mt-2" onClick={() => setOpenId(null)}>
                Close
              </Button>
            </div>
          ) : (
            <button
              key={rule.id}
              onClick={() => setOpenId(rule.id)}
              className="lift flex min-h-[56px] items-center justify-between rounded-2xl bg-surface px-5 py-3 text-left font-semibold shadow-card"
            >
              {rule.title}
              <ChevronDown className="size-5 text-muted-foreground" aria-hidden="true" />
            </button>
          ),
        )}
      </div>
    </section>
  )
}
