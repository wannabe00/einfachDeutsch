import { apiClient } from "./client"
import type {
  AnswerResult,
  CompleteResult,
  LessonDetail,
  PathEnergy,
  PathResponse,
  PathUnitDetail,
} from "@/types"

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

/** A lesson's playable items. 402 if a free user is out of energy (new lessons
    only — redoing a completed lesson is always free). */
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

/** Finish the lesson — the server re-grades everything and awards XP/crown. */
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
