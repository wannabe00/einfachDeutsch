import { useMemo, useRef, useState } from "react"
import { useQuery } from "@tanstack/react-query"

import { fetchWords } from "@/api/vocabulary"
import { normalize, shuffle } from "@/lib/german"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { UmlautBar } from "@/components/vocabulary/UmlautBar"
import { cn } from "@/lib/utils"
import { DrillShell } from "./DrillShell"

const ROUNDS = 10

export function BlindForge({ onExit }: { onExit: () => void }) {
  const { data: words } = useQuery({ queryKey: ["words", "all"], queryFn: () => fetchWords() })
  const [i, setI] = useState(0)
  const [score, setScore] = useState({ correct: 0, wrong: 0 })
  const [value, setValue] = useState("")
  const [verdict, setVerdict] = useState<null | "right" | "wrong">(null)
  const inputRef = useRef<HTMLInputElement>(null)

  const pool = useMemo(() => shuffle(words ?? []).slice(0, ROUNDS), [words])

  if (!words) return <DrillShell title="Blind Forge" onExit={onExit}><p className="text-sm text-muted-foreground">Loading…</p></DrillShell>
  if (pool.length === 0) return <DrillShell title="Blind Forge" onExit={onExit}><p className="text-sm text-muted-foreground">No words yet.</p></DrillShell>

  if (i >= pool.length) {
    const pct = Math.round((score.correct / pool.length) * 100)
    return (
      <DrillShell title="Blind Forge" onExit={onExit}>
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
    const ok = normalize(value) === normalize(current.german)
    setVerdict(ok ? "right" : "wrong")
    setScore((s) => ({ correct: s.correct + (ok ? 1 : 0), wrong: s.wrong + (ok ? 0 : 1) }))
  }

  return (
    <DrillShell title="Blind Forge" onExit={onExit} progress={(i / pool.length) * 100} counter={`${i + 1} / ${pool.length}`}>
      <div className="mx-auto flex max-w-md flex-col gap-4 py-6">
        <p className="text-center text-2xl font-semibold text-foreground">{current.english}</p>
        <form onSubmit={(e) => { e.preventDefault(); submit() }} className="flex flex-col gap-3">
          <Input
            ref={inputRef}
            value={value}
            onChange={(e) => setValue(e.target.value)}
            disabled={!!verdict}
            placeholder="Type the German…"
            aria-label="Type the German"
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
              {verdict === "right" ? "✓ Forged!" : `✗ ${current.german}`}
            </p>
          )}
          <Button type="submit">{verdict ? "Next" : "Forge"}</Button>
        </form>
      </div>
    </DrillShell>
  )
}
