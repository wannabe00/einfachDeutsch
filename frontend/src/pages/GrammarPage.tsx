import { useMemo, useState } from "react"
import { useQuery } from "@tanstack/react-query"
import { ArrowLeft, ArrowRight, ChevronLeft, ChevronRight, Lock, Search } from "lucide-react"
import { Link } from "react-router-dom"

import { fetchGrammarRules } from "@/api/grammar"
import type { GrammarRule } from "@/types"
import { GRAMMAR_CATEGORIES, grammarCategoryLabel } from "@/lib/labels"
import { sectionColor } from "@/lib/sections"
import { PageHeader } from "@/components/layout/PageHeader"
import { SectionCard } from "@/components/ui/SectionCard"
import { GrammarCard } from "@/components/grammar/GrammarCard"
import { Button } from "@/components/ui/button"

/*
 * Grammar v2 (Phase 23.10). Grouped **Level → topic** — no Lektion numbers.
 * Level-gating is server-side (only ≤ your level is returned); a topic at your
 * own level stays locked until the lesson that teaches it is done, and the
 * "next topic" banner points at whichever unlocks first.
 */
export default function GrammarPage() {
  const [openId, setOpenId] = useState<number | null>(null)
  const [query, setQuery] = useState("")

  const { data: rules } = useQuery({
    queryKey: ["grammar", "all"],
    queryFn: () => fetchGrammarRules(),
  })

  const all = useMemo(() => rules ?? [], [rules])

  const filtered = useMemo(() => {
    const q = query.trim().toLowerCase()
    if (!q) return all
    return all.filter((r) =>
      `${r.title} ${grammarCategoryLabel(r.category)} ${r.locked ? "" : r.content}`
        .toLowerCase()
        .includes(q),
    )
  }, [all, query])

  // The locked topic whose lesson comes first on the path.
  const nextTopic = useMemo(() => {
    const locked = all.filter((r) => r.locked && r.unlock_lesson)
    return (
      locked.sort(
        (a, b) =>
          a.unlock_lesson!.unit_order - b.unlock_lesson!.unit_order ||
          a.unlock_lesson!.lesson_order - b.unlock_lesson!.lesson_order,
      )[0] ?? null
    )
  }, [all])

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
    const readable = filtered.filter((r) => !r.locked)
    const idx = readable.findIndex((r) => r.id === openId)
    const rule = readable[idx]
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
            onClick={() => setOpenId(readable[idx - 1].id)}
          >
            <ChevronLeft className="size-4" /> Previous
          </Button>
          <span className="text-sm text-muted-foreground">
            {idx + 1} of {readable.length}
          </span>
          <Button
            variant="secondary"
            disabled={idx >= readable.length - 1}
            onClick={() => setOpenId(readable[idx + 1].id)}
          >
            Next <ChevronRight className="size-4" />
          </Button>
        </div>
      </div>
    )
  }

  // ---- Gallery view ------------------------------------------------------
  const lockedCount = all.filter((r) => r.locked).length

  return (
    <div className="flex flex-col gap-6">
      <PageHeader
        title="Grammar"
        subtitle={
          <>
            {all.length} topics up to your level
            {lockedCount > 0 && ` · ${lockedCount} still locked`}
          </>
        }
      />

      {nextTopic && <NextTopic rule={nextTopic} />}

      <div className="relative">
        <Search className="pointer-events-none absolute left-3 top-1/2 size-4 -translate-y-1/2 text-muted-foreground" />
        <input
          value={query}
          onChange={(e) => setQuery(e.target.value)}
          placeholder="Search grammar — e.g. accusative, sein, plurals…"
          className="w-full rounded-lg border border-border bg-surface py-2.5 pl-10 pr-3 text-sm focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring"
        />
      </div>

      {levels.length === 0 ? (
        <p className="py-10 text-center text-sm text-muted-foreground">
          {query ? `No topics match “${query}”.` : "No grammar topics yet."}
        </p>
      ) : (
        levels.map(([level, levelRules], i) => (
          <LevelSection key={level} level={level} rules={levelRules} index={i} onOpen={setOpenId} />
        ))
      )}
    </div>
  )
}

/** "Next topic" indicator — what unlocks next, and the lesson that does it. */
function NextTopic({ rule }: { rule: GrammarRule }) {
  const lesson = rule.unlock_lesson!
  return (
    <Link
      to={`/path/${lesson.unit_id}`}
      className="group flex items-center gap-4 rounded-2xl border border-white/10 bg-gradient-to-b from-surface-2 to-surface p-4 shadow-lg shadow-black/40 transition-transform hover:-translate-y-0.5"
    >
      <span
        className="flex size-12 shrink-0 items-center justify-center rounded-xl text-white"
        style={{ background: "hsl(var(--brand))" }}
      >
        <ArrowRight className="size-6 transition-transform group-hover:translate-x-0.5" />
      </span>
      <div className="min-w-0">
        <p className="text-xs font-semibold uppercase tracking-wider text-muted-foreground">
          Next topic
        </p>
        <p className="truncate font-bold">{rule.title}</p>
        <p className="truncate text-sm text-muted-foreground">
          Unlocks with “{lesson.title}” in {lesson.unit_title}
        </p>
      </div>
    </Link>
  )
}

function LevelSection({
  level,
  rules,
  index,
  onOpen,
}: {
  level: string
  rules: GrammarRule[]
  index: number
  onOpen: (id: number) => void
}) {
  const accent = sectionColor(index)
  const groups = GRAMMAR_CATEGORIES.map((c) => ({
    ...c,
    items: rules.filter((r) => r.category === c.value),
  })).filter((g) => g.items.length > 0)

  return (
    <section>
      <div className="mb-3 flex items-baseline gap-3">
        <h2 className="text-xl font-bold" style={{ color: accent }}>
          {level}
        </h2>
        <span className="text-sm text-muted-foreground">{rules.length} topics</span>
      </div>

      <div className="flex flex-col gap-4">
        {groups.map((g) => (
          <SectionCard key={g.value} accent={accent}>
            <div className="p-5">
              <p className="text-xs font-semibold uppercase tracking-wider text-muted-foreground">
                {g.label} <span className="text-muted-foreground/60">({g.items.length})</span>
              </p>
              <div className="mt-3 grid gap-2 sm:grid-cols-2">
                {g.items.map((rule) =>
                  rule.locked ? (
                    <LockedTopic key={rule.id} rule={rule} />
                  ) : (
                    <button
                      key={rule.id}
                      onClick={() => onOpen(rule.id)}
                      className="rounded-xl border border-border bg-surface px-4 py-3 text-left font-medium transition-colors hover:border-primary/50"
                    >
                      {rule.title}
                    </button>
                  ),
                )}
              </div>
            </div>
          </SectionCard>
        ))}
      </div>
    </section>
  )
}

function LockedTopic({ rule }: { rule: GrammarRule }) {
  const lesson = rule.unlock_lesson
  return (
    <div
      className="flex items-center justify-between gap-3 rounded-xl border border-dashed border-border px-4 py-3"
      title={lesson ? `Finish “${lesson.title}” in ${lesson.unit_title} to unlock` : "Locked"}
    >
      <span className="select-none truncate font-medium blur-[4px]" aria-hidden>
        {rule.title}
      </span>
      <Lock className="size-4 shrink-0 text-muted-foreground" />
    </div>
  )
}
