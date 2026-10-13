import { Loader2, Mic, Pencil, Square } from "lucide-react"

const mmss = (s: number) => `${Math.floor(s / 60)}:${String(s % 60).padStart(2, "0")}`

/** Step 2: the source text, a big record button and a live timer. */
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
    <div className="flex flex-col gap-5">
      <div className="rounded-[24px] bg-surface p-6 shadow-card sm:p-7">
        <div className="mb-3 flex items-center justify-between gap-3">
          <p className="text-[13px] font-semibold uppercase tracking-[0.04em] text-muted-foreground">
            Read this, then retell it
          </p>
          {!isRecording && !isPending && (
            <button
              onClick={onEdit}
              className="inline-flex min-h-[36px] items-center gap-1.5 rounded-full bg-surface-2 px-3 text-sm font-medium transition-colors hover:bg-border"
            >
              <Pencil className="size-3.5" aria-hidden="true" /> Edit text
            </button>
          )}
        </div>
        <p className="whitespace-pre-wrap text-lg leading-8">{sourceText}</p>
      </div>

      {error && (
        <p className="rounded-2xl bg-danger-bg p-4 text-sm font-medium text-danger" role="alert">
          {error}
        </p>
      )}

      <div className="flex flex-col items-center gap-4 rounded-[24px] bg-surface px-6 py-8 text-center shadow-card">
        {isPending ? (
          <>
            <span className="flex size-20 items-center justify-center rounded-full bg-surface-2">
              <Loader2 className="size-8 animate-spin text-muted-foreground" aria-hidden="true" />
            </span>
            <p className="font-semibold">Transcribing and grading…</p>
          </>
        ) : isRecording ? (
          <>
            <button
              onClick={onStop}
              aria-label="Stop recording"
              className="relative flex size-20 items-center justify-center rounded-full bg-primary text-primary-foreground transition active:scale-95"
            >
              <span className="absolute inset-0 animate-ping rounded-full bg-primary/40 motion-reduce:hidden" aria-hidden="true" />
              <Square className="relative size-7 fill-current" aria-hidden="true" />
            </button>
            <p className="font-semibold">Recording. Tap to stop.</p>
            <div className="w-full max-w-xs">
              <div className="h-2 overflow-hidden rounded-full bg-surface-2">
                <div
                  className="h-full rounded-full bg-primary transition-[width] duration-1000 ease-linear"
                  style={{ width: `${(seconds / maxSeconds) * 100}%` }}
                />
              </div>
              <p className="mt-2 text-sm tabular-nums text-muted-foreground">
                {mmss(seconds)} / {mmss(maxSeconds)}
              </p>
            </div>
          </>
        ) : (
          <>
            <button
              onClick={onStart}
              aria-label="Start recording"
              className="flex size-20 items-center justify-center rounded-full bg-primary text-primary-foreground shadow-lift transition hover:brightness-110 active:scale-95"
            >
              <Mic className="size-8" aria-hidden="true" />
            </button>
            <div>
              <p className="font-semibold">Ready when you are</p>
              <p className="text-sm text-muted-foreground">
                Retell it in your own words, up to {Math.round(maxSeconds / 60)} minutes.
              </p>
            </div>
          </>
        )}
      </div>
    </div>
  )
}
