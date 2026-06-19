/** Word-level diff between a target text and what was actually said.
 * Uses an LCS alignment so reordered/missing/extra words are classified. */

export interface DiffToken {
  text: string
  status: "ok" | "missing"
}

export interface WordDiff {
  target: DiffToken[] // the target text, each word marked ok/missing
  extras: string[] // words said that aren't in the target
  accuracy: number // 0–100, matched target words / total
}

function norm(w: string): string {
  return w.toLowerCase().replace(/[.,!?;:"'»«„“()¡¿]/g, "")
}

export function diffWords(targetText: string, saidText: string): WordDiff {
  const targetWords = targetText.trim().split(/\s+/).filter(Boolean)
  const saidWords = saidText.trim().split(/\s+/).filter(Boolean)
  const T = targetWords.map(norm)
  const S = saidWords.map(norm)
  const n = T.length
  const m = S.length

  // LCS length table.
  const dp: number[][] = Array.from({ length: n + 1 }, () =>
    new Array(m + 1).fill(0),
  )
  for (let i = n - 1; i >= 0; i--) {
    for (let j = m - 1; j >= 0; j--) {
      dp[i][j] = T[i] === S[j] ? dp[i + 1][j + 1] + 1 : Math.max(dp[i + 1][j], dp[i][j + 1])
    }
  }

  // Backtrack to mark matched indices on both sides.
  const matchedTarget = new Set<number>()
  const matchedSaid = new Set<number>()
  let i = 0
  let j = 0
  while (i < n && j < m) {
    if (T[i] === S[j]) {
      matchedTarget.add(i)
      matchedSaid.add(j)
      i++
      j++
    } else if (dp[i + 1][j] >= dp[i][j + 1]) {
      i++
    } else {
      j++
    }
  }

  const target: DiffToken[] = targetWords.map((w, idx) => ({
    text: w,
    status: matchedTarget.has(idx) ? "ok" : "missing",
  }))
  const extras = saidWords.filter((_, idx) => !matchedSaid.has(idx))
  const accuracy = n ? Math.round((matchedTarget.size / n) * 100) : 0

  return { target, extras, accuracy }
}
