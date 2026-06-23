import { apiClient } from "./client"
import type {
  CEFRLevel,
  PlacementResult,
  PlacementTest,
  StreakStatus,
} from "@/types"

export async function fetchStreak(): Promise<StreakStatus> {
  const { data } = await apiClient.get<StreakStatus>("/accounts/streak/")
  return data
}

export async function setLevel(level: CEFRLevel): Promise<void> {
  await apiClient.post("/accounts/set-level/", { cefr_level: level })
}

export async function fetchPlacementTest(): Promise<PlacementTest> {
  const { data } = await apiClient.get<PlacementTest>("/accounts/placement-test/")
  return data
}

export async function submitPlacementTest(
  answers: Record<string, string>,
  writing: string,
): Promise<PlacementResult> {
  const { data } = await apiClient.post<PlacementResult>(
    "/accounts/placement-test/",
    { answers, writing },
  )
  return data
}
