import { useMemo, useState } from "react"
import { useQuery } from "@tanstack/react-query"

import { fetchWords } from "@/api/vocabulary"
import { splitArticle, shuffle } from "@/lib/german"
import { WORD_THEMES } from "@/lib/wordThemes"
import { Button } from "@/components/ui/button"
import { cn } from "@/lib/utils"
import { DrillShell } from "./DrillShell"

const ROUNDS = 10

const THEME_OF = new Map(WORD_THEMES.flatMap((t) => t.words.map((w) => [w, t] as const)))

interface Card {
  id: number
  noun: string // shown without its article, so the article gives nothing away
  english: string
  theme: string
  pos: string
}

interface Round {
  words: Card[]
  odd: number // word id
  why: string
}

/** One round: three learned words from one theme plus one from another theme
    of the same part of speech (a verb among nouns would be too easy). */
function makeRound(cards: Card[], used: Set<number>): Round | null {
  const free = shuffle(cards.filter((c) => !used.has(c.id)))
  const byTheme = new Map<string, Card[]>()
  // Keyed by part of speech too: "weather" is a noun theme and a verb theme.
  for (const c of free) byTheme.set(`${c.pos} ${c.theme}`, [...(byTheme.get(`${c.pos} ${c.theme}`) ?? []), c])
  for (const [, members] of shuffle([...byTheme])) {
    const { pos, theme } = members[0]
    const odd = free.find((c) => c.pos === pos && c.theme !== theme)
    if (members.length < 3 || !odd) continue
    return {
      words: shuffle([...members.slice(0, 3), odd]),
      odd: odd.id,
      why: `${members.slice(0, 3).map((c) => c.noun).join(", ")}: ${theme}. ${odd.noun}: ${odd.theme}.`,
    }
  }
  return null
}

export function OddOneOut({ onExit }: { onExit: () => void }) {
  // All learned words, not the 60-word drill sample: only some of them are themed nouns.
  const { data: words } = useQuery({ queryKey: ["words", "all"], queryFn: () => fetchWords() })
  const [i, setI] = useState(0)
  const [score, setScore] = useState({ correct: 0, wrong: 0 })
  const [picked, setPicked] = useState<number | null>(null)
  const [seed, setSeed] = useState(0)

  const rounds = useMemo(() => {
    void seed // a new seed deals new rounds on "Again"
    const cards = (words ?? []).flatMap((w) => {
      const noun = splitArticle(w.german).noun
      const theme = THEME_OF.get(noun)
      return theme ? [{ id: w.id, noun, english: w.english, theme: theme.label, pos: theme.pos }] : []
    })
    let used = new Set<number>()
    const out: Round[] = []
    while (out.length < ROUNDS) {
      // Fresh words first; once they run out, words may come back.
      let r = makeRound(cards, used)
      if (!r && used.size) {
        used = new Set()
        r = makeRound(cards, used)
      }
      if (!r) break
      r.words.forEach((w) => used.add(w.id))
      out.push(r)
    }
    return out
  }, [words, seed])

  if (!words) return <DrillShell title="Odd One Out" onExit={onExit}><p className="py-10 text-center text-muted-foreground">Loading…</p></DrillShell>
  if (rounds.length === 0) return <DrillShell title="Odd One Out" onExit={onExit}><p className="py-10 text-center text-muted-foreground">Finish a few more lessons on your path to unlock this drill.</p></DrillShell>

  if (i >= rounds.length) {
    const pct = Math.round((score.correct / rounds.length) * 100)
    return (
      <DrillShell title="Odd One Out" onExit={onExit}>
        <div className="mx-auto flex w-full max-w-md flex-col items-center gap-4 rounded-[28px] bg-surface px-6 py-10 text-center shadow-card">
          <h2 className="text-3xl font-extrabold">Drill complete</h2>
          <p className="font-grotesk text-6xl font-extrabold tracking-tight text-primary animate-in zoom-in-50 fade-in-0 duration-500">{pct}%</p>
          <p className="text-sm text-muted-foreground">{score.correct} correct · {score.wrong} wrong</p>
          <div className="mt-3 flex w-full flex-col gap-2.5">
            <Button size="lg" onClick={() => { setI(0); setScore({ correct: 0, wrong: 0 }); setPicked(null); setSeed((s) => s + 1) }}>Again</Button>
            <Button size="lg" variant="secondary" onClick={onExit}>Back to drills</Button>
          </div>
        </div>
      </DrillShell>
    )
  }

  const current = rounds[i]

  function pick(id: number) {
    if (picked !== null) return
    setPicked(id)
    const ok = id === current.odd
    setScore((s) => ({ correct: s.correct + (ok ? 1 : 0), wrong: s.wrong + (ok ? 0 : 1) }))
  }

  return (
    <DrillShell title="Odd One Out" onExit={onExit} progress={(i / rounds.length) * 100} counter={`${i + 1} / ${rounds.length}`}>
      <div className="mx-auto flex max-w-md flex-col gap-5 py-6">
        <p className="text-center text-sm text-muted-foreground">Which word doesn't belong?</p>
        <div className="grid grid-cols-2 gap-3">
          {current.words.map((w) => (
            <button
              key={w.id}
              disabled={picked !== null}
              onClick={() => pick(w.id)}
              className={cn(
                "min-h-[72px] rounded-2xl border-2 px-3.5 py-3 text-center text-[17px] font-semibold transition-colors [overflow-wrap:anywhere]",
                picked === null
                  ? "border-transparent bg-surface text-foreground shadow-card hover:bg-surface-2"
                  : w.id === current.odd
                    ? "border-[hsl(var(--success))] bg-[hsl(var(--success-bg))] text-[hsl(var(--success))]"
                    : w.id === picked
                      ? "border-[hsl(var(--danger))] bg-[hsl(var(--danger-bg))] text-[hsl(var(--danger))]"
                      : "border-transparent bg-surface text-muted-foreground",
              )}
            >
              {w.noun}
              {picked !== null && <span className="mt-1 block text-xs font-normal text-muted-foreground">{w.english}</span>}
            </button>
          ))}
        </div>
        {picked !== null && (
          <>
            <p className={cn("text-center text-base font-semibold", picked === current.odd ? "text-[hsl(var(--success))]" : "text-[hsl(var(--danger))]")}>
              {picked === current.odd ? "Correct" : "Not quite"}
            </p>
            <p className="text-center text-muted-foreground">{current.why}</p>
            <Button size="lg" onClick={() => { setPicked(null); setI((n) => n + 1) }}>Next</Button>
          </>
        )}
      </div>
    </DrillShell>
  )
}
