import { apiClient } from "./client"
import type {
  AnswerResult,
  CheckData,
  CheckStart,
  CheckStatus,
  CompleteResult,
  FormResult,
  ExamResult,
  ExamStart,
  ExamStatus,
  Gamification,
  LesenAnswerResult,
  LesenSet,
  LesenSetDetail,
  LessonDetail,
  PathEnergy,
  PathResponse,
  PathUnitDetail,
  PracticeOptions,
  PointGrade,
  PracticeTask,
  SchreibenSet,
  SchreibenSetDetail,
  WriteResult,
  WritingAttempt,
} from "@/types"

/** XP + crowns + level progress for the Dashboard. */
export async function fetchGamification(): Promise<Gamification> {
  const { data } = await apiClient.get<Gamification>("/curriculum/gamification/")
  return data
}

/** Live energy for the global meter. Regen is computed server-side on read. */
export async function fetchEnergy(): Promise<PathEnergy> {
  const { data } = await apiClient.get<PathEnergy>("/curriculum/energy/")
  return data
}

/** The signed-in user's learning path: units ≤ their level, each lesson's
    state (completed/current/available/locked), energy, and what's next. */
export async function fetchPath(): Promise<PathResponse> {
  const { data } = await apiClient.get<PathResponse>("/curriculum/path/")
  return data
}

/** One unit: its lesson trail + the Lektion's vocab/grammar for review. */
export async function fetchUnit(unitId: number): Promise<PathUnitDetail> {
  const { data } = await apiClient.get<PathUnitDetail>(`/curriculum/units/${unitId}/`)
  return data
}

/** A lesson's playable items. Returns 402 when a free user is out of energy;
    that only applies to new lessons, since redoing one is always free. */
export async function fetchLesson(lessonId: number): Promise<LessonDetail> {
  const { data } = await apiClient.get<LessonDetail>(`/curriculum/lessons/${lessonId}/`)
  return data
}

/** Grade one item for immediate feedback (the solution comes back only now). */
export async function answerItem(
  lessonId: number,
  itemId: number,
  answer: unknown,
): Promise<AnswerResult> {
  const { data } = await apiClient.post<AnswerResult>(`/curriculum/lessons/${lessonId}/answer/`, {
    item_id: itemId,
    answer,
  })
  return data
}

/** Forget a started lesson's saved answers, to start it over. */
export async function restartLesson(lessonId: number): Promise<void> {
  await apiClient.delete(`/curriculum/lessons/${lessonId}/restart/`)
}

/** Finish the lesson. The server re-grades every answer (including ones saved
    before a resume) and awards XP and a crown. */
export async function completeLesson(
  lessonId: number,
  answers: { item_id: number; answer: unknown }[],
): Promise<CompleteResult> {
  const { data } = await apiClient.post<CompleteResult>(
    `/curriculum/lessons/${lessonId}/complete/`,
    { answers },
  )
  return data
}

/* ---- Level checkpoint exam ---- */

/** Progress toward the exam + whether it's unlocked. */
export async function fetchExamStatus(): Promise<ExamStatus> {
  const { data } = await apiClient.get<ExamStatus>("/curriculum/exam/")
  return data
}

/** Open an attempt. 403 while the level's path isn't finished. */
export async function startExam(): Promise<ExamStart> {
  const { data } = await apiClient.post<ExamStart>("/curriculum/exam/start/")
  return data
}

/** Submit answers keyed by question_id; the server grades and may promote you. */
export async function submitExam(
  attemptId: number,
  answers: Record<string, unknown>,
): Promise<ExamResult> {
  const { data } = await apiClient.post<ExamResult>("/curriculum/exam/submit/", {
    attempt_id: attemptId,
    answers,
  })
  return data
}

/* ---- Practice sets ---- */

/** The units and grammar topics a practice set can be narrowed to. */
export async function fetchPracticeOptions(): Promise<PracticeOptions> {
  const { data } = await apiClient.get<PracticeOptions>("/curriculum/practice/")
  return data
}

/** A new set of about ten tasks from finished lessons. */
export async function startPractice(filters: {
  unit?: number
  topic?: number
}): Promise<PracticeTask[]> {
  const { data } = await apiClient.post<{ tasks: PracticeTask[] }>(
    "/curriculum/practice/start/",
    filters,
  )
  return data.tasks
}

/** Grade one task. Same result shape as a lesson answer. */
export async function answerPractice(taskId: string, answer: unknown): Promise<AnswerResult> {
  const { data } = await apiClient.post<AnswerResult>("/curriculum/practice/answer/", {
    task_id: taskId,
    answer,
  })
  return data
}

