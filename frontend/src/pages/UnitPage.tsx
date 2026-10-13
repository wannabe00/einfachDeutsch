import { useParams } from "react-router-dom"
import { useQuery } from "@tanstack/react-query"

import { fetchUnit } from "@/api/curriculum"
import type { UnitGrammar, UnitWord } from "@/types"
import { grammarCategoryLabel } from "@/lib/labels"
import { BackLink } from "@/components/ui/BackLink"
import { Card } from "@/components/ui/card"
import { Markdown } from "@/components/ui/Markdown"
import { LektionCover } from "@/components/lektion/LektionCover"
import { LessonRows } from "@/components/lektion/LessonRows"
import { ProgressRing } from "@/components/lektion/ProgressRing"
import { lektionColor } from "@/components/lektion/lektionColor"

/*
 * One Lektion: a cover header, its lessons, then the grammar and full word
 * list, so there's something to study before the first lesson.
 */
export default function UnitPage() {
  const { unitId } = useParams()
  const id = Number(unitId)
  const { data, isLoading, isError } = useQuery({
    queryKey: ["unit", id],
    queryFn: () => fetchUnit(id),
    enabled: Number.isFinite(id),
  })

  if (isLoading) return <Centered>Loading Lektion…</Centered>
  if (isError || !data) return <Centered>Couldn’t load this Lektion.</Centered>

  const color = lektionColor(data.order)
  const done = data.lessons.filter((l) => l.state === "completed").length
  const total = data.lessons.length

  return (
    <div className="flex flex-col gap-6">
      <BackLink to="/path" label="Path" />

      <header className="grid overflow-hidden rounded-[24px] bg-surface shadow-card sm:grid-cols-[220px_1fr]">
        <LektionCover order={data.order} level={data.cefr_level} className="h-40 sm:h-full sm:min-h-[200px]" />
        <div className="flex min-w-0 flex-col justify-center gap-1.5 p-5 sm:p-6">
          <p className="text-[13px] font-semibold uppercase tracking-[0.04em]" style={{ color }}>
            Lektion {data.order} · {data.cefr_level}
          </p>
          <h1 className="text-[28px] font-extrabold leading-tight sm:text-[34px]">{data.title}</h1>
          {data.theme && <p className="text-muted-foreground">{data.theme}</p>}
          <div className="mt-2 flex items-center gap-3">
            <ProgressRing pct={total > 0 ? done / total : 0} color={color} size={40} stroke={5} />
            <span className="text-sm text-muted-foreground">
              {done} of {total} lessons done
            </span>
          </div>
        </div>
      </header>

      <section>
        <h2 className="mb-3 px-1 text-[22px] font-bold">Lessons</h2>
        <Card className="p-3 sm:p-4">
          <LessonRows lessons={data.lessons} unitId={data.id} />
        </Card>
      </section>

      {data.grammar.length > 0 && (
        <section className="flex flex-col gap-3">
          <h2 className="px-1 text-[22px] font-bold">Grammatik</h2>
          {data.grammar.map((rule) => (
            <GrammarPanel key={rule.id} rule={rule} />
          ))}
        </section>
      )}

      <VocabPanel words={data.words} />
    </div>
  )
}

function GrammarPanel({ rule }: { rule: UnitGrammar }) {
  const examples = rule.example_sentences.split("\n").filter(Boolean)
  return (
    <Card>
      <div className="p-5 sm:p-6">
        <p className="text-[13px] font-semibold uppercase tracking-[0.04em] text-muted-foreground">
          {grammarCategoryLabel(rule.category)}
        </p>
        <h3 className="mt-1 text-xl font-bold">{rule.title}</h3>
        <Markdown className="mt-2 text-muted-foreground">{rule.content}</Markdown>
        {examples.length > 0 && (
          <ul className="mt-4 space-y-1.5 rounded-xl bg-surface-2/70 p-4">
            {examples.map((ex) => (
              <li key={ex} className="text-[15px]">
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
    <section>
      <h2 className="mb-3 px-1 text-[22px] font-bold">
        Wortschatz <span className="text-muted-foreground">{words.length}</span>
      </h2>
      <Card className="p-2 sm:p-3">
        <ul className="grid sm:grid-cols-2 sm:gap-x-4">
          {words.map((w) => (
            <li
              key={w.id}
              className="flex min-h-[48px] items-baseline justify-between gap-3 border-b border-border/60 px-3 py-2.5 last:border-0"
            >
              <span className="font-medium">{w.german}</span>
              <span className="shrink-0 text-right text-sm text-muted-foreground">{w.english}</span>
            </li>
          ))}
        </ul>
      </Card>
    </section>
  )
}

function Centered({ children }: { children: React.ReactNode }) {
  return (
    <div className="flex h-64 items-center justify-center">
      <p className="text-muted-foreground">{children}</p>
    </div>
  )
}
