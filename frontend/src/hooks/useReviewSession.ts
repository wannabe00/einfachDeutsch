import { useState } from "react"
import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query"

import { fetchDueWords, reviewWord } from "@/api/vocabulary"
import { useGuestLimit } from "@/contexts/GuestLimitContext"
import type { ReviewQuality, Word } from "@/types"

// `null` = choosing; "all" = every chapter; number = a specific chapter id.
export type Selection = number | "all" | null

/**
 * The SRS review session state machine: fetches the due queue for the chosen
 * chapter, tracks per-session stats, records ratings (skips requeue without a
 * review), and reports completion. The page just renders what this returns.
 */
export function useReviewSession() {
  const qc = useQueryClient()
  const { guard } = useGuestLimit()
  const [selection, setSelection] = useState<Selection>(null)
  const [queue, setQueue] = useState<Word[]>([])
  const [total, setTotal] = useState(0)
  const [stats, setStats] = useState({ answered: 0, correct: 0, again: 0 })
  const [done, setDone] = useState(false)

  const started = selection !== null
  const { data: dueWords, isLoading } = useQuery({
    queryKey: ["due-words", selection],
    queryFn: () => fetchDueWords(selection === "all" ? undefined : (selection as number)),
    enabled: started,
    staleTime: 0,
  })

  // Seed the working queue when a new set of due words arrives (render-time,
  // keyed on the query result's identity so it only re-seeds per session).
  const [seededFrom, setSeededFrom] = useState<Word[] | null>(null)
  if (dueWords && dueWords !== seededFrom) {
    setSeededFrom(dueWords)
    setQueue(dueWords)
    setTotal(dueWords.length)
  }

  const mutation = useMutation({
    mutationFn: ({ id, quality }: { id: number; quality: ReviewQuality }) =>
      reviewWord(id, quality),
  })

  function restart() {
    setSelection(null)
    setQueue([])
    setTotal(0)
    setStats({ answered: 0, correct: 0, again: 0 })
    setDone(false)
    qc.invalidateQueries({ queryKey: ["due-counts"] })
  }

  function finishIfEmpty(remaining: Word[]) {
    if (remaining.length === 0) {
      for (const key of ["due-words", "words", "stats", "due-counts"]) {
        qc.invalidateQueries({ queryKey: [key] })
      }
      setDone(true)
    }
  }

  function rate(quality: ReviewQuality) {
    const word = queue[0]
    if (!word) return
    if (!guard()) return // guests: blocked once the daily free cap is hit
    mutation.mutate(
      { id: word.id, quality },
      {
        onSuccess: () => {
          setStats((s) => ({
            answered: s.answered + 1,
            correct: quality >= 4 ? s.correct + 1 : s.correct,
            again: quality === 0 ? s.again + 1 : s.again,
          }))
          setQueue((q) => {
            const next = q.slice(1)
            finishIfEmpty(next)
            return next
          })
        },
      },
    )
  }

  // Skip: move the current word to the end of the queue (no review recorded).
  function skip() {
    setQueue((q) => (q.length <= 1 ? q : [...q.slice(1), q[0]]))
  }

  return {
    selection,
    setSelection,
    started,
    isLoading,
    dueWords,
    queue,
    total,
    stats,
    done,
    current: queue[0],
    rate,
    skip,
    restart,
  }
}
