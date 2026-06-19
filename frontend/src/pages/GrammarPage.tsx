import { useMemo, useState } from "react"
import { useQuery } from "@tanstack/react-query"
import { ArrowLeft, ChevronLeft, ChevronRight, Search } from "lucide-react"

import { fetchGrammarRules } from "@/api/grammar"
import { fetchBooks } from "@/api/books"
import type { Chapter, GrammarRule } from "@/types"
import { grammarCategoryLabel } from "@/lib/labels"
import { GrammarCard } from "@/components/grammar/GrammarCard"
import { GrammarForm } from "@/components/grammar/GrammarForm"
import { Button } from "@/components/ui/button"

export default function GrammarPage() {
  const [openId, setOpenId] = useState<number | null>(null)
  const [query, setQuery] = useState("")
  const [showForm, setShowForm] = useState(false)

  const { data: books } = useQuery({ queryKey: ["books"], queryFn: fetchBooks })
  const { data: rules } = useQuery({
    queryKey: ["grammar", "all"],
    queryFn: () => fetchGrammarRules(),
  })

  const allChapters: Chapter[] = books?.flatMap((b) => b.chapters) ?? []
  const chapterShort = (id: number) =>
    (allChapters.find((c) => c.id === id)?.title ?? "—").replace(/ —.*/, "")
  const chapterFull = (id: number) =>
    allChapters.find((c) => c.id === id)?.title ?? "—"

  // Search across title, category, and content.
  const filtered = useMemo(() => {
    const q = query.trim().toLowerCase()
    if (!q) return rules ?? []
    return (rules ?? []).filter((r) =>
      `${r.title} ${grammarCategoryLabel(r.category)} ${r.content}`
        .toLowerCase()
        .includes(q),
    )
  }, [rules, query])

  // Group filtered rules under their chapter, preserving the API order.
  const groups = useMemo(() => {
    const map = new Map<number, GrammarRule[]>()
    for (const r of filtered) {
      if (!map.has(r.chapter)) map.set(r.chapter, [])
      map.get(r.chapter)!.push(r)
    }
    return [...map.entries()]
  }, [filtered])

  // ---- Reading view (a single rule opened) -------------------------------
  if (openId !== null) {
    const idx = filtered.findIndex((r) => r.id === openId)
    const rule = filtered[idx]
    if (!rule) {
      setOpenId(null)
      return null
    }
    return (
      <div>
        <button
          onClick={() => setOpenId(null)}
          className="inline-flex items-center gap-1.5 text-sm text-muted-foreground hover:text-accent"
        >
          <ArrowLeft className="size-4" /> All topics
        </button>
        <p className="mt-3 text-xs font-semibold uppercase tracking-wide text-muted-foreground">
          {chapterFull(rule.chapter)}
        </p>
        <div className="mt-3">
          <GrammarCard rule={rule} />
        </div>
        <div className="mt-6 flex items-center justify-between">
          <Button
            variant="secondary"
            disabled={idx <= 0}
            onClick={() => setOpenId(filtered[idx - 1].id)}
          >
            <ChevronLeft className="size-4" /> Previous
          </Button>
          <span className="text-sm text-muted-foreground">
            {idx + 1} of {filtered.length}
          </span>
          <Button
            variant="secondary"
            disabled={idx >= filtered.length - 1}
            onClick={() => setOpenId(filtered[idx + 1].id)}
          >
            Next <ChevronRight className="size-4" />
          </Button>
        </div>
      </div>
    )
  }

  // ---- Gallery view ------------------------------------------------------
  return (
    <div>
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-2xl font-semibold tracking-tight">Grammar</h1>
          <p className="mt-1 text-sm text-muted-foreground">
            {rules?.length ?? 0} topics
          </p>
        </div>
        <Button variant="secondary" onClick={() => setShowForm((v) => !v)}>
          {showForm ? "Cancel" : "Add topic"}
        </Button>
      </div>

      {showForm && allChapters.length > 0 && (
        <div className="mt-4 rounded-xl border border-border bg-surface p-4">
          <GrammarForm chapters={allChapters} onDone={() => setShowForm(false)} />
        </div>
      )}

      {/* Search */}
      <div className="relative mt-6">
        <Search className="pointer-events-none absolute left-3 top-1/2 size-4 -translate-y-1/2 text-muted-foreground" />
        <input
          value={query}
          onChange={(e) => setQuery(e.target.value)}
          placeholder="Search grammar — e.g. accusative, sein, plurals…"
          className="w-full rounded-lg border border-border bg-surface py-2.5 pl-10 pr-3 text-sm focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring"
        />
      </div>

      {/* Topic cards grouped by lesson */}
      {filtered.length === 0 ? (
        <p className="mt-8 text-sm text-muted-foreground">
          No topics match “{query}”.
        </p>
      ) : (
        <div className="mt-6 flex flex-col gap-8">
          {groups.map(([chapterId, items]) => (
            <section key={chapterId}>
              <h2 className="mb-3 text-xs font-semibold uppercase tracking-wide text-muted-foreground">
                {chapterShort(chapterId)}
              </h2>
              <div className="grid gap-3 sm:grid-cols-2">
                {items.map((rule) => (
                  <button
                    key={rule.id}
                    onClick={() => setOpenId(rule.id)}
                    className="group flex flex-col items-start gap-2 rounded-xl border border-border bg-surface p-4 text-left shadow-sm transition-all hover:border-accent hover:shadow-md"
                  >
                    <span className="rounded-full bg-muted px-2 py-0.5 text-xs font-medium text-muted-foreground">
                      {grammarCategoryLabel(rule.category)}
                    </span>
                    <span className="text-base font-semibold text-foreground group-hover:text-accent">
                      {rule.title}
                    </span>
                  </button>
                ))}
              </div>
            </section>
          ))}
        </div>
      )}
    </div>
  )
}
