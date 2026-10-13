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
