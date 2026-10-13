import type { GrammarCategory } from "@/types"

export const GRAMMAR_CATEGORIES: { value: GrammarCategory; label: string }[] = [
  { value: "articles", label: "Articles" },
  { value: "cases", label: "Cases" },
  { value: "verbs", label: "Verbs & Conjugation" },
  { value: "sentence_structure", label: "Sentence Structure" },
  { value: "pronouns", label: "Pronouns" },
  { value: "adjectives", label: "Adjectives" },
  { value: "other", label: "Other" },
]

export function grammarCategoryLabel(v: string): string {
  return GRAMMAR_CATEGORIES.find((c) => c.value === v)?.label ?? v
}

/** Word Bank groups, listed in this order. */
export const PARTS_OF_SPEECH = [
  { value: "noun", label: "Nouns" },
  { value: "verb", label: "Verbs" },
  { value: "adjective", label: "Adjectives" },
  { value: "adverb", label: "Adverbs" },
  { value: "phrase", label: "Phrases" },
  { value: "other", label: "Other" },
]

export function partOfSpeechLabel(v: string): string {
  return PARTS_OF_SPEECH.find((p) => p.value === v)?.label ?? v
}
