import { apiClient } from "./client"
import type { Stats, ActivityDay, PublicStats } from "@/types"

/** Live content counts for the landing page. Public, no login needed. */
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
