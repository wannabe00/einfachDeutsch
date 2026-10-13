import { useMemo, useState } from "react"
import { useQuery } from "@tanstack/react-query"
import { ArrowLeft, ChevronLeft, ChevronRight, Search } from "lucide-react"
import { Link } from "react-router-dom"

import { fetchGrammarRules, fetchNextGrammarTopic } from "@/api/grammar"
import type { GrammarNext, GrammarRule } from "@/types"
import { useAuth } from "@/contexts/AuthContext"
import { GRAMMAR_CATEGORIES, grammarCategoryLabel } from "@/lib/labels"
import { PageHeader } from "@/components/layout/PageHeader"
import { Card } from "@/components/ui/card"
import { GrammarCard } from "@/components/grammar/GrammarCard"
import { Button } from "@/components/ui/button"

/*
 * The grammar topics you've learned, grouped by level, then by kind. A topic
 * appears once you finish the lesson that teaches it; one quiet line says
 * which topic comes next on your path.
 */
export default function GrammarPage() {
  const { user } = useAuth()
  const [openId, setOpenId] = useState<number | null>(null)
  const [query, setQuery] = useState("")

  const { data: rules, isLoading } = useQuery({
    queryKey: ["grammar", "all"],
    queryFn: () => fetchGrammarRules(),
  })
  const { data: next } = useQuery({
    queryKey: ["grammar", "next"],
    queryFn: fetchNextGrammarTopic,
    enabled: !!user,
  })

  const all = useMemo(() => rules ?? [], [rules])

  const filtered = useMemo(() => {
    const q = query.trim().toLowerCase()
    if (!q) return all
    return all.filter((r) =>
      `${r.title} ${grammarCategoryLabel(r.category)} ${r.content}`
        .toLowerCase()
        .includes(q),
    )
  }, [all, query])

  const levels = useMemo(() => {
    const byLevel = new Map<string, GrammarRule[]>()
    for (const r of filtered) {
      const list = byLevel.get(r.cefr_level) ?? []
      list.push(r)
      byLevel.set(r.cefr_level, list)
    }
    return [...byLevel.entries()].sort((a, b) => b[0].localeCompare(a[0]))
  }, [filtered])

  // ---- Reading view (one topic opened) -----------------------------------
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
          className="inline-flex items-center gap-1.5 text-sm text-muted-foreground transition-colors hover:text-foreground"
        >
          <ArrowLeft className="size-4" /> All topics
        </button>
        <p className="mt-3 text-xs font-semibold uppercase tracking-wide text-muted-foreground">
          {rule.cefr_level} · {grammarCategoryLabel(rule.category)}
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
    <div className="flex flex-col gap-6">
      <PageHeader title="Grammar" subtitle={`${all.length} topics learned`} />

      <div className="relative">
        <Search className="pointer-events-none absolute left-3 top-1/2 size-4 -translate-y-1/2 text-muted-foreground" />
        <input
          value={query}
          onChange={(e) => setQuery(e.target.value)}
          placeholder="Search grammar, e.g. accusative, sein, plurals"
          className="w-full rounded-lg border border-border bg-surface py-2.5 pl-10 pr-3 text-sm focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring"
        />
      </div>

      {isLoading ? null : levels.length === 0 ? (
        <p className="py-10 text-center text-sm text-muted-foreground">
          {query
            ? `No topics match “${query}”.`
            : "Grammar topics appear here as you finish the lessons that teach them."}
        </p>
      ) : (
        levels.map(([level, levelRules]) => (
          <LevelSection key={level} level={level} rules={levelRules} onOpen={setOpenId} />
        ))
      )}

      {next && <NextTopic next={next} />}
    </div>
  )
}

/** One quiet line about the next topic on your path. */
function NextTopic({ next }: { next: GrammarNext }) {
  return (
    <p className="text-center text-sm text-muted-foreground">
      Coming up: <span className="text-foreground">{next.title}</span>, in{" "}
      <Link to={`/path/${next.lesson.unit_id}`} className="underline hover:text-foreground">
        Lektion {next.lesson.unit_order}: {next.lesson.unit_title}
      </Link>
    </p>
  )
}

function LevelSection({
  level,
  rules,
  onOpen,
}: {
  level: string
  rules: GrammarRule[]
  onOpen: (id: number) => void
}) {
  const groups = GRAMMAR_CATEGORIES.map((c) => ({
    ...c,
    items: rules.filter((r) => r.category === c.value),
  })).filter((g) => g.items.length > 0)

  return (
    <section>
      <div className="mb-3 flex items-baseline gap-3">
        <h2 className="text-xl font-bold">
          {level}
        </h2>
        <span className="text-sm text-muted-foreground">{rules.length} topics</span>
      </div>

      <div className="flex flex-col gap-4">
        {groups.map((g) => (
          <Card key={g.value}>
            <div className="p-5">
              <p className="text-xs font-semibold uppercase tracking-wider text-muted-foreground">
                {g.label} <span className="text-muted-foreground/60">({g.items.length})</span>
              </p>
              <div className="mt-3 grid gap-2 sm:grid-cols-2">
                {g.items.map((rule) => (
                  <button
                    key={rule.id}
                    onClick={() => onOpen(rule.id)}
                    className="rounded-xl border border-border bg-surface px-4 py-3 text-left font-medium transition-colors hover:bg-surface-2"
                  >
                    {rule.title}
                  </button>
                ))}
              </div>
            </div>
          </Card>
        ))}
      </div>
    </section>
  )
}
