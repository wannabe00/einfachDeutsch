import type { Word } from "@/types"

export type WordStatus = "new" | "learning" | "known"

/** Where a word stands in your flashcard reviews (SM-2): never reviewed, being
    learned, or known (next review more than three weeks away). */
export function wordStatus(word: Word): WordStatus {
  const p = word.progress
  if (!p || p.repetitions === 0) return "new"
  return p.interval > 21 ? "known" : "learning"
}

/** 0-4 for the strength meter, from the SM-2 interval. */
export function wordStrength(word: Word): number {
  const status = wordStatus(word)
  if (status === "new") return 0
  if (status === "known") return 4
  const interval = word.progress!.interval
  return interval < 3 ? 1 : interval < 8 ? 2 : 3
}
