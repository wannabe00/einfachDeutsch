import { apiClient } from "./client"
import type { CEFRLevel, PlacementQuestion, PlacementResult } from "@/types"

export async function setLevel(level: CEFRLevel): Promise<void> {
  await apiClient.post("/accounts/set-level/", { cefr_level: level })
}

export async function fetchPlacementTest(): Promise<PlacementQuestion[]> {
  const { data } = await apiClient.get<{ questions: PlacementQuestion[] }>(
    "/accounts/placement-test/",
  )
  return data.questions
}

export async function submitPlacementTest(
  answers: Record<string, string>,
): Promise<PlacementResult> {
  const { data } = await apiClient.post<PlacementResult>(
    "/accounts/placement-test/",
    { answers },
  )
  return data
}
