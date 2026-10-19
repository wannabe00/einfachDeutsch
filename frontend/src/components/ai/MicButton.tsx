import { useRef, useState } from "react"
import { useMutation } from "@tanstack/react-query"
import { Loader2, Mic, Square } from "lucide-react"

import { transcribe } from "@/api/ai"
import { errorText } from "@/lib/apiError"
import { cn } from "@/lib/utils"

/*
 * Speech to text for the chat box: tap to record, tap again to stop; the
 * recording goes to Django (Gemini transcribes it, German or English) and the
 * text lands in the input to check before sending.
 */

const MAX_SECONDS = 60 // the backend takes about a minute

const micSupported =
  typeof window !== "undefined" && "MediaRecorder" in window && !!navigator.mediaDevices?.getUserMedia

export function MicButton({ onText }: { onText: (text: string) => void }) {
  const recorder = useRef<MediaRecorder | null>(null)
  const [recording, setRecording] = useState(false)
  const [problem, setProblem] = useState("")
  const toText = useMutation({
    mutationFn: transcribe,
    onSuccess: (text) => {
      if (text.trim()) onText(text.trim())
      else setProblem("Didn't catch that. Please try again.")
    },
    onError: (err) => setProblem(errorText(err)),
  })

  async function start() {
    setProblem("")
    let stream: MediaStream
    try {
      stream = await navigator.mediaDevices.getUserMedia({ audio: true })
    } catch {
      setProblem("Allow the microphone in your browser to talk.")
      return
    }
    const rec = new MediaRecorder(stream)
    const chunks: Blob[] = []
    rec.ondataavailable = (e) => chunks.push(e.data)
    rec.onstop = () => {
      stream.getTracks().forEach((t) => t.stop())
      setRecording(false)
      const audio = new Blob(chunks, { type: rec.mimeType || "audio/webm" })
      if (audio.size) toText.mutate(audio)
    }
    rec.start()
    recorder.current = rec
    setRecording(true)
    window.setTimeout(() => rec.state === "recording" && rec.stop(), MAX_SECONDS * 1000)
  }

  if (!micSupported) return null
  const label = recording ? "Stop recording" : toText.isPending ? "Transcribing…" : "Speak"
  return (
    <div className="relative shrink-0">
      <button
        type="button"
        onClick={() => (recording ? recorder.current?.stop() : void start())}
        disabled={toText.isPending}
        aria-label={label}
        title={label}
        className={cn(
          "flex size-10 items-center justify-center rounded-full text-muted-foreground transition-colors hover:bg-surface-2 hover:text-foreground disabled:opacity-60 [&_svg]:size-5",
          recording && "bg-primary text-primary-foreground animate-pulse hover:bg-primary hover:text-primary-foreground",
        )}
      >
        {recording ? <Square /> : toText.isPending ? <Loader2 className="animate-spin" /> : <Mic />}
      </button>
      {problem && (
        <p role="status" className="absolute bottom-full right-0 mb-2 w-max max-w-64 rounded-lg bg-surface px-3 py-1.5 text-xs text-muted-foreground shadow-card">
          {problem}
        </p>
      )}
    </div>
  )
}
