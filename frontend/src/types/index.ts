/** API types. Keep these in sync with the Django serializers in backend/apps. */

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
}

export interface ShowSuggestion {
  id: number
  title: string
  /** What it is. */
  description: string
  /** Who it's for. */
  audience: string
  /** Format and length, e.g. "Episodes of 10-20 minutes, weekly." */
  format: string
  /** e.g. "Free" or "Netflix subscription". */
  cost: string
  /** How to use it for learning. */
  tips: string[]
  url: string
  platform: string
  cefr_level: CEFRLevel
  /** A YouTube thumbnail, or blank for a drawn platform tile (see SourceArt). */
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

/** What a history card needs; both built-in and AI-written lessons have it. */
export type HistoryCard = Omit<HistoryLessonSummary, "order">

/** One turn of the "ask for a lesson" conversation. */
export interface LessonGuideReply {
  /** ask: a follow-up question; ready: `topic` is agreed; refuse: off-topic. */
  status: "ask" | "ready" | "refuse"
  reply: string
  topic: string
}

/* ---- AI chat history (ai_assistant/serializers.py) ---- */

export interface ConversationMessage {
  id: number
  role: "user" | "assistant"
  content: string
  created_at: string
}

/** The learning tool a chat uses. */
export type ChatMode = "chat" | "quiz" | "correct" | "roleplay" | "explain"

/** Sidebar row. */
export interface Conversation {
  id: number
  title: string
  pinned: boolean
  mode: ChatMode
  created_at: string
  updated_at: string
}

/** A chat starter from the learner's progress. `send` false = switch to the
    tool and let the learner type. */
export interface ChatStarter {
  label: string
  message: string
  mode: ChatMode
  send: boolean
}

export interface AISettings {
  reply_language: "auto" | "en" | "mixed" | "de"
  tone: "friendly" | "strict"
  corrections: "major" | "all"
  interests: string
  about: string
  /** What "By my level" means for this learner right now. */
  auto_language?: "en" | "mixed" | "de"
}

/** A word the learner keeps for themselves (Word Bank, saved from chat). */
export interface SavedWord {
  id: number
  german: string
  english: string
  notes: string
  created_at: string
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
  /** A picture bundled with the app (`/history/...jpg`), or blank. */
  image_url: string
  /** Who made the picture and where it's from. */
  image_credit: string
  /** AI-written lessons only: what the user asked for. */
  topic?: string
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
  /** Two-factor login (authenticator app) is on. */
  two_factor: boolean
  /** Gate premium UI on this. It combines the paid flag, an active trial and
      the expiry date. */
  has_premium: boolean
  premium_until: string | null
  trial_started_at: string | null
  /** Staff may edit shared content (the API enforces it). */
  is_staff: boolean
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
  /** From the word's chapter. */
  cefr_level: CEFRLevel
  part_of_speech: PartOfSpeech
  /** What the Word Bank groups by: the unit that teaches the word (`order` is
      its place on the path), or the chapter you added it to (`order` null). */
  topic: { key: string; title: string; order: number | null }
  /** A noun's plural, e.g. "die Hunde"; empty when there is none. */
  plural: string
}

/** Quality scale sent to the review endpoint: Again | Hard | Good | Easy. */
export type ReviewQuality = 0 | 2 | 4 | 5

/** The next grammar topic on your path and the lesson that teaches it. */
export interface GrammarNext {
  title: string
  lesson: { title: string; unit_id: number; unit_order: number; unit_title: string }
}

export interface GrammarRule {
  id: number
  chapter: number
  title: string
  category: string
  content: string
  example_sentences: string
  /** From the rule's chapter. Grammar groups by level, then topic. */
  cefr_level: CEFRLevel
  /** One of the level's main topics, listed together first. */
  core: boolean
}

/** Solution-stripped payload shapes the UI receives (varies by type). */
export interface ExercisePayload {
  options?: string[] // multiple_choice
  left?: string[] // matching
  right?: string[] // matching (sorted)
  tokens?: string[] // sentence_order; error_spot: the sentence's words
  text?: string // word_bank ("Ich ___ in ___.")
  bank?: string[] // word_bank
  parts?: PartContent[] // group: the parts shown together on one screen
  /** A dialogue or reading text shown above the task (multiple_choice, group). */
  context?: string
  /** Base64 of German the browser reads aloud ("which word do you hear?", dictation). */
  say?: string
  /** A Hören recording and how often it may be played before checking. */
  audio?: { url: string; plays: number }
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
  /** Words taught by lessons the user has finished. */
  words_learned: number
  /** Words reviewed until their SM-2 interval is over three weeks. */
  mastered_total: number
  reviewed_today: number
  total_words: number
  total_grammar_rules: number
  total_exercises: number
}

export interface ActivityDay {
  date: string // ISO date
  count: number
}

/** Live content counts shown on the landing page. */
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

/* ---- Learning path (curriculum/serializers.py) ---- */

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

/* ---- XP and crowns ---- */

export interface Gamification {
  total_xp: number
  crowns: number
  lessons_completed: number
  level: CEFRLevel
  level_lessons_total: number
  level_lessons_done: number
}

/* ---- Level exam ---- */

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
  questions: ExamQuestion[]
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

/* ---- Lesson player. Answers are never sent to the client. ---- */

export type LessonItemKind = "exercise" | "drill" | "review" | "grammar"

/** One exercise as the player shows it: a whole exercise, one part of a
    multi-part ("group") exercise, or an exam question. */
export interface PartContent {
  type: string
  prompt: string
  hint: string
  /** Solution keys are stripped server-side. */
  payload: ExercisePayload
}

export interface ExerciseContent extends PartContent {
  exercise_id: number
}

export interface ExamQuestion extends PartContent {
  /** "12" for an exercise, "12:3" for part 3 of a multi-part one. */
  question_id: string
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
  /** Set when the lesson was started and left: where to pick up. The answers
      stay on the server, which counts them when the lesson is finished. */
  saved: { step: number; answers: Record<string, unknown> } | null
}

/** A string, a list (sentence order, word bank) or [left, right] pairs (matching). */
export type PartSolution = string | string[] | [string, string][]

export interface AnswerResult {
  correct: boolean
  /** One verdict per part; a single exercise has one. */
  parts: boolean[]
  /** A group's solution is one PartSolution per part. */
  solution: PartSolution | PartSolution[]
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

/** The Dashboard's short review of the unit finished most recently. */
/* ---- Practice sets ---- */

export interface PracticeOptions {
  units: { id: number; order: number; title: string; cefr_level: string }[]
  /** `lektion` is the Lektion that teaches the topic. */
  topics: { id: number; title: string; cefr_level: string; lektion: number }[]
}

export interface PracticeTask extends PartContent {
  /** "12" for an exercise, "12:0,3" for those parts of a multi-part one. */
  task_id: string
}

/* ---- Checks: Lektion reviews and Modul tests ---- */

export type CheckSkill = "words" | "grammar" | "listening" | "reading"

export interface CheckUnit {
  id: number
  order: number
  title: string
  cefr_level: string
}

export interface ModulTest {
  cefr_level: string
  modul: number
  first: number
  last: number
  unlocked: boolean
  /** 0..1, null until a test is finished. */
  best_score: number | null
  in_progress: boolean
}

export interface CheckStatus {
  /** The Lektion finished most recently, for the Dashboard. */
  last_unit: CheckUnit | null
  /** Every Lektion that can be reviewed. */
  units: CheckUnit[]
  moduls: ModulTest[]
}

export interface CheckTask extends PartContent {
  task_id: string
  skill: CheckSkill
}

export interface CheckData {
  id: number
  kind: "review" | "modul"
  cefr_level: string
  modul: number | null
  unit: CheckUnit
  title: string
  subtitle: string
  tasks: CheckTask[]
  /** Results of the tasks answered so far, by task id. */
  results: Record<string, AnswerResult>
  completed: boolean
  score: number | null
  skills: Partial<Record<CheckSkill, { right: number; total: number }>>
}

export type CheckStart = { kind: "review"; unit: number } | { kind: "modul"; level: string; modul: number }

/* ---- Lesen: exam-style reading, one set per Modul ---- */

export interface LesenTeilSummary {
  id: number
  teil: number
  title: string
  questions: number
  /** Best right answers so far; null until tried. */
  best: number | null
}

interface LesenSetBase {
  cefr_level: CEFRLevel
  modul: number
  first: number
  last: number
  questions: number
  /** Best right answers over the whole set, once every Teil is done. */
  best: number | null
  passed: boolean
}

export interface LesenSet extends LesenSetBase {
  locked: boolean
  teile: LesenTeilSummary[]
}

export interface LesenTeil extends ExerciseContent {
  teil: number
  best: number | null
}

export interface LesenSetDetail extends LesenSetBase {
  /** Share of right answers needed to pass, as in the exam (0.6). */
  pass_share: number
  teile: LesenTeil[]
}

export interface LesenAnswerResult extends AnswerResult {
  right: number
  total: number
  best: number
  /** Hören: the scripts, one per recording (a Teil's single recording, or one per question). */
  transcripts?: string[]
}

/* ---- Schreiben: exam-style writing, one set per Modul ---- */

/** A free-writing task. The model answer arrives only after writing. */
export interface WritingTask {
  situation: string
  points: string[]
  min_words: number
  max_words: number
  formal: boolean
}

export type PointGrade = "full" | "partial" | "missing"

export interface SchreibenBest {
  score: number
  out_of: number
  graded_by: "auto" | "self" | "ai"
}

export interface SchreibenTeilSummary {
  id: number
  teil: number
  title: string
  best: SchreibenBest | null
}

interface SchreibenSetBase {
  cefr_level: CEFRLevel
  modul: number
  first: number
  last: number
  /** Points over the whole set, once every Teil is graded. */
  best: number | null
  out_of: number | null
  passed: boolean
}

export interface SchreibenSet extends SchreibenSetBase {
  locked: boolean
  teile: SchreibenTeilSummary[]
}

/** A form Teil (A1 Teil 1, a group) or a free-writing Teil. */
export interface SchreibenTeil extends ExerciseContent {
  teil: number
  best: SchreibenBest | null
  payload: ExercisePayload & Partial<WritingTask>
}

export interface SchreibenSetDetail extends SchreibenSetBase {
  pass_share: number
  teile: SchreibenTeil[]
}

export interface WritingChecks {
  words: number
  min_words: number
  max_words: number
  in_range: boolean
  too_short: boolean
  greeting: boolean
  closing: boolean
}

export interface WritingAttempt {
  id: number
  exercise_id: number
  /** The text, or the form's answers. */
  answer: string | string[]
  words: number
  points: PointGrade[]
  /** null until graded (self-check or AI). */
  score: number | null
  max_score: number
  graded_by: "" | "auto" | "self" | "ai"
  feedback: {
    checks?: WritingChecks
    grades?: { communication?: number; task?: string; language?: string | null }
    comments?: string[]
    corrected?: string
    tips?: string[]
  }
  created_at: string
}

export interface WriteResult {
  attempt: WritingAttempt
  points: string[]
  model: string
}

export interface FormResult extends AnswerResult {
  attempt: WritingAttempt
}

/* ---- Talk to AI: live voice conversations (premium) ---- */

export interface TalkStart {
  id: number
  /** Short-lived Gemini Live token; the model, voice and role are locked into it. */
  token: string
  model: string
  minutes: number
}

export interface TalkTurn {
  role: "user" | "ai"
  text: string
}

export interface TalkReport {
  summary: string
  corrections: { you_said: string; better: string; why: string }[]
  phrases: string[]
  new_words: { german: string; english: string }[]
  practise: string[]
}

export interface TalkSummary {
  id: number
  started_at: string
  ended_at: string | null
  summary: string
}

export interface TalkDetail extends TalkSummary {
  transcript: TalkTurn[]
  /** Empty when the learner said nothing. */
  report: TalkReport | Record<string, never>
}
