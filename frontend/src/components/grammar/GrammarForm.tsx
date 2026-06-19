import { useState, type FormEvent } from "react"
import { useMutation, useQueryClient } from "@tanstack/react-query"

import { createGrammarRule } from "@/api/grammar"
import type { Chapter, GrammarCategory } from "@/types"
import { GRAMMAR_CATEGORIES } from "@/lib/labels"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"

interface GrammarFormProps {
  chapters: Chapter[]
  defaultChapterId?: number
  onDone?: () => void
}

export function GrammarForm({ chapters, defaultChapterId, onDone }: GrammarFormProps) {
  const qc = useQueryClient()
  const [title, setTitle] = useState("")
  const [category, setCategory] = useState<GrammarCategory>("other")
  const [chapterId, setChapterId] = useState(defaultChapterId ?? chapters[0]?.id ?? 0)
  const [content, setContent] = useState("")
  const [examples, setExamples] = useState("")

  const mutation = useMutation({
    mutationFn: createGrammarRule,
    onSuccess: () => {
      qc.invalidateQueries({ queryKey: ["grammar"] })
      setTitle("")
      setContent("")
      setExamples("")
      onDone?.()
    },
  })

  function handleSubmit(e: FormEvent) {
    e.preventDefault()
    if (!title.trim() || !content.trim() || !chapterId) return
    mutation.mutate({
      chapter: chapterId,
      title: title.trim(),
      category,
      content: content.trim(),
      example_sentences: examples.trim(),
    })
  }

  const selectClass =
    "rounded-md border border-input bg-background px-3 py-2 text-sm"
  const textareaClass =
    "w-full rounded-md border border-input bg-background px-3 py-2 text-sm focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring"

  return (
    <form onSubmit={handleSubmit} className="flex flex-col gap-3">
      <div className="flex flex-wrap gap-2">
        <Input
          placeholder="Rule title"
          value={title}
          onChange={(e) => setTitle(e.target.value)}
          className="w-64"
          required
        />
        <select
          value={category}
          onChange={(e) => setCategory(e.target.value as GrammarCategory)}
          className={selectClass}
        >
          {GRAMMAR_CATEGORIES.map((c) => (
            <option key={c.value} value={c.value}>
              {c.label}
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
      <textarea
        placeholder="Content (Markdown supported)"
        value={content}
        onChange={(e) => setContent(e.target.value)}
        rows={4}
        className={textareaClass}
        required
      />
      <textarea
        placeholder="Example sentences (one per line)"
        value={examples}
        onChange={(e) => setExamples(e.target.value)}
        rows={2}
        className={textareaClass}
      />
      <div>
        <Button type="submit" disabled={mutation.isPending}>
          {mutation.isPending ? "Saving…" : "Add Grammar Rule"}
        </Button>
      </div>
    </form>
  )
}
