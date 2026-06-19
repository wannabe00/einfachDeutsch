import { apiClient } from "./client"
import type { Stats, ActivityDay } from "@/types"

export async function fetchStats(): Promise<Stats> {
  const { data } = await apiClient.get<Stats>("/stats/")
  return data
}

export async function fetchActivity(): Promise<ActivityDay[]> {
  const { data } = await apiClient.get<ActivityDay[]>("/stats/activity/")
  return data
}
