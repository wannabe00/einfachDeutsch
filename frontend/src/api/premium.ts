import { apiClient } from "./client"
import type { PremiumStatus } from "@/types"

/** Am I premium, and can I still start the one-time trial? */
export async function fetchPremiumStatus(): Promise<PremiumStatus> {
  const { data } = await apiClient.get<PremiumStatus>("/accounts/premium/")
  return data
}

/** Start the one-time free trial. 400 if it's already been used. */
export async function startTrial(): Promise<PremiumStatus> {
  const { data } = await apiClient.post<PremiumStatus>("/accounts/premium/trial/")
  return data
}
