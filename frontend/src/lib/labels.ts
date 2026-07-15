import type { GrammarCategory, ExerciseType } from "@/types"

export const GRAMMAR_CATEGORIES: { value: GrammarCategory; label: string }[] = [
  { value: "articles", label: "Articles" },
  { value: "cases", label: "Cases" },
  { value: "verbs", label: "Verbs & Conjugation" },
  { value: "sentence_structure", label: "Sentence Structure" },
  { value: "pronouns", label: "Pronouns" },
  { value: "adjectives", label: "Adjectives" },
  { value: "other", label: "Other" },
]

export const EXERCISE_TYPES: { value: ExerciseType; label: string }[] = [
  { value: "translation", label: "Translate to German" },
  { value: "fill_blank", label: "Fill in the Blank" },
  { value: "article", label: "Choose Correct Article" },
  { value: "conjugation", label: "Conjugate the Verb" },
  { value: "free_text", label: "Free Text Answer" },
  { value: "multiple_choice", label: "Multiple Choice" },
  { value: "matching", label: "Match Pairs" },
  { value: "sentence_order", label: "Put Words in Order" },
  { value: "word_bank", label: "Fill from Word Bank" },
]

export function grammarCategoryLabel(v: string): string {
  return GRAMMAR_CATEGORIES.find((c) => c.value === v)?.label ?? v
}

export function exerciseTypeLabel(v: string): string {
  return EXERCISE_TYPES.find((t) => t.value === v)?.label ?? v
}

/** Word Bank groups (Phase 23.9). Order defines how the groups are listed. */
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
