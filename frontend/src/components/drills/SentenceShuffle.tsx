import { useMemo, useState } from "react"
import { useQuery } from "@tanstack/react-query"

import { fetchGrammarRules } from "@/api/grammar"
import { collectSentences } from "@/lib/sentences"
import { shuffle, normalize } from "@/lib/german"
import { Button } from "@/components/ui/button"
import { cn } from "@/lib/utils"
import { DrillShell } from "./DrillShell"

const ROUNDS = 10

export function SentenceShuffle({ onExit }: { onExit: () => void }) {
  const { data: rules } = useQuery({
    queryKey: ["grammar", "chapter", undefined, undefined],
    queryFn: () => fetchGrammarRules(),
  })
  const [i, setI] = useState(0)
  const [score, setScore] = useState({ correct: 0, wrong: 0 })
  const [built, setBuilt] = useState<number[]>([]) // indices into the shuffled token list
  const [verdict, setVerdict] = useState<null | "right" | "wrong">(null)

  const rounds = useMemo(() => {
    return shuffle(collectSentences(rules ?? []))
      .slice(0, ROUNDS)
      .map((s) => {
        const words = s.replace(/\s+/g, " ").trim().split(" ")
        return { words, scrambled: shuffle(words.map((w, idx) => ({ w, idx }))) }
      })
  }, [rules])

  if (!rules) return <DrillShell title="Sentence Shuffle" onExit={onExit}><p className="text-sm text-muted-foreground">Loading…</p></DrillShell>
  if (rounds.length === 0) return <DrillShell title="Sentence Shuffle" onExit={onExit}><p className="text-sm text-muted-foreground">No sentences available yet.</p></DrillShell>

  if (i >= rounds.length) {
    const pct = Math.round((score.correct / rounds.length) * 100)
    return (
      <DrillShell title="Sentence Shuffle" onExit={onExit}>
        <div className="flex flex-col items-center gap-6 py-16 text-center">
          <h2 className="text-2xl font-semibold">Drill complete</h2>
          <p className="text-5xl font-bold text-accent">{pct}%</p>
          <p className="text-sm text-muted-foreground">{score.correct} correct · {score.wrong} wrong</p>
          <div className="flex gap-3">
            <Button onClick={() => { setI(0); setScore({ correct: 0, wrong: 0 }); setBuilt([]); setVerdict(null) }}>Again</Button>
            <Button variant="secondary" onClick={onExit}>Back to drills</Button>
          </div>
        </div>
      </DrillShell>
    )
  }

  const round = rounds[i]
  const usedSlots = new Set(built)

  function check() {
    if (verdict) { setVerdict(null); setBuilt([]); setI((n) => n + 1); return }
    const answer = built.map((slot) => round.scrambled[slot].w)
    const ok = normalize(answer.join(" ")) === normalize(round.words.join(" "))
    setVerdict(ok ? "right" : "wrong")
    setScore((s) => ({ correct: s.correct + (ok ? 1 : 0), wrong: s.wrong + (ok ? 0 : 1) }))
  }

  return (
    <DrillShell title="Sentence Shuffle" onExit={onExit} progress={(i / rounds.length) * 100} counter={`${i + 1} / ${rounds.length}`}>
      <div className="mx-auto flex max-w-lg flex-col gap-4 py-6">
        <p className="text-center text-sm text-muted-foreground">Tap the words to rebuild the sentence.</p>
        <div className="flex min-h-[52px] flex-wrap gap-2 rounded-lg border border-dashed border-border bg-background p-3">
          {built.length === 0 && <span className="self-center text-sm text-muted-foreground">…</span>}
          {built.map((slot, pos) => (
            <button
              key={pos}
              disabled={!!verdict}
              onClick={() => setBuilt(built.filter((_, j) => j !== pos))}
              className="rounded-md bg-accent px-2.5 py-1 text-sm text-accent-foreground"
            >
              {round.scrambled[slot].w}
            </button>
          ))}
        </div>
        <div className="flex flex-wrap justify-center gap-2">
          {round.scrambled.map((t, slot) =>
            usedSlots.has(slot) ? null : (
              <button
                key={slot}
                disabled={!!verdict}
                onClick={() => setBuilt([...built, slot])}
                className="rounded-md border border-border bg-surface px-2.5 py-1 text-sm text-foreground hover:border-accent"
              >
                {t.w}
              </button>
            ),
          )}
        </div>
        {verdict && (
          <p className={cn("text-center text-sm font-medium", verdict === "right" ? "text-[hsl(var(--success))]" : "text-[hsl(var(--danger))]")}>
            {verdict === "right" ? "✓ Perfect!" : `✗ ${round.words.join(" ")}`}
          </p>
        )}
        <Button onClick={check} disabled={!verdict && built.length === 0}>
          {verdict ? "Next" : "Check"}
        </Button>
      </div>
    </DrillShell>
  )
}
