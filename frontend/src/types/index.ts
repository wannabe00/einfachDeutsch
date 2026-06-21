/**
 * Shared API types — keep in sync with the Django REST serializers.
 * Mirrors the models defined in backend/apps/*.
 */

export type CEFRLevel = "A1" | "A2" | "B1" | "B2" | "C1" | "C2"

export interface PlacementQuestion {
  id: string
  level: CEFRLevel
  prompt: string
  options: string[]
}

export interface PlacementResult {
  suggested_level: CEFRLevel
  correct: number
  total: number
  per_level: Record<string, { correct: number; total: number }>
}

export interface StreakStatus {
  current_streak: number
  longest_streak: number
  freeze_tokens: number
  last_active_date: string | null
  today_is_unlock_day: boolean
  next_unlock_date: string
  unlock_weekdays: number[]
}

export interface RecitationGrammarError {
  error: string
  correction: string
  type: string
}

export interface RecitationResult {
  id: number
  transcript: string
  coverage_score: number | null
  covered: string[]
  missed: string[]
  grammar_errors: RecitationGrammarError[]
  pronunciation_notes: string[]
  summary: string
}

export interface ShowSuggestion {
  id: number
  title: string
  description: string
  url: string
  platform: string
  cefr_level: CEFRLevel
}

export interface VideoSuggestionsResponse {
  unlocked: boolean
  unlock_level: CEFRLevel
  current_level: CEFRLevel
  suggestions: ShowSuggestion[]
}

export type UserRole = "student" | "teacher"

export interface User {
  pk: number
  username: string
  email: string
  first_name: string
  last_name: string
  cefr_level: CEFRLevel
  role: UserRole
  /** Whether the user has chosen/confirmed their level (onboarding done). */
  level_set: boolean
}

export interface Book {
  id: number
  title: string
  description: string
  chapters: Chapter[]
}

export interface Chapter {
  id: number
  book: number
  number: number
  title: string
  description: string
}

export interface WordProgress {
  repetitions: number
  ease_factor: number
  interval: number
  next_review: string // ISO date string
  last_reviewed: string | null
  times_seen: number
  times_correct: number
  times_wrong: number
  lapses: number
}

export interface Word {
  id: number
  chapter: number
  english: string
  german: string
  notes: string
  /** Per-user SM-2 state; null for new (unreviewed) words and for guests. */
  progress: WordProgress | null
}

/** Quality scale sent to the review endpoint: Again | Hard | Good | Easy. */
export type ReviewQuality = 0 | 2 | 4 | 5

export interface ReviewResult {
  quality: ReviewQuality
}

export interface GrammarRule {
  id: number
  chapter: number
  title: string
  category: string
  content: string
  example_sentences: string
}

export type ExerciseType =
  | "translation"
  | "fill_blank"
  | "article"
  | "conjugation"
  | "free_text"
  | "multiple_choice"
  | "matching"
  | "sentence_order"
  | "word_bank"

/** Solution-stripped payload shapes the UI receives (varies by type). */
export interface ExercisePayload {
  options?: string[] // multiple_choice
  left?: string[] // matching
  right?: string[] // matching (shuffled)
  tokens?: string[] // sentence_order
  text?: string // word_bank ("Ich ___ in ___.")
  bank?: string[] // word_bank
}

export interface Exercise {
  id: number
  chapter: number
  exercise_type: ExerciseType
  prompt: string
  payload: ExercisePayload
  hint: string
  explanation: string
  source: string
  // correct_answer is intentionally omitted — it is never sent in list/retrieve.
}

/** Returned by POST /api/exercises/{id}/attempt/ */
export interface AttemptResult {
  is_correct: boolean
  // Shape mirrors the type: string for simple, string[] / map for interactive.
  correct_answer: string | string[] | Record<string, string>
  explanation: string
  ai_feedback: string
}

export interface ExerciseAttempt {
  user_answer: string
  is_correct: boolean
  correct_answer: string
  ai_feedback: string
}

export type GrammarCategory =
  | "articles"
  | "cases"
  | "verbs"
  | "sentence_structure"
  | "pronouns"
  | "adjectives"
  | "other"

export interface AIResponse {
  content: string
}

export interface Stats {
  due_today: number
  learned_total: number
  reviewed_today: number
  total_words: number
  total_grammar_rules: number
  total_exercises: number
}

export interface ActivityDay {
  date: string // ISO date
  count: number
}

export interface ImportResult {
  created: number
  skipped: number
}
