import { useMemo, useState } from "react"
import { useQuery } from "@tanstack/react-query"
import { Lock, Plus, Search, Sparkles } from "lucide-react"

import { fetchWords } from "@/api/vocabulary"
import { fetchBooks } from "@/api/books"
import type { Chapter, Word } from "@/types"
import { PARTS_OF_SPEECH, partOfSpeechLabel } from "@/lib/labels"
import { sectionColor } from "@/lib/sections"
import { cn } from "@/lib/utils"
import { useAuth } from "@/contexts/AuthContext"
import { useAIPanel } from "@/contexts/AIPanelContext"
import { PageHeader } from "@/components/layout/PageHeader"
import { SectionCard } from "@/components/ui/SectionCard"
import { Button } from "@/components/ui/button"
import { WordForm } from "@/components/vocabulary/WordForm"
import { CSVImportButton } from "@/components/vocabulary/CSVImportButton"
import { PasteWordsButton } from "@/components/vocabulary/PasteWordsButton"

/*
 * Word Bank v2 (Phase 23.9). Grouped **Level → part of speech** — no Lektion
 * numbers, which meant nothing outside the book. Level-gating is server-side
 * (only ≤ your level is ever returned); words from a Lektion at your own level
 * that you haven't reached come back `locked` and are shown blurred.
 */
export default function WordBankPage() {
  const { user } = useAuth()
  const { openPanel } = useAIPanel()
  const [showForm, setShowForm] = useState(false)
  const [query, setQuery] = useState("")

  const { data: books } = useQuery({ queryKey: ["books"], queryFn: fetchBooks })
  const { data: words, isLoading } = useQuery({
    queryKey: ["words", "all"],
    queryFn: () => fetchWords(),
  })

  const allChapters: Chapter[] = books?.flatMap((b) => b.chapters) ?? []

  const filtered = useMemo(() => {
    const q = query.trim().toLowerCase()
    if (!q) return words ?? []
    return (words ?? []).filter((w) =>
      `${w.german} ${w.english}`.toLowerCase().includes(q),
    )
  }, [words, query])

  // Level → part of speech. Levels descend so your current level leads.
  const levels = useMemo(() => {
    const byLevel = new Map<string, Word[]>()
    for (const w of filtered) {
      const list = byLevel.get(w.cefr_level) ?? []
      list.push(w)
      byLevel.set(w.cefr_level, list)
    }
    return [...byLevel.entries()].sort((a, b) => b[0].localeCompare(a[0]))
  }, [filtered])

  const lockedCount = filtered.filter((w) => w.locked).length

  return (
    <div className="flex flex-col gap-6">
      <PageHeader
        title="Word Bank"
        subtitle={
          <>
            {words?.length ?? 0} words up to your level
            {lockedCount > 0 && ` · ${lockedCount} still locked`}
          </>
        }
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
        <SectionCard>
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
        </SectionCard>
      )}

      <div className="relative">
        <Search className="pointer-events-none absolute left-3 top-1/2 size-4 -translate-y-1/2 text-muted-foreground" />
        <input
          value={query}
          onChange={(e) => setQuery(e.target.value)}
          placeholder="Search your words — German or English…"
          className="w-full rounded-lg border border-border bg-surface py-2.5 pl-10 pr-3 text-sm focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring"
        />
      </div>

      {isLoading ? (
        <Centered>Loading your words…</Centered>
      ) : levels.length === 0 ? (
        <Centered>{query ? `No words match “${query}”.` : "No words yet."}</Centered>
      ) : (
        levels.map(([level, levelWords], i) => (
          <LevelSection key={level} level={level} words={levelWords} index={i} />
        ))
      )}
    </div>
  )
}

function LevelSection({ level, words, index }: { level: string; words: Word[]; index: number }) {
  const accent = sectionColor(index)
  const groups = PARTS_OF_SPEECH.map((p) => ({
    ...p,
    items: words.filter((w) => w.part_of_speech === p.value),
  })).filter((g) => g.items.length > 0)

  return (
    <section>
      <div className="mb-3 flex items-baseline gap-3">
        <h2 className="text-xl font-bold" style={{ color: accent }}>
          {level}
        </h2>
        <span className="text-sm text-muted-foreground">{words.length} words</span>
      </div>

      <div className="flex flex-col gap-4">
        {groups.map((g) => (
          <SectionCard key={g.value} accent={accent}>
            <div className="p-5">
              <p className="text-xs font-semibold uppercase tracking-wider text-muted-foreground">
                {partOfSpeechLabel(g.value)}{" "}
                <span className="text-muted-foreground/60">({g.items.length})</span>
              </p>
              <ul className="mt-3 grid gap-x-6 gap-y-1.5 sm:grid-cols-2 lg:grid-cols-3">
                {g.items.map((w) => (
                  <WordItem key={w.id} word={w} />
                ))}
              </ul>
            </div>
          </SectionCard>
        ))}
      </div>
    </section>
  )
}

function WordItem({ word }: { word: Word }) {
  const learned = (word.progress?.repetitions ?? 0) > 0

  if (word.locked) {
    return (
      <li
        className="flex items-baseline justify-between gap-3 border-b border-border/60 py-1"
        title="Reach this lesson on your path to unlock"
      >
        <span className="select-none blur-[4px]" aria-hidden>
          {word.german}
        </span>
        <Lock className="size-3 shrink-0 text-muted-foreground" />
      </li>
    )
  }

  return (
    <li className="flex items-baseline justify-between gap-3 border-b border-border/60 py-1">
      <span className={cn("font-medium", learned && "text-[hsl(var(--success))]")}>
        {word.german}
      </span>
      <span className="shrink-0 text-sm text-muted-foreground">{word.english}</span>
    </li>
  )
}

/** AI generation is premium (Spec v3) — free users see it locked. */
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
