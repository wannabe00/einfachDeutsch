import { apiClient } from "./client"
import type { Exercise, ExerciseType, AttemptResult } from "@/types"

export async function fetchExercises(
  chapter?: number,
  type?: ExerciseType,
): Promise<Exercise[]> {
  const params: Record<string, string | number> = {}
  if (chapter) params.chapter = chapter
  if (type) params.type = type
  const { data } = await apiClient.get<Exercise[]>("/exercises/", { params })
  return data
}

/** user_answer shape depends on type: string | string[] | {left:right} map. */
export type UserAnswer = string | string[] | Record<string, string>

export async function attemptExercise(
  exerciseId: number,
  userAnswer: UserAnswer,
): Promise<AttemptResult> {
  const { data } = await apiClient.post<AttemptResult>(
    `/exercises/${exerciseId}/attempt/`,
    { user_answer: userAnswer },
  )
  return data
}

export async function createExercise(payload: {
  chapter: number
  exercise_type: ExerciseType
  prompt: string
  correct_answer: string
  hint?: string
  explanation?: string
}): Promise<Exercise> {
  const { data } = await apiClient.post<Exercise>("/exercises/", payload)
  return data
}
