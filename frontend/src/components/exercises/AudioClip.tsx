import { useRef, useState } from "react"
import { Play } from "lucide-react"

import { cn } from "@/lib/utils"

/**
 * A Hören recording. Before the answers are checked it plays only `plays`
 * times, start to end with no pausing or seeking back, as in the exam; after
 * checking (`free`) it plays as often as you like.
 */
export function AudioClip({ audio, free }: { audio: { url: string; plays: number }; free: boolean }) {
  const ref = useRef<HTMLAudioElement>(null)
  const [used, setUsed] = useState(0)
  const [playing, setPlaying] = useState(false)
  const left = audio.plays - used
  const canPlay = !playing && (free || left > 0)

  function play() {
    const el = ref.current
    if (!el || !canPlay) return
    el.currentTime = 0
    if (!free) setUsed((u) => u + 1)
    el.play().catch(() => {
      // Blocked or missing audio: give the play back.
      if (!free) setUsed((u) => u - 1)
      setPlaying(false)
    })
  }

  return (
    <div className="flex flex-wrap items-center gap-3">
      <audio
        ref={ref}
        src={audio.url}
        preload="auto"
        onPlay={() => setPlaying(true)}
        onEnded={() => setPlaying(false)}
        onPause={() => setPlaying(false)}
      />
      <button
        type="button"
        onClick={play}
        disabled={!canPlay}
        className={cn(
          "inline-flex h-11 items-center gap-2 rounded-xl px-4 text-[15px] font-semibold transition-colors",
          canPlay ? "bg-primary text-primary-foreground hover:bg-primary/90" : "bg-surface-2 text-muted-foreground",
        )}
      >
        <Play className="size-4" aria-hidden="true" />
        {playing ? "Playing…" : used || free ? "Play again" : "Play"}
      </button>
      <span className="text-sm text-muted-foreground" aria-live="polite">
        {free
          ? "Replay as often as you like."
          : left === 0
            ? "No plays left."
            : `${left} ${left === 1 ? "play" : "plays"} left`}
      </span>
    </div>
  )
}
