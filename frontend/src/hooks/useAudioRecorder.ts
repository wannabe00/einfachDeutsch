import { useEffect, useRef, useState } from "react"

/** Whether this browser can record audio (used to gate the Recite feature). */
export const recorderSupported =
  typeof navigator !== "undefined" &&
  !!navigator.mediaDevices?.getUserMedia &&
  typeof window !== "undefined" &&
  "MediaRecorder" in window

/**
 * Wraps MediaRecorder + a 1s tick that auto-stops at `maxSeconds`. Calls
 * `onComplete` with the recorded blob when recording stops, then releases the
 * mic. `start()` resolves to `false` if mic permission was denied.
 */
export function useAudioRecorder({
  maxSeconds,
  onComplete,
}: {
  maxSeconds: number
  onComplete: (audio: Blob) => void
}) {
  const [isRecording, setIsRecording] = useState(false)
  const [seconds, setSeconds] = useState(0)

  const recorderRef = useRef<MediaRecorder | null>(null)
  const chunksRef = useRef<Blob[]>([])
  const intervalRef = useRef<number | null>(null)
  const secondsRef = useRef(0)
  // Always call the latest callback without re-creating the recorder.
  const onCompleteRef = useRef(onComplete)
  useEffect(() => {
    onCompleteRef.current = onComplete
  }, [onComplete])

  function stopTimer() {
    if (intervalRef.current !== null) {
      window.clearInterval(intervalRef.current)
      intervalRef.current = null
    }
  }

  function stop() {
    stopTimer()
    setIsRecording(false)
    const rec = recorderRef.current
    if (rec && rec.state !== "inactive") rec.stop()
  }

  async function start(): Promise<boolean> {
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
        const blob = new Blob(chunksRef.current, { type: rec.mimeType || "audio/webm" })
        onCompleteRef.current(blob)
      }
      rec.start()
      setIsRecording(true)
      secondsRef.current = 0
      setSeconds(0)
      intervalRef.current = window.setInterval(() => {
        secondsRef.current += 1
        setSeconds(secondsRef.current)
        if (secondsRef.current >= maxSeconds) stop()
      }, 1000)
      return true
    } catch {
      return false
    }
  }

  // Clear the timer if the component unmounts mid-recording.
  useEffect(() => stopTimer, [])

  return { isRecording, seconds, start, stop }
}
