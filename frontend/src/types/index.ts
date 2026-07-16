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

export interface ReadingPassage {
  id: string
  level: CEFRLevel
  title: string
  text: string
  questions: PlacementQuestion[]
}

export interface PlacementTest {
  grammar: PlacementQuestion[]
  reading: ReadingPassage[]
  writing: { id: string; prompt: string }
}

export interface PlacementResult {
  suggested_level: CEFRLevel
  /** "ai" when Gemini decided the level, "local" on fallback. */
  source: "ai" | "local"
  rationale: string
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
  /** Optional artwork. Blank → the UI draws a platform tile instead. Must be a
      CSP-allowed host (Cloudinary/Unsplash) — see SourceArt. */
  image_url: string
}

export interface VideoSuggestionsResponse {
  unlocked: boolean
  unlock_level: CEFRLevel
  current_level: CEFRLevel
  suggestions: ShowSuggestion[]
}

export interface HistoryLessonSummary {
  id: number
  title: string
  era: string
  order: number
  completed: boolean
  cefr_level: CEFRLevel
  /** Teaser for the article card; derived from the body when not authored. */
  excerpt: string
  /** Optional hero image (CSP-allowed host). Blank → the card draws an era tile. */
  image_url: string
}

/* ---- AI chat history (Phase 23.13) — mirrors ai_assistant/serializers.py ---- */

export interface ConversationMessage {
  id: number
  role: "user" | "assistant"
  content: string
  created_at: string
}

/** Sidebar row. */
export interface Conversation {
  id: number
  title: string
  created_at: string
  updated_at: string
}

export interface ConversationDetail extends Conversation {
  messages: ConversationMessage[]
}

export interface HistoryQuizQuestion {
  id: number
  prompt: string
  options: string[]
}

export interface HistoryLessonDetail {
  id: number
  title: string
  era: string
  body_en: string
  body_de: string
  quiz: HistoryQuizQuestion[]
  completed: boolean
}

export interface HistoryCompleteResult {
  score: number
  correct: number
  total: number
  results: { id: number; correct: boolean; answer: string }[]
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
  /** False right after a social signup; true once username/password/name set. */
  profile_complete: boolean
  birthday: string | null
  avatar_url: string
  preferences: Record<string, unknown>
  /** Gate premium UI on this — it folds together the paid flag, an active
      trial, and expiry (Phase 23.7). */
  has_premium: boolean
  premium_until: string | null
  trial_started_at: string | null
}

