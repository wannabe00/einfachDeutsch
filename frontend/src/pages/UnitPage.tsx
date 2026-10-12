import { Link, useParams } from "react-router-dom"
import { useQuery } from "@tanstack/react-query"
import { ArrowLeft } from "lucide-react"

import { fetchUnit } from "@/api/curriculum"
import type { UnitGrammar, UnitWord } from "@/types"
import { resolveAccent } from "@/lib/sections"
import { grammarCategoryLabel } from "@/lib/labels"
import { PageHeader } from "@/components/layout/PageHeader"
import { Card } from "@/components/ui/card"
import { Markdown } from "@/components/ui/Markdown"
import { LessonTrail } from "@/components/path/LessonTrail"

/*
 * One unit: the lesson road on the left, and the Lektion's grammar and full
 * word list on the right, so there's something to study before the first lesson.
 */
export default function UnitPage() {
  const { unitId } = useParams()
  const id = Number(unitId)
  const { data, isLoading, isError } = useQuery({
    queryKey: ["unit", id],
    queryFn: () => fetchUnit(id),
    enabled: Number.isFinite(id),
  })

  if (isLoading) return <Centered>Loading unit…</Centered>
  if (isError || !data) return <Centered>Couldn’t load this unit.</Centered>

  const accent = resolveAccent(data.accent_color, data.order - 1)
  const done = data.lessons.filter((l) => l.state === "completed").length

  return (
    <div className="flex flex-col gap-6">
      <Link
        to="/path"
        className="inline-flex w-fit items-center gap-1.5 text-sm text-muted-foreground transition-colors hover:text-foreground"
      >
        <ArrowLeft className="size-4" /> All units
      </Link>

      <PageHeader
        title={data.title}
        subtitle={`Unit ${data.order} · ${data.cefr_level}${data.theme ? ` · ${data.theme}` : ""} · ${done}/${data.lessons.length} lessons done`}
      />

      <div className="grid gap-8 lg:grid-cols-[280px_1fr]">
        <LessonTrail lessons={data.lessons} accent={accent} unitId={data.id} />

        <div className="flex min-w-0 flex-col gap-4">
          {data.grammar.map((rule) => (
            <GrammarPanel key={rule.id} rule={rule} />
          ))}
          <VocabPanel words={data.words} />
        </div>
      </div>

    </div>
  )
}

function GrammarPanel({ rule }: { rule: UnitGrammar }) {
  const examples = rule.example_sentences.split("\n").filter(Boolean)
  return (
    <Card>
      <div className="p-5">
        <p className="text-xs font-semibold uppercase tracking-wider text-muted-foreground">
          {grammarCategoryLabel(rule.category)}
        </p>
        <h3 className="mt-1 text-lg font-bold">{rule.title}</h3>
        <Markdown className="mt-2 text-muted-foreground">{rule.content}</Markdown>
        {examples.length > 0 && (
          <ul className="mt-3 space-y-1 border-t border-border pt-3">
            {examples.map((ex) => (
              <li key={ex} className="text-sm text-foreground">
                {ex}
              </li>
            ))}
          </ul>
        )}
      </div>
    </Card>
  )
}

function VocabPanel({ words }: { words: UnitWord[] }) {
  if (words.length === 0) return null
  return (
    <Card>
      <div className="p-5">
        <p className="text-xs font-semibold uppercase tracking-wider text-muted-foreground">
          Quick review
        </p>
        <h3 className="mt-1 text-lg font-bold">
          Wortschatz <span className="text-muted-foreground">({words.length})</span>
        </h3>
        <ul className="mt-3 grid gap-x-6 gap-y-1.5 sm:grid-cols-2">
          {words.map((w) => (
            <li key={w.id} className="flex items-baseline justify-between gap-3 border-b border-border/60 py-1">
              <span className="font-medium">{w.german}</span>
              <span className="shrink-0 text-sm text-muted-foreground">{w.english}</span>
            </li>
          ))}
        </ul>
      </div>
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
