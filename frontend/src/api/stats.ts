import { apiClient } from "./client"
import type { Stats, ActivityDay, PublicStats } from "@/types"

/** Real content totals for the landing (Phase 22.4) — public, no auth. */
export async function fetchPublicStats(): Promise<PublicStats> {
  const { data } = await apiClient.get<PublicStats>("/stats/public/")
  return data
}

export async function fetchStats(): Promise<Stats> {
  const { data } = await apiClient.get<Stats>("/stats/")
  return data
}

export async function fetchActivity(): Promise<ActivityDay[]> {
  const { data } = await apiClient.get<ActivityDay[]>("/stats/activity/")
  return data
}
