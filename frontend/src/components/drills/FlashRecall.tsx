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

  if (!rules) return <DrillShell title="Flash Recall" onExit={onExit}><p className="py-10 text-center text-muted-foreground">Loading…</p></DrillShell>
  if (rounds.length === 0) return <DrillShell title="Flash Recall" onExit={onExit}><p className="py-10 text-center text-muted-foreground">Finish a grammar lesson on your path to unlock sentences for this drill.</p></DrillShell>

  if (i >= rounds.length) {
    const pct = Math.round((score.correct / rounds.length) * 100)
    return (
      <DrillShell title="Flash Recall" onExit={onExit}>
        <div className="mx-auto flex w-full max-w-md flex-col items-center gap-4 rounded-[28px] bg-surface px-6 py-10 text-center shadow-card">
          <h2 className="text-3xl font-extrabold">Drill complete</h2>
          <p className="font-grotesk text-6xl font-extrabold tracking-tight text-primary animate-in zoom-in-50 fade-in-0 duration-500">{pct}%</p>
          <p className="text-sm text-muted-foreground">{score.correct} correct · {score.wrong} wrong</p>
          <div className="mt-3 flex w-full flex-col gap-2.5">
            <Button size="lg" onClick={() => { setI(0); setScore({ correct: 0, wrong: 0 }); setValue(""); setVerdict(null); setPhase("show") }}>Again</Button>
            <Button size="lg" variant="secondary" onClick={onExit}>Back to drills</Button>
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
      <div className="mx-auto flex min-h-[320px] w-full max-w-2xl flex-col items-center justify-center gap-6 rounded-[28px] bg-surface p-6 shadow-card sm:p-10">
        {phase === "show" ? (
          <>
            <p className="text-[13px] font-semibold uppercase tracking-[0.04em] text-primary">Memorize…</p>
            <p className="text-center font-grotesk text-4xl font-extrabold tracking-tight text-foreground sm:text-5xl">{sentence}</p>
            <div className="h-2 w-64 overflow-hidden rounded-full bg-surface-2">
              <div className="h-2 rounded-full bg-primary" style={{ width: "100%", animation: `drainbar ${FLASH_MS}ms linear forwards` }} />
            </div>
            <style>{`@keyframes drainbar{from{width:100%}to{width:0%}}`}</style>
          </>
        ) : (
          <form onSubmit={(e) => { e.preventDefault(); submit() }} className="flex w-full flex-col gap-4">
            <p className="text-center text-lg font-semibold text-muted-foreground">Type the sentence from memory.</p>
            <Input
              ref={inputRef}
              value={value}
              onChange={(e) => setValue(e.target.value)}
              disabled={!!verdict}
              autoFocus
              placeholder="Rebuild it…"
              aria-label="Type the sentence"
              className={cn(
                "h-16 text-center text-xl",
                verdict === "right" && "border-[hsl(var(--success))]",
                verdict === "wrong" && "border-[hsl(var(--danger))]",
              )}
            />
            {!verdict && <UmlautBar inputRef={inputRef} value={value} onChange={setValue} />}
            {verdict && (
              <p className={cn("text-center text-lg font-semibold", verdict === "right" ? "text-[hsl(var(--success))]" : "text-[hsl(var(--danger))]")}>
                {verdict === "right" ? "Correct" : `Answer: ${sentence}`}
              </p>
            )}
            <Button type="submit" size="lg">{verdict ? "Next" : "Check"}</Button>
          </form>
        )}
      </div>
    </DrillShell>
  )
}
