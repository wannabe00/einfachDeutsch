import { useMemo, useState } from "react"
import { Link, useNavigate } from "react-router-dom"
import { useQuery } from "@tanstack/react-query"
import { BookMarked, ChevronDown, Lock, Plus, Sparkles } from "lucide-react"

import { fetchWords } from "@/api/vocabulary"
import { fetchBooks } from "@/api/books"
import type { Chapter, Word } from "@/types"
import { cn } from "@/lib/utils"
import { wordStatus, wordStrength, type WordStatus } from "@/lib/wordStrength"
import { useAuth } from "@/contexts/AuthContext"
import { useAIPanel } from "@/contexts/AIPanelContext"
import { PageHeader } from "@/components/layout/PageHeader"
import { Card } from "@/components/ui/card"
import { Button } from "@/components/ui/button"
import { SearchField } from "@/components/ui/SearchField"
import { LektionCover } from "@/components/lektion/LektionCover"
import { ArticleBadge } from "@/components/vocabulary/ArticleBadge"
import { WordForm } from "@/components/vocabulary/WordForm"
import { SavedWords } from "@/components/vocabulary/SavedWords"
import { CSVImportButton } from "@/components/vocabulary/CSVImportButton"
import { PasteWordsButton } from "@/components/vocabulary/PasteWordsButton"

/*
 * The words you've learned, grouped by topic (the unit that taught them) in
 * learning order. Filter by part of speech, article and how well you know a
 * word, search, and send the filtered words to a flashcard session.
 */

const KINDS = [
  { value: "noun", label: "Nouns" },
  { value: "verb", label: "Verbs" },
  { value: "adjective", label: "Adjectives" },
  { value: "phrase", label: "Phrases" },
]
const ARTICLES = ["der", "die", "das"]
const STATUSES: { value: WordStatus; label: string }[] = [
  { value: "new", label: "New" },
  { value: "learning", label: "Learning" },
  { value: "known", label: "Known" },
]
// Words sent to one "Practise these" session, weakest first.
const PRACTICE_LIMIT = 30

interface Topic {
  key: string
  title: string
  /** Lektion number and level for path units; null for your own chapters. */
  order: number | null
  level: string
  words: Word[]
}

function toggle(list: string[], value: string): string[] {
  return list.includes(value) ? list.filter((v) => v !== value) : [...list, value]
}

