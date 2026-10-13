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

  if (!rules) return <DrillShell title="Sentence Shuffle" onExit={onExit}><p className="py-10 text-center text-muted-foreground">Loading…</p></DrillShell>
  if (rounds.length === 0) return <DrillShell title="Sentence Shuffle" onExit={onExit}><p className="py-10 text-center text-muted-foreground">Finish a grammar lesson on your path to unlock sentences for this drill.</p></DrillShell>

  if (i >= rounds.length) {
    const pct = Math.round((score.correct / rounds.length) * 100)
    return (
      <DrillShell title="Sentence Shuffle" onExit={onExit}>
        <div className="mx-auto flex w-full max-w-md flex-col items-center gap-4 rounded-[28px] bg-surface px-6 py-10 text-center shadow-card">
          <h2 className="text-3xl font-extrabold">Drill complete</h2>
          <p className="font-grotesk text-6xl font-extrabold tracking-tight text-primary animate-in zoom-in-50 fade-in-0 duration-500">{pct}%</p>
          <p className="text-sm text-muted-foreground">{score.correct} correct · {score.wrong} wrong</p>
          <div className="mt-3 flex w-full flex-col gap-2.5">
            <Button size="lg" onClick={() => { setI(0); setScore({ correct: 0, wrong: 0 }); setBuilt([]); setVerdict(null) }}>Again</Button>
            <Button size="lg" variant="secondary" onClick={onExit}>Back to drills</Button>
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
        <div className="flex min-h-[64px] flex-wrap gap-2 rounded-2xl border-2 border-dashed border-border p-3">
          {built.length === 0 && <span className="self-center text-sm text-muted-foreground">…</span>}
          {built.map((slot, pos) => (
            <button
              key={pos}
              disabled={!!verdict}
              onClick={() => setBuilt(built.filter((_, j) => j !== pos))}
              className="min-h-[44px] rounded-xl bg-primary px-3.5 py-2 text-[15px] font-medium text-primary-foreground"
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
                className="min-h-[44px] rounded-xl bg-surface px-3.5 py-2 text-[15px] font-medium text-foreground shadow-card transition-colors hover:bg-surface-2"
              >
                {t.w}
              </button>
            ),
          )}
        </div>
        {verdict && (
          <p className={cn("text-center text-base font-semibold", verdict === "right" ? "text-[hsl(var(--success))]" : "text-[hsl(var(--danger))]")}>
            {verdict === "right" ? "Correct" : `Answer: ${round.words.join(" ")}`}
          </p>
        )}
        <Button size="lg" onClick={check} disabled={!verdict && built.length === 0}>
          {verdict ? "Next" : "Check"}
        </Button>
      </div>
    </DrillShell>
  )
}
