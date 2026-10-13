import { useMemo, useState } from "react"
import { useQuery } from "@tanstack/react-query"
import {
  BookOpen,
  ChevronLeft,
  ChevronRight,
  Layers,
  ListOrdered,
  Lock,
  Palette,
  PenLine,
  Shapes,
  Tags,
  Users,
  type LucideIcon,
} from "lucide-react"
import { Link } from "react-router-dom"

import { fetchGrammarRules, fetchNextGrammarTopic } from "@/api/grammar"
import type { GrammarCategory, GrammarNext, GrammarRule } from "@/types"
import { useAuth } from "@/contexts/AuthContext"
import { GRAMMAR_CATEGORIES, grammarCategoryLabel } from "@/lib/labels"
import { PageHeader } from "@/components/layout/PageHeader"
import { Card } from "@/components/ui/card"
import { GrammarCard } from "@/components/grammar/GrammarCard"
import { Button } from "@/components/ui/button"
import { cn } from "@/lib/utils"
import { BackLink } from "@/components/ui/BackLink"
import { SearchField } from "@/components/ui/SearchField"

/** Each category's icon and colour (one of the six unit colours). */
const CATEGORY_LOOK: Record<GrammarCategory, { icon: LucideIcon; color: string }> = {
  articles: { icon: Tags, color: "hsl(var(--section-1))" },
  cases: { icon: Layers, color: "hsl(var(--section-2))" },
  verbs: { icon: PenLine, color: "hsl(var(--section-6))" },
  sentence_structure: { icon: ListOrdered, color: "hsl(var(--section-3))" },
  pronouns: { icon: Users, color: "hsl(var(--section-5))" },
  adjectives: { icon: Palette, color: "hsl(var(--section-4))" },
  other: { icon: Shapes, color: "hsl(var(--muted-foreground))" },
}

function lookFor(category: string) {
  return CATEGORY_LOOK[category as GrammarCategory] ?? CATEGORY_LOOK.other
}

/** The first sentence of a topic's explanation, without Markdown marks. */
function preview(content: string): string {
  const text = content
    .split("\n")
    .map((l) =>
      l
        .replace(/^\s*([-*+]|\d+\.)\s+/, "")
        .replace(/[#>*_`|]/g, "")
        .trim(),
    )
    .find((l) => l.length > 0 && !/^-+$/.test(l))
  return text ?? ""
}

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
      <div className="mx-auto flex max-w-3xl flex-col gap-4">
        <BackLink onClick={() => setOpenId(null)} label="All topics" />
        <p className="flex items-center gap-2.5 text-[13px] font-semibold uppercase tracking-[0.04em] text-muted-foreground">
          <CategoryIcon category={rule.category} size="sm" />
          {rule.cefr_level} · {grammarCategoryLabel(rule.category)}
        </p>
        <GrammarCard rule={rule} />
        <div className="mt-2 flex items-center justify-between gap-3">
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
      <PageHeader title="Grammar" subtitle="The rules behind the words, unlocked as your lessons teach them." />

      {all.length > 0 && (
        <div className={cn("grid gap-4", next && "md:grid-cols-[1fr_1.2fr]")}>
          <Card className="flex min-w-0 items-center gap-4 p-5">
            <span className="flex size-14 shrink-0 items-center justify-center rounded-2xl bg-primary text-primary-foreground">
              <BookOpen className="size-7" aria-hidden="true" />
            </span>
            <div className="min-w-0">
              <p className="font-grotesk text-3xl font-extrabold tabular-nums">{all.length}</p>
              <p className="text-sm text-muted-foreground">
                {all.length === 1 ? "topic" : "topics"} learned across{" "}
                {new Set(all.map((r) => r.category)).size} areas
              </p>
            </div>
          </Card>
          {next && <NextTopic next={next} />}
        </div>
      )}

      <SearchField
        value={query}
        onChange={setQuery}
        placeholder="Search grammar, e.g. accusative, sein, plurals"
      />

      {isLoading ? null : levels.length === 0 ? (
        <Card className="mx-auto flex max-w-md flex-col items-center gap-3 px-6 py-12 text-center">
          <span className="flex size-16 items-center justify-center rounded-2xl bg-surface-2 text-muted-foreground">
            <BookOpen className="size-8" aria-hidden="true" />
          </span>
          <p className="mt-2 text-muted-foreground">
            {query
              ? `No topics match “${query}”.`
              : "Grammar topics appear here as you finish the lessons that teach them."}
          </p>
        </Card>
      ) : (
        levels.map(([level, levelRules]) => (
          <LevelSection key={level} level={level} rules={levelRules} onOpen={setOpenId} />
        ))
      )}

      {all.length === 0 && next && <NextTopic next={next} />}
    </div>
  )
}

