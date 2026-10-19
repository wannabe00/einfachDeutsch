import { useMemo, useRef, useState } from "react"
import { useQuery } from "@tanstack/react-query"

import { fetchDrillWords } from "@/api/vocabulary"
import { normalize, shuffle } from "@/lib/german"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { UmlautBar } from "@/components/vocabulary/UmlautBar"
import { cn } from "@/lib/utils"
import { DrillShell } from "./DrillShell"

const ROUNDS = 10

export function BlindForge({ onExit }: { onExit: () => void }) {
  const { data: words } = useQuery({ queryKey: ["drill-words"], queryFn: fetchDrillWords })
  const [i, setI] = useState(0)
  const [score, setScore] = useState({ correct: 0, wrong: 0 })
  const [value, setValue] = useState("")
  const [verdict, setVerdict] = useState<null | "right" | "wrong">(null)
  const inputRef = useRef<HTMLInputElement>(null)

  const pool = useMemo(() => shuffle(words ?? []).slice(0, ROUNDS), [words])

  if (!words) return <DrillShell title="Blind Forge" onExit={onExit}><p className="py-10 text-center text-muted-foreground">Loading…</p></DrillShell>
  if (pool.length === 0) return <DrillShell title="Blind Forge" onExit={onExit}><p className="py-10 text-center text-muted-foreground">Finish a lesson on your path to unlock words for this drill.</p></DrillShell>

  if (i >= pool.length) {
    const pct = Math.round((score.correct / pool.length) * 100)
    return (
      <DrillShell title="Blind Forge" onExit={onExit}>
        <div className="mx-auto flex w-full max-w-md flex-col items-center gap-4 rounded-[28px] bg-surface px-6 py-10 text-center shadow-card">
          <h2 className="text-3xl font-extrabold">Drill complete</h2>
          <p className="font-grotesk text-6xl font-extrabold tracking-tight text-primary animate-in zoom-in-50 fade-in-0 duration-500">{pct}%</p>
          <p className="text-sm text-muted-foreground">{score.correct} correct · {score.wrong} wrong</p>
          <div className="mt-3 flex w-full flex-col gap-2.5">
            <Button size="lg" onClick={() => { setI(0); setScore({ correct: 0, wrong: 0 }); setValue(""); setVerdict(null) }}>Again</Button>
            <Button size="lg" variant="secondary" onClick={onExit}>Back to drills</Button>
          </div>
        </div>
      </DrillShell>
    )
  }

  const current = pool[i]

  function submit() {
    if (verdict) { setVerdict(null); setValue(""); setI((n) => n + 1); return }
    if (!value.trim()) return
    const ok = normalize(value) === normalize(current.german)
    setVerdict(ok ? "right" : "wrong")
    setScore((s) => ({ correct: s.correct + (ok ? 1 : 0), wrong: s.wrong + (ok ? 0 : 1) }))
  }

  return (
    <DrillShell title="Blind Forge" onExit={onExit} progress={(i / pool.length) * 100} counter={`${i + 1} / ${pool.length}`}>
      <div className="mx-auto flex w-full max-w-2xl flex-col gap-6 rounded-[28px] bg-surface p-6 shadow-card sm:p-10">
        <div className="flex flex-col items-center gap-2 py-4 text-center">
          <p className="text-[13px] font-semibold uppercase tracking-[0.04em] text-muted-foreground">Type the German for</p>
          <p className="font-grotesk text-4xl font-extrabold tracking-tight text-foreground sm:text-5xl">{current.english}</p>
        </div>
        <form onSubmit={(e) => { e.preventDefault(); submit() }} className="flex flex-col gap-4">
          <Input
            ref={inputRef}
            value={value}
            onChange={(e) => setValue(e.target.value)}
            disabled={!!verdict}
            placeholder="Type the German…"
            aria-label="Type the German"
            autoFocus
            className={cn(
              "h-16 text-center text-xl",
              verdict === "right" && "border-[hsl(var(--success))]",
              verdict === "wrong" && "border-[hsl(var(--danger))]",
            )}
          />
          {!verdict && <UmlautBar inputRef={inputRef} value={value} onChange={setValue} />}
          {verdict && (
            <p className={cn("text-center text-lg font-semibold", verdict === "right" ? "text-[hsl(var(--success))]" : "text-[hsl(var(--danger))]")}>
              {verdict === "right" ? "Correct" : `Answer: ${current.german}`}
            </p>
          )}
          <Button type="submit" size="lg">{verdict ? "Next" : "Forge"}</Button>
        </form>
      </div>
    </DrillShell>
  )
}
