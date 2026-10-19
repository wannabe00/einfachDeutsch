import { useMemo, useState } from "react"
import { useQuery } from "@tanstack/react-query"

import { fetchDrillWords } from "@/api/vocabulary"
import { shuffle, normalize } from "@/lib/german"
import { Button } from "@/components/ui/button"
import { cn } from "@/lib/utils"
import { DrillShell } from "./DrillShell"

const PER_ROUND = 5
const ROUNDS = 5

export function MatchPairs({ onExit }: { onExit: () => void }) {
  const { data: words } = useQuery({ queryKey: ["drill-words"], queryFn: fetchDrillWords })
  const [round, setRound] = useState(0)
  const [score, setScore] = useState({ correct: 0, wrong: 0 })
  const [selectedLeft, setSelectedLeft] = useState<string | null>(null)
  const [matched, setMatched] = useState<Record<string, string>>({}) // german -> english (locked)
  const [wrongFlash, setWrongFlash] = useState<string | null>(null)

  const allRounds = useMemo(() => {
    const pool = shuffle(words ?? []).filter((w) => w.english && w.german)
    const groups: { german: string; english: string }[][] = []
    for (let r = 0; r < ROUNDS; r++) {
      const slice = pool.slice(r * PER_ROUND, r * PER_ROUND + PER_ROUND)
      if (slice.length === PER_ROUND) groups.push(slice.map((w) => ({ german: w.german, english: w.english })))
    }
    return groups
  }, [words])

  // Shuffled English column for the current round (hook stays above early returns).
  const rights = useMemo(
    () => shuffle((allRounds[round] ?? []).map((p) => p.english)),
    [allRounds, round],
  )

  if (!words) return <DrillShell title="Match Pairs" onExit={onExit}><p className="py-10 text-center text-muted-foreground">Loading…</p></DrillShell>
  if (allRounds.length === 0) return <DrillShell title="Match Pairs" onExit={onExit}><p className="py-10 text-center text-muted-foreground">Finish a lesson on your path to unlock words for this drill.</p></DrillShell>

  if (round >= allRounds.length) {
    const total = score.correct + score.wrong
    const pct = total ? Math.round((score.correct / total) * 100) : 0
    return (
      <DrillShell title="Match Pairs" onExit={onExit}>
        <div className="mx-auto flex w-full max-w-md flex-col items-center gap-4 rounded-[28px] bg-surface px-6 py-10 text-center shadow-card">
          <h2 className="text-3xl font-extrabold">Drill complete</h2>
          <p className="font-grotesk text-6xl font-extrabold tracking-tight text-primary animate-in zoom-in-50 fade-in-0 duration-500">{pct}%</p>
          <p className="text-sm text-muted-foreground">{score.correct} correct · {score.wrong} wrong</p>
          <div className="mt-3 flex w-full flex-col gap-2.5">
            <Button size="lg" onClick={() => { setRound(0); setScore({ correct: 0, wrong: 0 }); setMatched({}); setSelectedLeft(null) }}>Again</Button>
            <Button size="lg" variant="secondary" onClick={onExit}>Back to drills</Button>
          </div>
        </div>
      </DrillShell>
    )
  }

  const pairs = allRounds[round]
  const correctMap = new Map(pairs.map((p) => [p.german, p.english]))
  const allMatched = Object.keys(matched).length === pairs.length

  function pickRight(english: string) {
    if (!selectedLeft) return
    if (normalize(correctMap.get(selectedLeft) ?? "") === normalize(english)) {
      setMatched((m) => ({ ...m, [selectedLeft]: english }))
      setScore((s) => ({ ...s, correct: s.correct + 1 }))
      setSelectedLeft(null)
    } else {
      setScore((s) => ({ ...s, wrong: s.wrong + 1 }))
      setWrongFlash(english)
      setTimeout(() => setWrongFlash(null), 350)
    }
  }

  function nextRound() {
    setMatched({})
    setSelectedLeft(null)
    setRound((r) => r + 1)
  }

  return (
    <DrillShell title="Match Pairs" onExit={onExit} progress={(round / allRounds.length) * 100} counter={`${round + 1} / ${allRounds.length}`}>
      <div className="mx-auto w-full max-w-2xl rounded-[28px] bg-surface p-6 shadow-card sm:p-10">
        <p className="mb-6 text-center text-lg font-semibold text-muted-foreground">Tap a German word, then its English meaning.</p>
        <div className="grid grid-cols-2 gap-4">
          <div className="flex flex-col gap-3">
            <p className="px-1 text-[13px] font-semibold uppercase tracking-[0.04em] text-muted-foreground">Deutsch</p>
            {pairs.map((p) => {
              const done = matched[p.german]
              return (
                <button
                  key={p.german}
                  disabled={!!done}
                  onClick={() => setSelectedLeft(selectedLeft === p.german ? null : p.german)}
                  className={cn(
                    "min-h-[64px] rounded-2xl border-2 px-4 py-3 text-left text-lg font-semibold transition-colors [overflow-wrap:anywhere]",
                    done
                      ? "border-[hsl(var(--success))] bg-[hsl(var(--success-bg))] text-[hsl(var(--success))]"
                      : selectedLeft === p.german
                        ? "border-[hsl(var(--choice))] bg-[hsl(var(--choice-bg))] text-foreground"
                        : "border-transparent bg-surface-2 text-foreground hover:bg-border",
                  )}
                >
                  {p.german}
                </button>
              )
            })}
          </div>
          <div className="flex flex-col gap-3">
            <p className="px-1 text-[13px] font-semibold uppercase tracking-[0.04em] text-muted-foreground">English</p>
            {rights.map((english) => {
              const done = Object.values(matched).includes(english)
              return (
                <button
                  key={english}
                  disabled={done || !selectedLeft}
                  onClick={() => pickRight(english)}
                  className={cn(
                    "min-h-[64px] rounded-2xl border-2 px-4 py-3 text-left text-lg font-semibold transition-colors [overflow-wrap:anywhere]",
                    done
                      ? "border-[hsl(var(--success))] bg-[hsl(var(--success-bg))] text-[hsl(var(--success))]"
                      : wrongFlash === english
                        ? "border-[hsl(var(--danger))] bg-[hsl(var(--danger-bg))]"
                        : "border-transparent bg-surface-2 text-foreground hover:bg-border",
                    !selectedLeft && !done && "opacity-60",
                  )}
                >
                  {english}
                </button>
              )
            })}
          </div>
        </div>
        {allMatched && (
          <div className="mt-8 text-center">
            <Button size="lg" onClick={nextRound}>{round + 1 >= allRounds.length ? "Finish" : "Next round"}</Button>
          </div>
        )}
      </div>
    </DrillShell>
  )
}
