import { useEffect, useMemo, useRef, useState } from "react"
import { useQuery } from "@tanstack/react-query"

import { fetchGrammarRules } from "@/api/grammar"
import { collectSentences } from "@/lib/sentences"
import { shuffle, normalize } from "@/lib/german"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { UmlautBar } from "@/components/vocabulary/UmlautBar"
import { cn } from "@/lib/utils"
import { DrillShell } from "./DrillShell"

const ROUNDS = 8
const FLASH_MS = 3000

export function FlashRecall({ onExit }: { onExit: () => void }) {
  const { data: rules } = useQuery({
    queryKey: ["grammar", "chapter", undefined, undefined],
    queryFn: () => fetchGrammarRules(),
  })
  const [i, setI] = useState(0)
  const [phase, setPhase] = useState<"show" | "input">("show")
  const [value, setValue] = useState("")
  const [verdict, setVerdict] = useState<null | "right" | "wrong">(null)
  const [score, setScore] = useState({ correct: 0, wrong: 0 })
  const inputRef = useRef<HTMLInputElement>(null)

  const rounds = useMemo(
    () => shuffle(collectSentences(rules ?? [])).slice(0, ROUNDS),
    [rules],
  )

  // Flash the sentence for a fixed time, then switch to input.
  useEffect(() => {
    if (phase !== "show" || rounds.length === 0) return
    const t = setTimeout(() => setPhase("input"), FLASH_MS)
    return () => clearTimeout(t)
  }, [phase, i, rounds.length])

  if (!rules) return <DrillShell title="Flash Recall" onExit={onExit}><p className="text-sm text-muted-foreground">Loading…</p></DrillShell>
  if (rounds.length === 0) return <DrillShell title="Flash Recall" onExit={onExit}><p className="text-sm text-muted-foreground">No sentences available yet.</p></DrillShell>

  if (i >= rounds.length) {
    const pct = Math.round((score.correct / rounds.length) * 100)
    return (
      <DrillShell title="Flash Recall" onExit={onExit}>
        <div className="flex flex-col items-center gap-6 py-16 text-center">
          <h2 className="text-2xl font-semibold">Drill complete</h2>
          <p className="text-5xl font-bold text-accent">{pct}%</p>
          <p className="text-sm text-muted-foreground">{score.correct} correct · {score.wrong} wrong</p>
          <div className="flex gap-3">
            <Button onClick={() => { setI(0); setScore({ correct: 0, wrong: 0 }); setValue(""); setVerdict(null); setPhase("show") }}>Again</Button>
            <Button variant="secondary" onClick={onExit}>Back to drills</Button>
          </div>
        </div>
      </DrillShell>
    )
  }

  const sentence = rounds[i]

  function submit() {
    if (verdict) {
      setVerdict(null)
      setValue("")
      setPhase("show")
      setI((n) => n + 1)
      return
    }
    if (!value.trim()) return
    const ok = normalize(value) === normalize(sentence)
    setVerdict(ok ? "right" : "wrong")
    setScore((s) => ({ correct: s.correct + (ok ? 1 : 0), wrong: s.wrong + (ok ? 0 : 1) }))
  }

  return (
    <DrillShell title="Flash Recall" onExit={onExit} progress={(i / rounds.length) * 100} counter={`${i + 1} / ${rounds.length}`}>
      <div className="mx-auto flex max-w-lg flex-col items-center gap-5 py-10">
        {phase === "show" ? (
          <>
            <p className="text-xs font-medium uppercase tracking-wide text-accent">Memorize…</p>
            <p className="text-center text-2xl font-semibold text-foreground">{sentence}</p>
            <div className="h-1 w-40 overflow-hidden rounded-full bg-border">
              <div className="h-1 animate-[shrink_3s_linear] rounded-full bg-accent" style={{ width: "100%", animation: `drainbar ${FLASH_MS}ms linear forwards` }} />
            </div>
            <style>{`@keyframes drainbar{from{width:100%}to{width:0%}}`}</style>
          </>
        ) : (
          <form onSubmit={(e) => { e.preventDefault(); submit() }} className="flex w-full flex-col gap-3">
            <p className="text-center text-sm text-muted-foreground">Type the sentence from memory.</p>
            <Input
              ref={inputRef}
              value={value}
              onChange={(e) => setValue(e.target.value)}
              disabled={!!verdict}
              autoFocus
              placeholder="Rebuild it…"
              aria-label="Type the sentence"
              className={cn(
                "text-center text-base",
                verdict === "right" && "border-[hsl(var(--success))]",
                verdict === "wrong" && "border-[hsl(var(--danger))]",
              )}
            />
            {!verdict && <UmlautBar inputRef={inputRef} value={value} onChange={setValue} />}
            {verdict && (
              <p className={cn("text-center text-sm font-medium", verdict === "right" ? "text-[hsl(var(--success))]" : "text-[hsl(var(--danger))]")}>
                {verdict === "right" ? "✓ Perfect recall!" : `✗ ${sentence}`}
              </p>
            )}
            <Button type="submit">{verdict ? "Next" : "Check"}</Button>
          </form>
        )}
      </div>
    </DrillShell>
  )
}
