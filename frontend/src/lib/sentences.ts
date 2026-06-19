import type { GrammarRule } from "@/types"

/** Collect usable example sentences from grammar rules (one per line). */
export function collectSentences(rules: GrammarRule[]): string[] {
  const out: string[] = []
  for (const r of rules) {
    for (const line of (r.example_sentences ?? "").split("\n")) {
      const s = line.trim()
      // Keep real sentences: a few words, ending punctuation optional.
      if (s && s.split(/\s+/).length >= 3 && s.split(/\s+/).length <= 12) {
        out.push(s)
      }
    }
  }
  return out
}

