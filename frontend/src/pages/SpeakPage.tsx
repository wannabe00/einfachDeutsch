import { useEffect, useState } from "react"
import { useMutation } from "@tanstack/react-query"
import { Mic, Square, RotateCcw, Eye, EyeOff, Sparkles } from "lucide-react"

import { aiCheckAnswer } from "@/api/ai"
import { useSpeechRecognition } from "@/hooks/useSpeechRecognition"
import { diffWords } from "@/lib/worddiff"
import { Button } from "@/components/ui/button"
import { cn } from "@/lib/utils"

type Phase = "edit" | "study" | "recite" | "result"

export default function SpeakPage() {
  const [phase, setPhase] = useState<Phase>("edit")
  const [target, setTarget] = useState("")
  const [said, setSaid] = useState("")
  const { supported, listening, transcript, interim, error, start, stop } =
    useSpeechRecognition("de-DE")

  const aiNote = useMutation({
    mutationFn: () =>
      aiCheckAnswer(
        "Recite this German text from memory (compare meaning, not punctuation):",
        target,
        said,
      ),
  })

  // Start listening when we enter the recite phase.
  useEffect(() => {
    if (phase === "recite") start()
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [phase])

  function finishRecite() {
    stop()
    setSaid(transcript)
    setPhase("result")
  }

  // Ask the AI tutor once we have a result + a transcript.
  useEffect(() => {
    if (phase === "result" && said.trim()) aiNote.mutate()
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [phase])

  const diff = phase === "result" ? diffWords(target, said) : null

  return (
    <div>
      <h1 className="text-2xl font-semibold tracking-tight">Recite</h1>
      <p className="mt-1 text-sm text-muted-foreground">
        Learn a text, then say it out loud — the AI checks how well you knew it.
      </p>

      {!supported && (
        <div className="mt-6 rounded-md border border-warning/40 bg-[hsl(var(--warning-bg))] px-3 py-2 text-sm text-[hsl(var(--warning))]">
          Speech recognition needs Chrome or Edge. (Your browser doesn't support it.)
        </div>
      )}

      {/* ---- Edit: paste the text to learn ---- */}
      {phase === "edit" && (
        <div className="mt-6 flex flex-col gap-3">
          <label className="text-sm font-medium text-muted-foreground">
            Paste the German text you want to memorize
          </label>
          <textarea
            value={target}
            onChange={(e) => setTarget(e.target.value)}
            rows={6}
            placeholder={"Guten Morgen! Ich heiße Anna und ich komme aus Berlin.\nIch lerne Deutsch und ich wohne in München."}
            className="w-full rounded-lg border border-border bg-surface px-3 py-2 text-base leading-7 focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring"
          />
          <div>
            <Button disabled={!target.trim()} onClick={() => setPhase("study")}>
              Study this text
            </Button>
          </div>
        </div>
      )}

      {/* ---- Study: read it before reciting ---- */}
      {phase === "study" && (
        <div className="mt-6 flex flex-col gap-4">
          <div className="rounded-xl border border-border bg-surface p-5 text-lg leading-8 text-foreground">
            {target}
          </div>
          <div className="flex gap-2">
            <Button onClick={() => setPhase("recite")} disabled={!supported}>
              <EyeOff className="mr-2 size-4" /> Hide & recite
            </Button>
            <Button variant="secondary" onClick={() => setPhase("edit")}>
              Edit text
            </Button>
          </div>
        </div>
      )}

      {/* ---- Recite: mic on, text hidden ---- */}
      {phase === "recite" && (
        <div className="mt-6 flex flex-col items-center gap-6 py-8">
          <div
            className={cn(
              "flex size-24 items-center justify-center rounded-full border-2 transition-colors",
              listening
                ? "border-accent bg-accent/10 text-accent motion-safe:animate-pulse"
                : "border-border text-muted-foreground",
            )}
          >
            <Mic className="size-10" />
          </div>
          <p className="text-sm text-muted-foreground">
            {listening ? "Listening… speak the text now." : "Starting microphone…"}
          </p>
          <div className="min-h-[60px] w-full max-w-xl rounded-lg border border-dashed border-border bg-background p-3 text-center text-base">
            <span className="text-foreground">{transcript}</span>{" "}
            <span className="text-muted-foreground">{interim}</span>
            {!transcript && !interim && (
              <span className="text-muted-foreground">Your words appear here…</span>
            )}
          </div>
          {error && (
            <p className="text-sm text-[hsl(var(--danger))]">
              Mic error: {error}. Check microphone permission.
            </p>
          )}
          <Button onClick={finishRecite} disabled={!transcript && !interim}>
            <Square className="mr-2 size-4" /> Stop & check
          </Button>
        </div>
      )}

      {/* ---- Result: diff + AI note ---- */}
      {phase === "result" && diff && (
        <div className="mt-6 flex flex-col gap-5">
          <div className="flex items-baseline gap-3">
            <span className="text-4xl font-bold text-accent">{diff.accuracy}%</span>
            <span className="text-sm text-muted-foreground">words recalled</span>
          </div>

          <div className="rounded-xl border border-border bg-surface p-5 text-lg leading-9">
            {diff.target.map((tok, i) => (
              <span
                key={i}
                className={cn(
                  tok.status === "ok"
                    ? "text-foreground"
                    : "rounded bg-[hsl(var(--danger-bg))] px-1 text-[hsl(var(--danger))] line-through",
                )}
              >
                {tok.text}{" "}
              </span>
            ))}
          </div>

          {diff.extras.length > 0 && (
            <p className="text-sm text-muted-foreground">
              Extra / misheard words:{" "}
              <span className="text-[hsl(var(--warning))]">
                {diff.extras.join(", ")}
              </span>
            </p>
          )}

          <details className="text-sm text-muted-foreground">
            <summary className="cursor-pointer">What the mic heard</summary>
            <p className="mt-1 italic">“{said || "(nothing)"}”</p>
          </details>

          {/* AI note */}
          {aiNote.isPending && (
            <p className="flex items-center gap-1.5 text-sm text-muted-foreground">
              <Sparkles className="size-3.5 animate-pulse" /> AI tutor is reviewing…
            </p>
          )}
          {aiNote.data && (
            <div className="rounded-lg border border-accent/30 bg-accent/5 px-4 py-3">
              <p className="mb-1 flex items-center gap-1.5 text-xs font-medium text-accent">
                <Sparkles className="size-3.5" /> AI tutor
              </p>
              <p className="text-sm text-foreground">{aiNote.data}</p>
            </div>
          )}

          <div className="flex gap-2">
            <Button onClick={() => setPhase("study")}>
              <RotateCcw className="mr-2 size-4" /> Try again
            </Button>
            <Button variant="secondary" onClick={() => setPhase("study")}>
              <Eye className="mr-2 size-4" /> See the text
            </Button>
            <Button variant="ghost" onClick={() => setPhase("edit")}>
              New text
            </Button>
          </div>
        </div>
      )}
    </div>
  )
}
