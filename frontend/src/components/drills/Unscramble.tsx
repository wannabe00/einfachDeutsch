import { useMemo, useRef, useState } from "react"
import { useQuery } from "@tanstack/react-query"

import { fetchWords } from "@/api/vocabulary"
import { splitArticle, normalize, shuffle } from "@/lib/german"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { UmlautBar } from "@/components/vocabulary/UmlautBar"
import { ArticleBadge } from "@/components/vocabulary/ArticleBadge"
import { cn } from "@/lib/utils"
import { DrillShell } from "./DrillShell"

const ROUNDS = 10

function scrambleLetters(word: string): string {
  if (word.length < 2) return word
  let out = word
  let tries = 0
  while (out === word && tries < 10) {
    out = shuffle(word.split("")).join("")
    tries++
  }
  return out
}

export function Unscramble({ onExit }: { onExit: () => void }) {
  const { data: words } = useQuery({ queryKey: ["words", "all"], queryFn: () => fetchWords() })
  const [i, setI] = useState(0)
  const [score, setScore] = useState({ correct: 0, wrong: 0 })
  const [value, setValue] = useState("")
  const [verdict, setVerdict] = useState<null | "right" | "wrong">(null)
  const inputRef = useRef<HTMLInputElement>(null)

  const pool = useMemo(() => {
    const items = (words ?? [])
      .map((w) => {
        const s = splitArticle(w.german)
        return { ...s, english: w.english }
      })
      .filter((x) => x.noun.length >= 3)
    return shuffle(items)
      .slice(0, ROUNDS)
      .map((x) => ({ ...x, scrambled: scrambleLetters(x.noun) }))
  }, [words])

  if (!words) return <DrillShell title="Unscramble" onExit={onExit}><p className="text-sm text-muted-foreground">Loading…</p></DrillShell>
  if (pool.length === 0) return <DrillShell title="Unscramble" onExit={onExit}><p className="text-sm text-muted-foreground">No words yet.</p></DrillShell>

  if (i >= pool.length) {
    const pct = Math.round((score.correct / pool.length) * 100)
    return (
      <DrillShell title="Unscramble" onExit={onExit}>
        <div className="flex flex-col items-center gap-6 py-16 text-center">
          <h2 className="text-2xl font-semibold">Drill complete</h2>
          <p className="text-5xl font-bold text-accent">{pct}%</p>
          <p className="text-sm text-muted-foreground">{score.correct} correct · {score.wrong} wrong</p>
          <div className="flex gap-3">
            <Button onClick={() => { setI(0); setScore({ correct: 0, wrong: 0 }); setValue(""); setVerdict(null) }}>Again</Button>
            <Button variant="secondary" onClick={onExit}>Back to drills</Button>
          </div>
        </div>
      </DrillShell>
    )
  }

  const current = pool[i]

  function submit() {
    if (verdict) { setVerdict(null); setValue(""); setI((n) => n + 1); return }
    if (!value.trim()) return
    const ok = normalize(value) === normalize(current.noun)
    setVerdict(ok ? "right" : "wrong")
    setScore((s) => ({ correct: s.correct + (ok ? 1 : 0), wrong: s.wrong + (ok ? 0 : 1) }))
  }

  return (
    <DrillShell title="Unscramble" onExit={onExit} progress={(i / pool.length) * 100} counter={`${i + 1} / ${pool.length}`}>
      <div className="mx-auto flex max-w-md flex-col gap-5 py-6">
        <div className="text-center">
          <div className="flex items-center justify-center gap-2">
            {current.article && <ArticleBadge german={`${current.article} x`} />}
            <p className="font-mono text-3xl font-bold uppercase tracking-[0.3em] text-foreground">
              {current.scrambled}
            </p>
          </div>
          <p className="mt-2 text-sm text-muted-foreground">{current.english}</p>
        </div>
        <form onSubmit={(e) => { e.preventDefault(); submit() }} className="flex flex-col gap-3">
          <Input
            ref={inputRef}
            value={value}
            onChange={(e) => setValue(e.target.value)}
            disabled={!!verdict}
            placeholder="Unscramble the word…"
            aria-label="Unscramble the word"
            autoFocus
            className={cn(
              "text-center text-base",
              verdict === "right" && "border-[hsl(var(--success))]",
              verdict === "wrong" && "border-[hsl(var(--danger))]",
            )}
          />
          {!verdict && <UmlautBar inputRef={inputRef} value={value} onChange={setValue} />}
          {verdict && (
            <p className={cn("text-center text-sm font-medium", verdict === "right" ? "text-[hsl(var(--success))]" : "text-[hsl(var(--danger))]")}>
              {verdict === "right" ? "✓ Solved!" : `✗ ${current.noun}`}
            </p>
          )}
          <Button type="submit">{verdict ? "Next" : "Check"}</Button>
        </form>
      </div>
    </DrillShell>
  )
}
