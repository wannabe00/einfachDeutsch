import { useState, type FormEvent } from "react"
import { useMutation, useQueryClient } from "@tanstack/react-query"
import { createWord } from "@/api/vocabulary"
import type { Chapter } from "@/types"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"

interface WordFormProps {
  chapters: Chapter[]
  defaultChapterId?: number
  onDone?: () => void
}

export function WordForm({ chapters, defaultChapterId, onDone }: WordFormProps) {
  const qc = useQueryClient()
  const [english, setEnglish] = useState("")
  const [german, setGerman] = useState("")
  const [chapterId, setChapterId] = useState<number>(
    defaultChapterId ?? chapters[0]?.id ?? 0,
  )
  const [notes, setNotes] = useState("")

  const mutation = useMutation({
    mutationFn: createWord,
    onSuccess: () => {
      qc.invalidateQueries({ queryKey: ["words"] })
      setEnglish("")
      setGerman("")
      setNotes("")
      onDone?.()
    },
  })

  function handleSubmit(e: FormEvent) {
    e.preventDefault()
    if (!english.trim() || !german.trim() || !chapterId) return
    mutation.mutate({ english: english.trim(), german: german.trim(), chapter: chapterId, notes })
  }

  return (
    <form onSubmit={handleSubmit} className="flex flex-wrap gap-2">
      <Input
        placeholder="English"
        value={english}
        onChange={(e) => setEnglish(e.target.value)}
        className="w-36"
        required
      />
      <Input
        placeholder="German (e.g. der Hund)"
        value={german}
        onChange={(e) => setGerman(e.target.value)}
        className="w-48"
        required
      />
      <select
        value={chapterId}
        onChange={(e) => setChapterId(Number(e.target.value))}
        className="rounded-md border border-input bg-background px-3 py-2 text-sm"
      >
        {chapters.map((c) => (
          <option key={c.id} value={c.id}>
            {c.title}
          </option>
        ))}
      </select>
      <Input
        placeholder="Notes (optional)"
        value={notes}
        onChange={(e) => setNotes(e.target.value)}
        className="w-40"
      />
      <Button type="submit" disabled={mutation.isPending}>
        {mutation.isPending ? "Adding…" : "Add Word"}
      </Button>
    </form>
  )
}