/** One quiet line about the next topic on your path. */
function NextTopic({ next }: { next: GrammarNext }) {
  return (
    <Link
      to={`/path/${next.lesson.unit_id}`}
      className="lift flex min-w-0 items-center gap-4 rounded-2xl bg-surface p-5 shadow-card"
    >
      <span className="flex size-11 shrink-0 items-center justify-center rounded-2xl bg-surface-2 text-muted-foreground">
        <Lock className="size-5" aria-hidden="true" />
      </span>
      <span className="min-w-0 flex-1">
        <span className="block text-xs font-semibold uppercase tracking-[0.04em] text-muted-foreground">
          Coming up
        </span>
        <span className="block font-semibold">{next.title}</span>
        <span className="block truncate text-sm text-muted-foreground">
          Lektion {next.lesson.unit_order}: {next.lesson.unit_title}
        </span>
      </span>
      <ChevronRight className="size-5 shrink-0 text-muted-foreground" aria-hidden="true" />
    </Link>
  )
}

function CategoryIcon({ category, size = "md" }: { category: string; size?: "sm" | "md" }) {
  const { icon: Icon, color } = lookFor(category)
  return (
    <span
      className={cn(
        "flex shrink-0 items-center justify-center text-white",
        size === "sm" ? "size-7 rounded-lg" : "size-11 rounded-2xl",
      )}
      style={{ background: color }}
    >
      <Icon className={size === "sm" ? "size-4" : "size-5"} aria-hidden="true" />
    </span>
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
      <div className="mb-3 flex items-baseline gap-3 px-1">
        <h2 className="text-[22px] font-bold">{level}</h2>
        <span className="text-sm text-muted-foreground">{rules.length} topics</span>
      </div>

      <div className="gap-5 lg:columns-2">
        {groups.map((g) => (
          <Card key={g.value} className="mb-5 overflow-hidden break-inside-avoid">
            <div className="flex items-center gap-3 px-5 pb-2 pt-5">
              <CategoryIcon category={g.value} />
              <div>
                <h3 className="text-lg font-bold leading-tight">{g.label}</h3>
                <p className="text-sm text-muted-foreground">
                  {g.items.length} {g.items.length === 1 ? "topic" : "topics"}
                </p>
              </div>
            </div>
            <div className="p-1.5">
              {g.items.map((rule, i) => (
                <div key={rule.id}>
                  {i > 0 && <div className="mx-3.5 h-px bg-border/70" aria-hidden="true" />}
                  <button
                    onClick={() => onOpen(rule.id)}
                    className="flex min-h-[60px] w-full items-center justify-between gap-3 rounded-xl px-3.5 py-2.5 text-left transition-colors hover:bg-surface-2"
                  >
                    <span className="min-w-0">
                      <span className="block font-semibold">{rule.title}</span>
                      {preview(rule.content) && (
                        <span className="block truncate text-sm text-muted-foreground">
                          {preview(rule.content)}
                        </span>
                      )}
                    </span>
                    <ChevronRight className="size-5 shrink-0 text-muted-foreground" aria-hidden="true" />
                  </button>
                </div>
              ))}
            </div>
          </Card>
        ))}
      </div>
    </section>
  )
}
