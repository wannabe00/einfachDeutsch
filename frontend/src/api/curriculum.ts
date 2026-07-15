import { apiClient } from "./client"
import type { PathResponse, PathUnitDetail } from "@/types"

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
