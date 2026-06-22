import { Loader2, Mic, Square } from "lucide-react"

import { Button } from "@/components/ui/button"

const mmss = (s: number) => `${Math.floor(s / 60)}:${String(s % 60).padStart(2, "0")}`

/** Step 2 — show the source text and the record controls / live timer. */
export function StudyRecordStep({
  sourceText,
  error,
  isPending,
  isRecording,
  seconds,
  maxSeconds,
  onStart,
  onStop,
  onEdit,
}: {
  sourceText: string
  error: string
  isPending: boolean
  isRecording: boolean
  seconds: number
  maxSeconds: number
  onStart: () => void
  onStop: () => void
  onEdit: () => void
}) {
  return (
    <div className="mt-6 flex flex-col gap-4">
      <div className="rounded-xl border border-border bg-surface p-5">
        <p className="mb-2 text-xs font-semibold uppercase tracking-wide text-muted-foreground">
          Read this, then retell it
        </p>
        <p className="whitespace-pre-wrap text-sm leading-relaxed">{sourceText}</p>
      </div>

      {error && <p className="text-sm text-[hsl(var(--danger))]">{error}</p>}

      {isPending ? (
        <div className="flex items-center gap-2 text-sm text-muted-foreground">
          <Loader2 className="size-4 animate-spin" /> Transcribing & grading…
        </div>
      ) : isRecording ? (
        <div className="flex items-center gap-3">
          <Button variant="destructive" onClick={onStop}>
            <Square className="mr-2 size-4" /> Stop
          </Button>
          <span className="text-sm tabular-nums text-muted-foreground">
            {mmss(seconds)} / {mmss(maxSeconds)}
          </span>
        </div>
      ) : (
        <div className="flex items-center gap-3">
          <Button onClick={onStart}>
            <Mic className="mr-2 size-4" /> Start recording
          </Button>
          <button onClick={onEdit} className="text-sm text-muted-foreground hover:text-foreground">
            Edit text
          </button>
        </div>
      )}
    </div>
  )
}