/* ---- Checks: Lektion reviews and Modul tests ---- */

/** What can be reviewed or tested. */
export async function fetchChecks(): Promise<CheckStatus> {
  const { data } = await apiClient.get<CheckStatus>("/curriculum/checks/")
  return data
}

/** Start a check, or resume the unfinished one for the same Lektion or Modul. */
export async function startCheck(what: CheckStart): Promise<CheckData> {
  const { data } = await apiClient.post<CheckData>("/curriculum/checks/start/", what)
  return data
}

export async function fetchCheck(id: number): Promise<CheckData> {
  const { data } = await apiClient.get<CheckData>(`/curriculum/checks/${id}/`)
  return data
}

export async function answerCheck(id: number, taskId: string, answer: unknown): Promise<AnswerResult> {
  const { data } = await apiClient.post<AnswerResult>(`/curriculum/checks/${id}/answer/`, {
    task_id: taskId,
    answer,
  })
  return data
}

/** Score a check whose tasks are all answered. */
export async function finishCheck(id: number): Promise<CheckData> {
  const { data } = await apiClient.post<CheckData>(`/curriculum/checks/${id}/finish/`)
  return data
}

/** Every Lesen set the user may see, with locks and best scores. */
export async function fetchLesenSets(): Promise<LesenSet[]> {
  const { data } = await apiClient.get<LesenSet[]>("/curriculum/lesen/")
  return data
}

export async function fetchLesenSet(level: string, modul: number): Promise<LesenSetDetail> {
  const { data } = await apiClient.get<LesenSetDetail>(`/curriculum/lesen/${level}/${modul}/`)
  return data
}

export async function answerLesenTeil(exerciseId: number, answer: unknown): Promise<LesenAnswerResult> {
  const { data } = await apiClient.post<LesenAnswerResult>(`/curriculum/lesen/teil/${exerciseId}/answer/`, {
    answer,
  })
  return data
}

/** Every Schreiben set the user may see, with locks and best scores. */
export async function fetchSchreibenSets(): Promise<SchreibenSet[]> {
  const { data } = await apiClient.get<SchreibenSet[]>("/curriculum/schreiben/")
  return data
}

export async function fetchSchreibenSet(level: string, modul: number): Promise<SchreibenSetDetail> {
  const { data } = await apiClient.get<SchreibenSetDetail>(`/curriculum/schreiben/${level}/${modul}/`)
  return data
}

/** A1 Teil 1: grade the form. */
export async function answerSchreibenForm(exerciseId: number, answer: unknown): Promise<FormResult> {
  const { data } = await apiClient.post<FormResult>(`/curriculum/schreiben/teil/${exerciseId}/form/`, {
    answer,
  })
  return data
}

/** Save a written text; returns the checks, the points and the model answer. */
export async function writeSchreiben(exerciseId: number, text: string): Promise<WriteResult> {
  const { data } = await apiClient.post<WriteResult>(`/curriculum/schreiben/teil/${exerciseId}/write/`, {
    text,
  })
  return data
}

export async function selfCheckWriting(attemptId: number, points: PointGrade[]): Promise<WritingAttempt> {
  const { data } = await apiClient.post<WritingAttempt>(`/curriculum/schreiben/attempts/${attemptId}/self/`, {
    points,
  })
  return data
}

/** Premium: Gemini grades the text on the exam's criteria. */
export async function aiGradeWriting(attemptId: number): Promise<WritingAttempt> {
  const { data } = await apiClient.post<WritingAttempt>(`/curriculum/schreiben/attempts/${attemptId}/ai/`)
  return data
}

export async function fetchWritingAttempts(exerciseId: number): Promise<WritingAttempt[]> {
  const { data } = await apiClient.get<WritingAttempt[]>(`/curriculum/schreiben/teil/${exerciseId}/attempts/`)
  return data
}

/** Every recorded Hören set the user may see (same shape as Lesen). */
export async function fetchHoerenSets(): Promise<LesenSet[]> {
  const { data } = await apiClient.get<LesenSet[]>("/curriculum/hoeren/")
  return data
}

export async function fetchHoerenSet(level: string, modul: number): Promise<LesenSetDetail> {
  const { data } = await apiClient.get<LesenSetDetail>(`/curriculum/hoeren/${level}/${modul}/`)
  return data
}

export async function answerHoerenTeil(exerciseId: number, answer: unknown): Promise<LesenAnswerResult> {
  const { data } = await apiClient.post<LesenAnswerResult>(`/curriculum/hoeren/teil/${exerciseId}/answer/`, {
    answer,
  })
  return data
}