/** Premium status for the upsell (GET /accounts/premium/). */
export interface PremiumStatus {
  has_premium: boolean
  premium_until: string | null
  trial_started_at: string | null
  trial_available: boolean
  trial_days: number
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

export type PartOfSpeech = "noun" | "verb" | "adjective" | "adverb" | "phrase" | "other"

export interface Word {
  id: number
  chapter: number
  english: string
  german: string
  notes: string
  /** Per-user SM-2 state; null for new (unreviewed) words and for guests. */
  progress: WordProgress | null
  /** From the word's chapter — the Word Bank groups by Level → part of speech. */
  cefr_level: CEFRLevel
  part_of_speech: PartOfSpeech
  /** True for a Lektion at your own level you haven't reached yet (Phase 23.9). */
  locked: boolean
}

/** Quality scale sent to the review endpoint: Again | Hard | Good | Easy. */
export type ReviewQuality = 0 | 2 | 4 | 5

export interface ReviewResult {
  quality: ReviewQuality
}

/** The lesson that teaches a grammar topic — powers the "next topic" hint. */
export interface GrammarUnlockLesson {
  id: number
  title: string
  unit_id: number
  unit_title: string
  unit_order: number
  lesson_order: number
}

export interface GrammarRule {
  id: number
  chapter: number
  title: string
  category: string
  content: string
  example_sentences: string
  /** From the rule's chapter — Grammar groups by Level → topic (Phase 23.10). */
  cefr_level: CEFRLevel
  /** Locked until the lesson that teaches it is done. */
  locked: boolean
  /** Non-null only while locked. */
  unlock_lesson: GrammarUnlockLesson | null
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

/** Real content totals for the marketing landing (Phase 22.4). */
export interface PublicStats {
  words: number
  exercises: number
  grammar_topics: number
  history_reads: number
  video_picks: number
}

export interface ImportResult {
  created: number
  skipped: number
}

/* ---- Learning path (Phase 23) — mirrors apps/curriculum/serializers.py ---- */

export type PathLessonState = "completed" | "current" | "available" | "locked"

export interface PathLesson {
  id: number
  order: number
  title: string
  xp_reward: number
  state: PathLessonState
  crown: number
}

export interface PathUnit {
  id: number
  cefr_level: string
  order: number
  title: string
  theme: string
  accent_color: string
  lessons: PathLesson[]
}

export interface PathEnergy {
  current: number
  max: number
  premium: boolean
  /** null when full or premium. */
  seconds_until_next: number | null
  refill_hours: number
}

export interface PathNextUp {
  lesson_id: number
  lesson_title: string
  unit_title: string
}

export interface PathResponse {
  level: string
  energy: PathEnergy
  next_up: PathNextUp | null
  units: PathUnit[]
}

export interface UnitWord {
  id: number
  german: string
  english: string
}

export interface UnitGrammar {
  id: number
  title: string
  category: string
  content: string
  example_sentences: string
}

/** One unit's page: its lessons plus the whole Lektion's review material. */
export interface PathUnitDetail extends PathUnit {
  words: UnitWord[]
  grammar: UnitGrammar[]
}

/* ---- Gamification (Phase 23.15) ---- */

export interface Gamification {
  total_xp: number
  crowns: number
  lessons_completed: number
  level: CEFRLevel
  level_lessons_total: number
  level_lessons_done: number
}

/* ---- Level checkpoint exam (Phase 23.14) ---- */

export interface ExamStatus {
  level: CEFRLevel
  next_level: CEFRLevel | null
  completed_lessons: number
  total_lessons: number
  /** 0..1 share of the level's lessons completed. */
  progress: number
  unlock_ratio: number
  unlocked: boolean
  pass_threshold: number
  question_count: number
  last_attempt: { score: number; passed: boolean; completed_at: string } | null
}

export interface ExamStart {
  attempt_id: number
  questions: ExerciseContent[]
}

export interface ExamResult {
  passed: boolean
  score: number
  correct: number
  total: number
  pass_threshold: number
  /** The level you were promoted to, or null if you didn't pass. */
  promoted_to: CEFRLevel | null
  level: CEFRLevel
  visible_levels: CEFRLevel[]
}

/* ---- Lesson player (Phase 23.5). Answers are never sent to the client. ---- */

export type LessonItemKind = "exercise" | "drill" | "review" | "grammar"

export interface ExerciseContent {
  exercise_id: number
  type: string
  prompt: string
  hint: string
  /** Solution keys are stripped server-side; holds e.g. options / tokens. */
  payload: { options?: string[]; tokens?: string[]; text?: string; bank?: string[] }
}

export interface ReviewContent {
  word_id: number
  german: string
  english: string
}

export interface GrammarContent {
  grammar_id: number
  title: string
  category: string
  content: string
  example_sentences: string
}

export interface LessonItemDTO {
  id: number
  order: number
  kind: LessonItemKind
  content: ExerciseContent | ReviewContent | GrammarContent | null
}

export interface LessonDetail {
  id: number
  order: number
  title: string
  xp_reward: number
  unit_id: number
  unit_title: string
  accent_color: string
  items: LessonItemDTO[]
  is_new: boolean
}

export interface AnswerResult {
  correct: boolean
  solution: string | string[]
  explanation: string
}

export interface CompleteResult {
  passed: boolean
  score: number
  correct: number
  total: number
  xp_earned: number
  crown: number
  spent_energy: boolean
  energy: PathEnergy
}