export default function WordBankPage() {
  const { user } = useAuth()
  const { openPanel } = useAIPanel()
  const navigate = useNavigate()
  const [showForm, setShowForm] = useState(false)
  const [query, setQuery] = useState("")
  const [kinds, setKinds] = useState<string[]>([])
  const [articles, setArticles] = useState<string[]>([])
  const [statuses, setStatuses] = useState<string[]>([])
  // Topics the user opened or closed; by default only the newest is open.
  const [toggled, setToggled] = useState<string[]>([])

  const { data: books } = useQuery({ queryKey: ["books"], queryFn: fetchBooks })
  const { data: words, isLoading } = useQuery({
    queryKey: ["words", "all"],
    queryFn: () => fetchWords(),
  })
  const allChapters: Chapter[] = books?.flatMap((b) => b.chapters) ?? []

  const filtered = useMemo(() => {
    const q = query.trim().toLowerCase()
    return (words ?? []).filter(
      (w) =>
        (!q || `${w.german} ${w.english} ${w.plural}`.toLowerCase().includes(q)) &&
        (!kinds.length || kinds.includes(w.part_of_speech)) &&
        (!articles.length || articles.includes(w.german.split(" ")[0])) &&
        (!statuses.length || statuses.includes(wordStatus(w))),
    )
  }, [words, query, kinds, articles, statuses])

  // Topics in learning order: by level, then by place on the path; words you
  // added to a chapter of your own come last.
  const topics = useMemo(() => {
    const byKey = new Map<string, Topic & { sort: [string, number] }>()
    for (const w of filtered) {
      const t = w.topic
      if (!byKey.has(t.key)) {
        byKey.set(t.key, {
          key: t.key,
          title: t.title,
          order: t.order,
          level: w.cefr_level,
          words: [],
          sort: [w.cefr_level, t.order ?? Number.MAX_SAFE_INTEGER],
        })
      }
      byKey.get(t.key)!.words.push(w)
    }
    return [...byKey.values()].sort(
      (a, b) => a.sort[0].localeCompare(b.sort[0]) || a.sort[1] - b.sort[1],
    )
  }, [filtered])

  const narrowed = !!query.trim() || kinds.length + articles.length + statuses.length > 0
  const newest = topics.filter((t) => t.key.startsWith("u")).at(-1)?.key
  const isOpen = (key: string) => narrowed || (key === newest) !== toggled.includes(key)

  function practise() {
    const weakestFirst = [...filtered].sort((a, b) => wordStrength(a) - wordStrength(b))
    navigate("/review", { state: { words: weakestFirst.slice(0, PRACTICE_LIMIT) } })
  }

  return (
    <div className="flex flex-col gap-6">
      <PageHeader
        title="Word Bank"
        subtitle={`${words?.length ?? 0} words learned`}
        actions={
          <>
            <GenerateWithAI
              premium={!!user?.has_premium}
              onOpen={() =>
                openPanel(
                  "AI · Generate words",
                  "Suggest 10 German vocabulary words for my level. Give German (with article) and English.",
                )
              }
            />
            {user && (
              <Button onClick={() => setShowForm((v) => !v)}>
                {showForm ? (
                  "Cancel"
                ) : (
                  <>
                    <Plus /> Add words
                  </>
                )}
              </Button>
            )}
          </>
        }
      />

      {showForm && (
        <Card>
          <div className="flex flex-col gap-4 p-5 sm:p-6">
            <p className="text-sm text-muted-foreground">Words you add are yours: they show under “Your words”.</p>
            <WordForm onDone={() => setShowForm(false)} />
            {/* Shared words for everyone: staff only (the API checks it too). */}
            {user?.is_staff && allChapters.length > 0 && (
              <div className="flex flex-wrap gap-2 border-t border-border pt-4">
                <PasteWordsButton chapters={allChapters} defaultChapterId={allChapters[0]?.id} />
                <CSVImportButton chapters={allChapters} defaultChapterId={allChapters[0]?.id} />
              </div>
            )}
          </div>
        </Card>
      )}

      {user && <SavedWords />}

      {!!words?.length && (
        <div className="grid grid-cols-3 gap-3">
          {STATUSES.map((st) => {
            const on = statuses.includes(st.value)
            const count = words.filter((w) => wordStatus(w) === st.value).length
            return (
              <button
                key={st.value}
                onClick={() => setStatuses(toggle(statuses, st.value))}
                aria-pressed={on}
                className={cn(
                  "lift min-w-0 rounded-2xl bg-surface p-3 text-left shadow-card sm:p-4",
                  on && "ring-2 ring-primary",
                )}
              >
                <span className="block font-grotesk text-2xl font-extrabold tabular-nums sm:text-3xl">{count}</span>
                <span className="flex items-center gap-2 text-sm text-muted-foreground">
                  <span className="hidden sm:block">
                    <StrengthBars level={st.value === "new" ? 0 : st.value === "learning" ? 2 : 4} />
                  </span>
                  <span className="truncate">{st.label}</span>
                </span>
              </button>
            )
          })}
        </div>
      )}

      <div className="flex flex-col gap-3">
        <SearchField value={query} onChange={setQuery} placeholder="Search in German or English" />
        <div className="flex flex-wrap gap-x-4 gap-y-2">
          <ChipGroup options={KINDS} selected={kinds} onToggle={(v) => setKinds(toggle(kinds, v))} />
          <ChipGroup
            options={ARTICLES.map((a) => ({ value: a, label: a }))}
            selected={articles}
            onToggle={(v) => setArticles(toggle(articles, v))}
          />
        </div>
        {filtered.length > 0 && (
          <div className="flex flex-wrap items-center justify-between gap-3">
            <p className="text-sm text-muted-foreground">
              {narrowed ? `${filtered.length} of ${words?.length ?? 0} words` : " "}
            </p>
            <Button onClick={practise}>
              Practise {narrowed ? "these" : "your weakest"} (
              {Math.min(filtered.length, PRACTICE_LIMIT)})
            </Button>
          </div>
        )}
      </div>

      {isLoading ? (
        <Centered>Loading your words…</Centered>
      ) : !words?.length ? (
        <Empty signedIn={!!user} />
      ) : topics.length === 0 ? (
        <Centered>No words match these filters.</Centered>
      ) : (
        <div className="flex flex-col gap-3">
          {topics.map((t) => (
            <TopicSection
              key={t.key}
              topic={t}
              open={isOpen(t.key)}
              onToggle={() => setToggled(toggle(toggled, t.key))}
            />
          ))}
        </div>
      )}
    </div>
  )
}

function ChipGroup({
  options,
  selected,
  onToggle,
}: {
  options: { value: string; label: string }[]
  selected: string[]
  onToggle: (value: string) => void
}) {
  return (
    <div className="flex flex-wrap gap-1.5">
      {options.map((o) => {
        const on = selected.includes(o.value)
        return (
          <button
            key={o.value}
            onClick={() => onToggle(o.value)}
            aria-pressed={on}
            className={cn(
              "min-h-[36px] rounded-full px-3.5 text-sm font-medium transition-colors",
              on
                ? "bg-foreground text-background"
                : "bg-surface text-muted-foreground shadow-card hover:text-foreground",
            )}
          >
            {o.label}
          </button>
        )
      })}
    </div>
  )
}

