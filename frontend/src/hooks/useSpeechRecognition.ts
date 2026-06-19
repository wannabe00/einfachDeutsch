import { useCallback, useRef, useState } from "react"

/* The Web Speech API isn't in the standard TS lib, so we treat the
 * recognition object loosely. Available in Chrome/Edge as
 * (webkit)SpeechRecognition. */
type AnyRecognition = {
  lang: string
  continuous: boolean
  interimResults: boolean
  start: () => void
  stop: () => void
  onresult: ((e: SpeechResultLike) => void) | null
  onerror: ((e: { error?: string }) => void) | null
  onend: (() => void) | null
}
interface SpeechResultLike {
  resultIndex: number
  results: ArrayLike<{ 0: { transcript: string }; isFinal: boolean }>
}

function getRecognitionCtor(): (new () => AnyRecognition) | null {
  if (typeof window === "undefined") return null
  const w = window as unknown as Record<string, unknown>
  const ctor = w.SpeechRecognition || w.webkitSpeechRecognition
  return ctor ? (ctor as new () => AnyRecognition) : null
}

export function useSpeechRecognition(lang = "de-DE") {
  const supported = !!getRecognitionCtor()
  const [listening, setListening] = useState(false)
  const [transcript, setTranscript] = useState("")
  const [interim, setInterim] = useState("")
  const [error, setError] = useState("")
  const recRef = useRef<AnyRecognition | null>(null)
  const finalRef = useRef("")

  const start = useCallback(() => {
    const Ctor = getRecognitionCtor()
    if (!Ctor) {
      setError("unsupported")
      return
    }
    finalRef.current = ""
    setTranscript("")
    setInterim("")
    setError("")

    const rec = new Ctor()
    rec.lang = lang
    rec.continuous = true
    rec.interimResults = true
    rec.onresult = (e) => {
      let interimText = ""
      for (let i = e.resultIndex; i < e.results.length; i++) {
        const res = e.results[i]
        const txt = res[0].transcript
        if (res.isFinal) finalRef.current += txt + " "
        else interimText += txt
      }
      setTranscript(finalRef.current.trim())
      setInterim(interimText)
    }
    rec.onerror = (e) => {
      if (e.error && e.error !== "no-speech" && e.error !== "aborted") {
        setError(e.error)
      }
    }
    rec.onend = () => setListening(false)

    recRef.current = rec
    rec.start()
    setListening(true)
  }, [lang])

  const stop = useCallback(() => {
    recRef.current?.stop()
    setListening(false)
  }, [])

  return { supported, listening, transcript, interim, error, start, stop }
}
