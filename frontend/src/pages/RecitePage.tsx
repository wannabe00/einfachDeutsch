import { useRef, useState } from "react"
import { useMutation } from "@tanstack/react-query"
import { isAxiosError } from "axios"
import {
  Check,
  Loader2,
  Mic,
  RotateCcw,
  Square,
  X,
} from "lucide-react"

import { submitRecitation } from "@/api/recitation"
import type { RecitationResult } from "@/types"
import { Button } from "@/components/ui/button"

const MAX_SECONDS = 120
const recorderSupported =
  typeof navigator !== "undefined" &&
  !!navigator.mediaDevices?.getUserMedia &&
  typeof window !== "undefined" &&
  "MediaRecorder" in window

type Phase = "edit" | "study" | "record" | "done"

export default function RecitePage() {
  const [phase, setPhase] = useState<Phase>("edit")
  const [sourceText, setSourceText] = useState("")
  const [isRecording, setIsRecording] = useState(false)
  const [seconds, setSeconds] = useState(0)
  const [result, setResult] = useState<RecitationResult | null>(null)
  const [error, setError] = useState("")

  const recorderRef = useRef<MediaRecorder | null>(null)
  const chunksRef = useRef<Blob[]>([])
  const intervalRef = useRef<number | null>(null)
  const secondsRef = useRef(0)

  const submit = useMutation({
    mutationFn: (audio: Blob) => submitRecitation(sourceText, audio),
    onSuccess: (r) => {
      setResult(r)
      setPhase("done")
    },
    onError: (err) => {
      let msg = "Something went wrong. Please try again."
      if (isAxiosError(err) && err.response?.data) {
        const data = err.response.data as { detail?: string }
        if (data.detail) msg = data.detail
      }
      setError(msg)
      setPhase("study")
    },
  })

  function stopTimer() {
    if (intervalRef.current !== null) {
      window.clearInterval(intervalRef.current)
      intervalRef.current = null
    }
  }

  function stopRecording() {
    stopTimer()
    setIsRecording(false)
    const rec = recorderRef.current
    if (rec && rec.state !== "inactive") rec.stop()
  }

  async function startRecording() {
    setError("")
    try {
      const stream = await navigator.mediaDevices.getUserMedia({ audio: true })
      const rec = new MediaRecorder(stream)
      recorderRef.current = rec
      chunksRef.current = []
      rec.ondataavailable = (e) => {
        if (e.data.size > 0) chunksRef.current.push(e.data)
      }
      rec.onstop = () => {
        stream.getTracks().forEach((t) => t.stop())
        const blob = new Blob(chunksRef.current, {
          type: rec.mimeType || "audio/webm",
        })
        submit.mutate(blob)
      }
      rec.start()
      setIsRecording(true)
      secondsRef.current = 0
      setSeconds(0)
      intervalRef.current = window.setInterval(() => {
        secondsRef.current += 1
        setSeconds(secondsRef.current)
        if (secondsRef.current >= MAX_SECONDS) stopRecording()
      }, 1000)
    } catch {
      setError("Microphone access was blocked. Allow it and try again.")
    }
  }

  function reset() {
    setResult(null)
    setError("")
    setSeconds(0)
    setPhase("edit")
  }

  const mmss = (s: number) =>
    `${Math.floor(s / 60)}:${String(s % 60).padStart(2, "0")}`

  return (
    <div>
      <h1 className="text-2xl font-semibold tracking-tight">Recite</h1>
      <p className="mt-1 text-sm text-muted-foreground">
        Read a short German text, then retell it from memory in your own words.
        We transcribe and grade your retelling (your audio is discarded after).
      </p>

      {!recorderSupported && (
        <p className="mt-6 rounded-lg border border-border bg-surface p-4 text-sm text-[hsl(var(--danger))]">
          Your browser doesn't support audio recording. Try Chrome, Edge, or
          Firefox on desktop.
        </p>
      )}

      {/* Step 1 — paste the source text */}
      {phase === "edit" && (
        <div className="mt-6 flex flex-col gap-3 rounded-xl border border-border bg-surface p-5">
          <label className="text-sm font-medium">Text to retell</label>
          <textarea
            value={sourceText}
            onChange={(e) => setSourceText(e.target.value)}
            rows={6}
            placeholder="Paste or type a short German paragraph here…"
            className="w-full rounded-lg border border-border bg-background p-3 text-sm"
          />
          <Button
            className="self-start"
            disabled={!sourceText.trim() || !recorderSupported}
            onClick={() => setPhase("study")}
          >
            Study it →
          </Button>
        </div>
      )}

      {/* Step 2 — study, then record */}
      {(phase === "study" || phase === "record") && (
        <div className="mt-6 flex flex-col gap-4">
          <div className="rounded-xl border border-border bg-surface p-5">
            <p className="mb-2 text-xs font-semibold uppercase tracking-wide text-muted-foreground">
              Read this, then retell it
            </p>
            <p className="whitespace-pre-wrap text-sm leading-relaxed">
              {sourceText}
            </p>
          </div>

          {error && (
            <p className="text-sm text-[hsl(var(--danger))]">{error}</p>
          )}

          {submit.isPending ? (
            <div className="flex items-center gap-2 text-sm text-muted-foreground">
              <Loader2 className="size-4 animate-spin" /> Transcribing & grading…
            </div>
          ) : isRecording ? (
            <div className="flex items-center gap-3">
              <Button variant="destructive" onClick={stopRecording}>
                <Square className="mr-2 size-4" /> Stop
              </Button>
              <span className="text-sm tabular-nums text-muted-foreground">
                {mmss(seconds)} / {mmss(MAX_SECONDS)}
              </span>
            </div>
          ) : (
            <div className="flex items-center gap-3">
              <Button onClick={startRecording}>
                <Mic className="mr-2 size-4" /> Start recording
              </Button>
              <button
                onClick={reset}
                className="text-sm text-muted-foreground hover:text-foreground"
              >
                Edit text
              </button>
            </div>
          )}
        </div>
      )}

      {/* Step 3 — feedback card */}
      {phase === "done" && result && (
        <div className="mt-6 flex flex-col gap-4">
          <div className="rounded-xl border border-border bg-surface p-5">
            <div className="flex items-center justify-between">
              <h2 className="text-base font-semibold">Your feedback</h2>
              {result.coverage_score !== null && (
                <span className="text-2xl font-bold text-accent">
                  {result.coverage_score}%
                </span>
              )}
            </div>
            {result.summary && (
              <p className="mt-2 text-sm text-muted-foreground">{result.summary}</p>
            )}
          </div>

          {result.covered.length > 0 && (
            <FeedbackList
              title="Covered"
              items={result.covered}
              tone="success"
            />
          )}
          {result.missed.length > 0 && (
            <FeedbackList title="Missed" items={result.missed} tone="danger" />
          )}

          {result.grammar_errors.length > 0 && (
            <div className="rounded-xl border border-border bg-surface p-5">
              <h3 className="mb-3 text-sm font-semibold">Grammar</h3>
              <ul className="flex flex-col gap-2">
                {result.grammar_errors.map((g, i) => (
                  <li key={i} className="text-sm">
                    <span className="rounded bg-muted px-1.5 py-0.5 text-xs text-muted-foreground">
                      {g.type}
                    </span>{" "}
                    <span className="text-[hsl(var(--danger))] line-through">
                      {g.error}
                    </span>{" "}
                    → <span className="text-[hsl(var(--success))]">{g.correction}</span>
                  </li>
                ))}
              </ul>
            </div>
          )}

          {result.pronunciation_notes.length > 0 && (
            <FeedbackList
              title="Pronunciation to watch"
              items={result.pronunciation_notes}
              tone="muted"
            />
          )}

          <details className="rounded-xl border border-border bg-surface p-5">
            <summary className="cursor-pointer text-sm font-medium">
              What we heard (transcript)
            </summary>
            <p className="mt-2 whitespace-pre-wrap text-sm text-muted-foreground">
              {result.transcript || "—"}
            </p>
          </details>

          <Button variant="secondary" className="self-start" onClick={reset}>
            <RotateCcw className="mr-2 size-4" /> Try another
          </Button>
        </div>
      )}
    </div>
  )
}

function FeedbackList({
  title,
  items,
  tone,
}: {
  title: string
  items: string[]
  tone: "success" | "danger" | "muted"
}) {
  const Icon = tone === "success" ? Check : tone === "danger" ? X : null
  const color =
    tone === "success"
      ? "text-[hsl(var(--success))]"
      : tone === "danger"
        ? "text-[hsl(var(--danger))]"
        : "text-muted-foreground"
  return (
    <div className="rounded-xl border border-border bg-surface p-5">
      <h3 className="mb-3 text-sm font-semibold">{title}</h3>
      <ul className="flex flex-col gap-1.5">
        {items.map((it, i) => (
          <li key={i} className="flex items-start gap-2 text-sm">
            {Icon && <Icon className={`mt-0.5 size-4 shrink-0 ${color}`} />}
            <span>{it}</span>
          </li>
        ))}
      </ul>
    </div>
  )
}