function TopicSection({
  topic,
  open,
  onToggle,
}: {
  topic: Topic
  open: boolean
  onToggle: () => void
}) {
  return (
    <Card>
      <button
        onClick={onToggle}
        aria-expanded={open}
        className="flex w-full items-center gap-4 p-3 pr-5 text-left"
      >
        {topic.order ? (
          <LektionCover order={topic.order} level={topic.level} size="sm" className="h-14 w-11 shrink-0 rounded-[10px]" />
        ) : (
          <span className="flex h-14 w-11 shrink-0 items-center justify-center rounded-[10px] bg-surface-2 text-muted-foreground">
            <BookMarked className="size-5" aria-hidden="true" />
          </span>
        )}
        <span className="min-w-0 flex-1">
          {topic.order && (
            <span className="block text-xs font-semibold uppercase tracking-[0.04em] text-muted-foreground">
              {topic.level} · Lektion {topic.order}
            </span>
          )}
          <span className="block truncate font-semibold">{topic.title}</span>
        </span>
        <span className="flex shrink-0 items-center gap-2 text-sm font-medium text-muted-foreground">
          {topic.words.length}
          <ChevronDown className={cn("size-5 transition-transform", open && "rotate-180")} />
        </span>
      </button>
      {open && (
        <ul className="grid gap-x-6 border-t border-border px-5 py-2 sm:grid-cols-2">
          {topic.words.map((w) => (
            <WordRow key={w.id} word={w} />
          ))}
        </ul>
      )}
    </Card>
  )
}

function WordRow({ word }: { word: Word }) {
  // The coloured badge carries the article, so the noun is shown without it.
  const [first, ...rest] = word.german.split(" ")
  const bare = ARTICLES.includes(first) && rest.length ? rest.join(" ") : word.german
  return (
    <li className="flex min-h-[60px] min-w-0 items-center justify-between gap-3 border-b border-border/60 py-2.5 last:border-0">
      <div className="min-w-0">
        <p className="flex items-center gap-2 font-medium">
          <ArticleBadge german={word.german} />
          <span className="truncate">{bare}</span>
        </p>
        <p className="truncate text-sm text-muted-foreground">
          {word.english}
          {word.plural && <span className="ml-2 text-xs">Pl. {word.plural}</span>}
        </p>
      </div>
      <StrengthMeter word={word} />
    </li>
  )
}

/** Four bars: how well you know the word, from your flashcard reviews. */
function StrengthMeter({ word }: { word: Word }) {
  const label = { new: "New", learning: "Learning", known: "Known" }[wordStatus(word)]
  return (
    <span className="shrink-0" title={label} aria-label={label}>
      <StrengthBars level={wordStrength(word)} />
    </span>
  )
}

function StrengthBars({ level }: { level: number }) {
  return (
    <span className="flex items-end gap-0.5" aria-hidden="true">
      {[1, 2, 3, 4].map((n) => (
        <span
          key={n}
          className={cn("w-1.5 rounded-sm", n <= level ? "bg-[hsl(var(--success))]" : "bg-surface-2")}
          style={{ height: 4 + n * 3 }}
        />
      ))}
    </span>
  )
}

function Empty({ signedIn }: { signedIn: boolean }) {
  return (
    <Card className="mx-auto flex max-w-md flex-col items-center gap-3 px-6 py-12 text-center">
      <span className="flex size-16 items-center justify-center rounded-2xl bg-surface-2 text-muted-foreground">
        <BookMarked className="size-8" aria-hidden="true" />
      </span>
      <p className="mt-2 text-xl font-bold">No words here yet</p>
      <p className="max-w-sm text-muted-foreground">
        {signedIn
          ? "Words appear here as you finish lessons on your path."
          : "Sign in to collect the words from your lessons."}
      </p>
      <Button asChild size="lg" className="mt-2">
        <Link to={signedIn ? "/path" : "/login"}>{signedIn ? "Go to your path" : "Sign in"}</Link>
      </Button>
    </Card>
  )
}

/** AI word generation is premium, so free users see it locked. */
function GenerateWithAI({ premium, onOpen }: { premium: boolean; onOpen: () => void }) {
  if (!premium) {
    return (
      <Button variant="secondary" disabled title="Generating words with AI is a Premium feature">
        <Lock /> Generate with AI
      </Button>
    )
  }
  return (
    <Button variant="secondary" onClick={onOpen}>
      <Sparkles /> Generate with AI
    </Button>
  )
}

function Centered({ children }: { children: React.ReactNode }) {
  return (
    <div className="flex h-40 items-center justify-center">
      <p className="text-sm text-muted-foreground">{children}</p>
    </div>
  )
}
