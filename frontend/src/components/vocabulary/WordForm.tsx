import { useState, type FormEvent } from "react"
import { useMutation, useQueryClient } from "@tanstack/react-query"
import { saveWord } from "@/api/vocabulary"
import { errorText } from "@/lib/apiError"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"

/** Add a word to the learner's own words (shared words are edited by staff). */
export function WordForm({ onDone }: { onDone?: () => void }) {
  const qc = useQueryClient()
  const [english, setEnglish] = useState("")
  const [german, setGerman] = useState("")
  const [notes, setNotes] = useState("")

  const mutation = useMutation({
    mutationFn: saveWord,
    onSuccess: () => {
      qc.invalidateQueries({ queryKey: ["saved-words"] })
      setEnglish("")
      setGerman("")
      setNotes("")
      onDone?.()
    },
  })

  function handleSubmit(e: FormEvent) {
    e.preventDefault()
    if (!german.trim()) return
    mutation.mutate({ german: german.trim(), english: english.trim(), notes: notes.trim() })
  }

  return (
    <form onSubmit={handleSubmit} className="flex flex-wrap items-center gap-2">
      <Input
        placeholder="German (e.g. der Hund)"
        aria-label="German"
        value={german}
        onChange={(e) => setGerman(e.target.value)}
        className="w-48"
        required
      />
      <Input placeholder="English" aria-label="English" value={english} onChange={(e) => setEnglish(e.target.value)} className="w-40" />
      <Input
        placeholder="Notes (optional)"
        aria-label="Notes"
        value={notes}
        onChange={(e) => setNotes(e.target.value)}
        className="w-40"
      />
      <Button type="submit" disabled={mutation.isPending}>
        {mutation.isPending ? "Adding…" : "Add word"}
      </Button>
      {mutation.isError && <p className="w-full text-sm text-danger">{errorText(mutation.error)}</p>}
    </form>
  )
}
