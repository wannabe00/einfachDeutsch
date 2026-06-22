import { useState } from "react"
import { useMutation } from "@tanstack/react-query"
import { isAxiosError } from "axios"

import { submitRecitation } from "@/api/recitation"
import type { RecitationResult } from "@/types"
import { recorderSupported, useAudioRecorder } from "@/hooks/useAudioRecorder"
import { EditStep } from "@/components/recite/EditStep"
import { StudyRecordStep } from "@/components/recite/StudyRecordStep"
import { ResultCard } from "@/components/recite/ResultCard"

const MAX_SECONDS = 120

type Phase = "edit" | "study" | "record" | "done"

export default function RecitePage() {
  const [phase, setPhase] = useState<Phase>("edit")
  const [sourceText, setSourceText] = useState("")
  const [result, setResult] = useState<RecitationResult | null>(null)
  const [error, setError] = useState("")

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

  const recorder = useAudioRecorder({
    maxSeconds: MAX_SECONDS,
    onComplete: (audio) => submit.mutate(audio),
  })

  async function handleStart() {
    setError("")
    const started = await recorder.start()
    if (!started) setError("Microphone access was blocked. Allow it and try again.")
  }

  function reset() {
    setResult(null)
    setError("")
    setPhase("edit")
  }

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

      {phase === "edit" && (
        <EditStep
          sourceText={sourceText}
          onChange={setSourceText}
          onStudy={() => setPhase("study")}
          disabled={!sourceText.trim() || !recorderSupported}
        />
      )}

      {(phase === "study" || phase === "record") && (
        <StudyRecordStep
          sourceText={sourceText}
          error={error}
          isPending={submit.isPending}
          isRecording={recorder.isRecording}
          seconds={recorder.seconds}
          maxSeconds={MAX_SECONDS}
          onStart={handleStart}
          onStop={recorder.stop}
          onEdit={reset}
        />
      )}

      {phase === "done" && result && <ResultCard result={result} onReset={reset} />}
    </div>
  )
}
