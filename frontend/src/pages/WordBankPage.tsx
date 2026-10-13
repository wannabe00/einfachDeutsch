import { useMemo, useState } from "react"
import { Link, useNavigate } from "react-router-dom"
import { useQuery } from "@tanstack/react-query"
import { ChevronDown, Lock, Plus, Search, Sparkles } from "lucide-react"

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
import { ArticleBadge } from "@/components/vocabulary/ArticleBadge"
import { WordForm } from "@/components/vocabulary/WordForm"
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
          title: t.order ? `${w.cefr_level} · Lektion ${t.order}: ${t.title}` : t.title,
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
            <Button onClick={() => setShowForm((v) => !v)}>
              {showForm ? (
                "Cancel"
              ) : (
                <>
                  <Plus className="mr-2 size-4" /> Add Words
                </>
              )}
            </Button>
          </>
        }
      />

      {showForm && allChapters.length > 0 && (
        <Card>
          <div className="flex flex-col gap-4 p-5">
            <WordForm
              chapters={allChapters}
              defaultChapterId={allChapters[0]?.id}
              onDone={() => setShowForm(false)}
            />
            <div className="flex flex-wrap gap-2 border-t border-border pt-4">
              <PasteWordsButton chapters={allChapters} defaultChapterId={allChapters[0]?.id} />
              <CSVImportButton chapters={allChapters} defaultChapterId={allChapters[0]?.id} />
            </div>
          </div>
        </Card>
      )}

      <div className="flex flex-col gap-3">
        <div className="relative">
          <Search className="pointer-events-none absolute left-3 top-1/2 size-4 -translate-y-1/2 text-muted-foreground" />
          <input
            value={query}
            onChange={(e) => setQuery(e.target.value)}
            placeholder="Search in German or English"
            className="w-full rounded-lg border border-border bg-surface py-2.5 pl-10 pr-3 text-sm focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring"
          />
        </div>
        <div className="flex flex-wrap gap-x-4 gap-y-2">
          <ChipGroup options={KINDS} selected={kinds} onToggle={(v) => setKinds(toggle(kinds, v))} />
          <ChipGroup
            options={ARTICLES.map((a) => ({ value: a, label: a }))}
            selected={articles}
            onToggle={(v) => setArticles(toggle(articles, v))}
          />
          <ChipGroup
            options={STATUSES}
            selected={statuses}
            onToggle={(v) => setStatuses(toggle(statuses, v))}
          />
        </div>
        {filtered.length > 0 && (
          <div className="flex flex-wrap items-center justify-between gap-3">
            <p className="text-sm text-muted-foreground">
              {narrowed ? `${filtered.length} of ${words?.length ?? 0} words` : " "}
            </p>
            <Button variant="secondary" onClick={practise}>
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
              "rounded-full border px-3 py-1 text-sm transition-colors",
              on
                ? "border-primary bg-primary/15 text-foreground"
                : "border-border text-muted-foreground hover:text-foreground",
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
        className="flex w-full items-center justify-between gap-3 px-5 py-4 text-left"
      >
        <span className="min-w-0 truncate font-semibold">{topic.title}</span>
        <span className="flex shrink-0 items-center gap-2 text-sm text-muted-foreground">
          {topic.words.length}
          <ChevronDown className={cn("size-4 transition-transform", open && "rotate-180")} />
        </span>
      </button>
      {open && (
        <ul className="grid gap-x-6 border-t border-border px-5 py-3 sm:grid-cols-2">
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
    <li className="flex items-center justify-between gap-3 border-b border-border/60 py-2 last:border-0">
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
  const strength = wordStrength(word)
  const label = { new: "New", learning: "Learning", known: "Known" }[wordStatus(word)]
  return (
    <span className="flex shrink-0 items-end gap-0.5" title={label} aria-label={label}>
      {[1, 2, 3, 4].map((n) => (
        <span
          key={n}
          className={cn(
            "w-1.5 rounded-sm",
            n <= strength ? "bg-[hsl(var(--success))]" : "bg-border",
          )}
          style={{ height: 4 + n * 3 }}
        />
      ))}
    </span>
  )
}

function Empty({ signedIn }: { signedIn: boolean }) {
  return (
    <div className="flex flex-col items-center gap-3 py-16 text-center">
      <p className="font-medium">No words here yet.</p>
      <p className="max-w-sm text-sm text-muted-foreground">
        {signedIn
          ? "Words appear here as you finish lessons on your path."
          : "Sign in to collect the words from your lessons."}
      </p>
      <Button asChild variant="secondary">
        <Link to={signedIn ? "/path" : "/login"}>{signedIn ? "Go to your path" : "Sign in"}</Link>
      </Button>
    </div>
  )
}

/** AI word generation is premium, so free users see it locked. */
function GenerateWithAI({ premium, onOpen }: { premium: boolean; onOpen: () => void }) {
  if (!premium) {
    return (
      <Button variant="secondary" disabled title="Generating words with AI is a Premium feature">
        <Lock className="mr-2 size-4" /> Generate with AI
      </Button>
    )
  }
  return (
    <Button variant="secondary" onClick={onOpen}>
      <Sparkles className="mr-2 size-4" /> Generate with AI
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
