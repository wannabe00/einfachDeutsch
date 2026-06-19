import { useMemo, useState } from "react"
import { useQuery } from "@tanstack/react-query"

import { fetchWords } from "@/api/vocabulary"
import { shuffle, normalize } from "@/lib/german"
import { Button } from "@/components/ui/button"
import { cn } from "@/lib/utils"
import { DrillShell } from "./DrillShell"

const PER_ROUND = 5
const ROUNDS = 5

export function MatchPairs({ onExit }: { onExit: () => void }) {
  const { data: words } = useQuery({ queryKey: ["words", "all"], queryFn: () => fetchWords() })
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

  if (!words) return <DrillShell title="Match Pairs" onExit={onExit}><p className="text-sm text-muted-foreground">Loading…</p></DrillShell>
  if (allRounds.length === 0) return <DrillShell title="Match Pairs" onExit={onExit}><p className="text-sm text-muted-foreground">Not enough words yet.</p></DrillShell>

  if (round >= allRounds.length) {
    const total = score.correct + score.wrong
    const pct = total ? Math.round((score.correct / total) * 100) : 0
    return (
      <DrillShell title="Match Pairs" onExit={onExit}>
        <div className="flex flex-col items-center gap-6 py-16 text-center">
          <h2 className="text-2xl font-semibold">Drill complete</h2>
          <p className="text-5xl font-bold text-accent">{pct}%</p>
          <p className="text-sm text-muted-foreground">{score.correct} correct · {score.wrong} wrong</p>
          <div className="flex gap-3">
            <Button onClick={() => { setRound(0); setScore({ correct: 0, wrong: 0 }); setMatched({}); setSelectedLeft(null) }}>Again</Button>
            <Button variant="secondary" onClick={onExit}>Back to drills</Button>
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
      <div className="mx-auto max-w-lg py-6">
        <p className="mb-4 text-center text-sm text-muted-foreground">Tap a German word, then its English meaning.</p>
        <div className="grid grid-cols-2 gap-3">
          <div className="flex flex-col gap-2">
            {pairs.map((p) => {
              const done = matched[p.german]
              return (
                <button
                  key={p.german}
                  disabled={!!done}
                  onClick={() => setSelectedLeft(selectedLeft === p.german ? null : p.german)}
                  className={cn(
                    "rounded-lg border px-3 py-2 text-left text-sm transition-colors",
                    done
                      ? "border-[hsl(var(--success))] bg-[hsl(var(--success-bg))] text-[hsl(var(--success))]"
                      : selectedLeft === p.german
                        ? "border-accent bg-accent/10 text-foreground"
                        : "border-border bg-background text-foreground hover:border-accent",
                  )}
                >
                  {p.german}
                </button>
              )
            })}
          </div>
          <div className="flex flex-col gap-2">
            {rights.map((english) => {
              const done = Object.values(matched).includes(english)
              return (
                <button
                  key={english}
                  disabled={done || !selectedLeft}
                  onClick={() => pickRight(english)}
                  className={cn(
                    "rounded-lg border px-3 py-2 text-left text-sm transition-colors",
                    done
                      ? "border-[hsl(var(--success))] bg-[hsl(var(--success-bg))] text-[hsl(var(--success))]"
                      : wrongFlash === english
                        ? "border-[hsl(var(--danger))] bg-[hsl(var(--danger-bg))]"
                        : "border-border bg-background text-foreground hover:border-accent",
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
          <div className="mt-6 text-center">
            <Button onClick={nextRound}>{round + 1 >= allRounds.length ? "Finish" : "Next round"}</Button>
          </div>
        )}
      </div>
    </DrillShell>
  )
}
