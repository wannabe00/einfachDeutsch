import { useMemo, useState } from "react"
import { useQuery } from "@tanstack/react-query"

import { fetchWords } from "@/api/vocabulary"
import { splitArticle, shuffle } from "@/lib/german"
import { useGuestLimit } from "@/contexts/GuestLimitContext"
import { Button } from "@/components/ui/button"
import { cn } from "@/lib/utils"
import { DrillShell } from "./DrillShell"

const ROUNDS = 15
const ARTICLES = ["der", "die", "das"] as const
// Full, literal class strings so Tailwind can see them at build time (it scans
// source text — a `var(--${...})` interpolation would emit unparseable CSS).
const ARTICLE_TEXT: Record<string, string> = {
  der: "text-[hsl(var(--article-der))]",
  die: "text-[hsl(var(--article-die))]",
  das: "text-[hsl(var(--article-das))]",
}

export function GenderTriage({ onExit }: { onExit: () => void }) {
  const { data: words } = useQuery({ queryKey: ["words", "all"], queryFn: () => fetchWords() })
  const [i, setI] = useState(0)
  const [score, setScore] = useState({ correct: 0, wrong: 0 })
  const [picked, setPicked] = useState<string | null>(null)
  const { guard } = useGuestLimit()

  const pool = useMemo(() => {
    const nouns = (words ?? [])
      .map((w) => {
        const s = splitArticle(w.german)
        return { article: s.article, noun: s.noun, english: w.english }
      })
      .filter((x): x is { article: string; noun: string; english: string } =>
        Boolean(x.article),
      )
    return shuffle(nouns).slice(0, ROUNDS)
  }, [words])

  if (!words) return <DrillShell title="Gender Triage" onExit={onExit}><p className="text-sm text-muted-foreground">Loading…</p></DrillShell>
  if (pool.length === 0)
    return (
      <DrillShell title="Gender Triage" onExit={onExit}>
        <p className="text-sm text-muted-foreground">No nouns with articles found. Add some words first.</p>
      </DrillShell>
    )

  if (i >= pool.length) {
    return (
      <DrillShell title="Gender Triage" onExit={onExit}>
        <Summary score={score} total={pool.length} onAgain={() => { setI(0); setScore({ correct: 0, wrong: 0 }); setPicked(null) }} onExit={onExit} />
      </DrillShell>
    )
  }

  const current = pool[i]
  function choose(a: string) {
    if (picked) return
    if (!guard()) return // guests: blocked once the daily free cap is hit
    setPicked(a)
    const ok = a === current.article
    setScore((s) => ({ correct: s.correct + (ok ? 1 : 0), wrong: s.wrong + (ok ? 0 : 1) }))
    setTimeout(() => {
      setPicked(null)
      setI((n) => n + 1)
    }, 800)
  }

  return (
    <DrillShell title="Gender Triage" onExit={onExit} progress={(i / pool.length) * 100} counter={`${i + 1} / ${pool.length}`}>
      <div className="mx-auto flex max-w-md flex-col items-center gap-8 py-6">
        <div className="text-center">
          <p className="text-3xl font-semibold text-foreground">{current.noun}</p>
          <p className="mt-2 text-sm text-muted-foreground">{current.english}</p>
        </div>
        <div className="grid w-full grid-cols-3 gap-3">
          {ARTICLES.map((a) => {
            const isCorrect = picked && a === current.article
            const isWrongPick = picked === a && a !== current.article
            return (
              <button
                key={a}
                onClick={() => choose(a)}
                disabled={!!picked}
                className={cn(
                  "rounded-xl border-2 py-6 text-xl font-bold transition-colors",
                  isCorrect
                    ? "border-[hsl(var(--success))] bg-[hsl(var(--success-bg))] text-[hsl(var(--success))]"
                    : isWrongPick
                      ? "border-[hsl(var(--danger))] bg-[hsl(var(--danger-bg))] text-[hsl(var(--danger))]"
                      : "border-border bg-surface hover:border-accent " +
                        ARTICLE_TEXT[a],
                )}
              >
                {a}
              </button>
            )
          })}
        </div>
      </div>
    </DrillShell>
  )
}

function Summary({ score, total, onAgain, onExit }: { score: { correct: number; wrong: number }; total: number; onAgain: () => void; onExit: () => void }) {
  const pct = total ? Math.round((score.correct / total) * 100) : 0
  return (
    <div className="flex flex-col items-center gap-6 py-16 text-center">
      <h2 className="text-2xl font-semibold">Drill complete</h2>
      <p className="text-5xl font-bold text-accent">{pct}%</p>
      <p className="text-sm text-muted-foreground">{score.correct} correct · {score.wrong} wrong</p>
      <div className="flex gap-3">
        <Button onClick={onAgain}>Again</Button>
        <Button variant="secondary" onClick={onExit}>Back to drills</Button>
      </div>
    </div>
  )
}
