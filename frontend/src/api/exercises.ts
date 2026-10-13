import { apiClient } from "./client"
import type { Exercise } from "@/types"

/** The shared exercises of a chapter, without answers (used for counts). */
export async function fetchExercises(chapter?: number): Promise<Exercise[]> {
  const params = chapter ? { chapter } : {}
  const { data } = await apiClient.get<Exercise[]>("/exercises/", { params })
  return data
}
