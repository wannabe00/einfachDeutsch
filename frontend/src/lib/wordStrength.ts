import type { Word } from "@/types"

export type WordStatus = "new" | "learning" | "known"

/** Correct reviews in a row that make a word known (keep in sync with the
    backend's vocabulary KNOWN_AFTER). */
const KNOWN_AFTER = 2

/** Where a word stands in your flashcard reviews: never reviewed, being
    learned, or known (answered right twice in a row). A wrong answer drops a
    known word back to learning, never to new. */
export function wordStatus(word: Word): WordStatus {
  const p = word.progress
  if (!p || p.times_seen === 0) return "new"
  return p.repetitions >= KNOWN_AFTER ? "known" : "learning"
}

/** 0-4 for the strength meter: learning 1-2 by correct answers in a row,
    known 3, and 4 once the next review is three weeks or more away. */
export function wordStrength(word: Word): number {
  const status = wordStatus(word)
  if (status === "new") return 0
  const p = word.progress!
  if (status === "learning") return p.repetitions === 0 ? 1 : 2
  return p.interval >= 21 ? 4 : 3
}
