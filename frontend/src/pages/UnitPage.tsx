import { Link, useParams } from "react-router-dom"
import { useQuery } from "@tanstack/react-query"
import ReactMarkdown from "react-markdown"
import { ArrowLeft, BookOpen, Sparkles } from "lucide-react"

import { fetchUnit } from "@/api/curriculum"
import type { UnitGrammar, UnitWord } from "@/types"
import { resolveAccent } from "@/lib/sections"
import { grammarCategoryLabel } from "@/lib/labels"
import { PageHeader } from "@/components/layout/PageHeader"
import { SectionCard } from "@/components/ui/SectionCard"
import { LessonTrail } from "@/components/path/LessonTrail"

/*
 * One unit's page (Phase 23.4b): the winding lesson road on the left, and a
 * review panel on the right (this Lektion's grammar + full Wortschatz) so the
 * page teaches something even before you tap a lesson.
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
        subtitle={`Unit ${data.order} · ${data.cefr_level}${data.theme ? ` · ${data.theme}` : ""} — ${done}/${data.lessons.length} lessons`}
      />

      <div className="grid gap-8 lg:grid-cols-[280px_1fr]">
        <LessonTrail lessons={data.lessons} accent={accent} />

        <div className="flex min-w-0 flex-col gap-4">
          {data.grammar.map((rule) => (
            <GrammarPanel key={rule.id} rule={rule} accent={accent} />
          ))}
          <VocabPanel words={data.words} accent={accent} />
        </div>
      </div>

      <p className="pb-4 text-center text-xs text-muted-foreground">
        Tapping a lesson opens the player — arriving in the next brick (23.5).
      </p>
    </div>
  )
}

function GrammarPanel({ rule, accent }: { rule: UnitGrammar; accent: string }) {
  const examples = rule.example_sentences.split("\n").filter(Boolean)
  return (
    <SectionCard accent={accent} glow>
      <div className="p-5">
        <p className="flex items-center gap-2 text-xs font-semibold uppercase tracking-wider text-muted-foreground">
          <BookOpen className="size-3.5" /> {grammarCategoryLabel(rule.category)}
        </p>
        <h3 className="mt-1 text-lg font-bold">{rule.title}</h3>
        <div className="prose-sm mt-2 space-y-1 text-sm text-muted-foreground [&_strong]:text-foreground">
          <ReactMarkdown>{rule.content}</ReactMarkdown>
        </div>
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
    </SectionCard>
  )
}

function VocabPanel({ words, accent }: { words: UnitWord[]; accent: string }) {
  if (words.length === 0) return null
  return (
    <SectionCard>
      <div className="p-5">
        <p className="flex items-center gap-2 text-xs font-semibold uppercase tracking-wider text-muted-foreground">
          <Sparkles className="size-3.5" style={{ color: accent }} /> Quick review
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
    </SectionCard>
  )
}

function Centered({ children }: { children: React.ReactNode }) {
  return (
    <div className="flex h-64 items-center justify-center">
      <p className="text-sm text-muted-foreground">{children}</p>
    </div>
  )
}
