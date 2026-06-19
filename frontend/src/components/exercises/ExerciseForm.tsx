import { useState, type FormEvent } from "react"
import { useMutation, useQueryClient } from "@tanstack/react-query"

import { createExercise } from "@/api/exercises"
import type { Chapter, ExerciseType } from "@/types"
import { EXERCISE_TYPES } from "@/lib/labels"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"

interface ExerciseFormProps {
  chapters: Chapter[]
  defaultChapterId?: number
  onDone?: () => void
}

export function ExerciseForm({ chapters, defaultChapterId, onDone }: ExerciseFormProps) {
  const qc = useQueryClient()
  const [chapterId, setChapterId] = useState(defaultChapterId ?? chapters[0]?.id ?? 0)
  const [type, setType] = useState<ExerciseType>("translation")
  const [prompt, setPrompt] = useState("")
  const [answer, setAnswer] = useState("")
  const [hint, setHint] = useState("")
  const [explanation, setExplanation] = useState("")

  const mutation = useMutation({
    mutationFn: createExercise,
    onSuccess: () => {
      qc.invalidateQueries({ queryKey: ["exercises"] })
      setPrompt("")
      setAnswer("")
      setHint("")
      setExplanation("")
      onDone?.()
    },
  })

  function handleSubmit(e: FormEvent) {
    e.preventDefault()
    if (!prompt.trim() || !answer.trim() || !chapterId) return
    mutation.mutate({
      chapter: chapterId,
      exercise_type: type,
      prompt: prompt.trim(),
      correct_answer: answer.trim(),
      hint: hint.trim(),
      explanation: explanation.trim(),
    })
  }

  const selectClass =
    "rounded-md border border-input bg-background px-3 py-2 text-sm"

  return (
    <form onSubmit={handleSubmit} className="flex flex-col gap-3">
      <div className="flex flex-wrap gap-2">
        <select
          value={type}
          onChange={(e) => setType(e.target.value as ExerciseType)}
          className={selectClass}
        >
          {EXERCISE_TYPES.map((t) => (
            <option key={t.value} value={t.value}>
              {t.label}
            </option>
          ))}
        </select>
        <select
          value={chapterId}
          onChange={(e) => setChapterId(Number(e.target.value))}
          className={selectClass}
        >
          {chapters.map((c) => (
            <option key={c.id} value={c.id}>
              {c.title}
            </option>
          ))}
        </select>
      </div>
      <Input
        placeholder="Prompt (the question)"
        value={prompt}
        onChange={(e) => setPrompt(e.target.value)}
        required
      />
      <Input
        placeholder="Correct answer"
        value={answer}
        onChange={(e) => setAnswer(e.target.value)}
        required
      />
      <div className="flex flex-wrap gap-2">
        <Input
          placeholder="Hint (optional)"
          value={hint}
          onChange={(e) => setHint(e.target.value)}
          className="w-60"
        />
        <Input
          placeholder="Explanation (optional)"
          value={explanation}
          onChange={(e) => setExplanation(e.target.value)}
          className="w-60"
        />
      </div>
      <div>
        <Button type="submit" disabled={mutation.isPending}>
          {mutation.isPending ? "Saving…" : "Add Exercise"}
        </Button>
      </div>
    </form>
  )
}
