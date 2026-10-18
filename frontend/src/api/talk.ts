import { apiClient } from "./client"
import type { TalkDetail, TalkStart, TalkSummary, TalkTurn } from "@/types"

/** Start a talk: returns the short-lived Live token for the browser. */
export async function startTalk(): Promise<TalkStart> {
  const { data } = await apiClient.post<TalkStart>("/talk/start/")
  return data
}

/** Send the transcript; returns the talk with its report. */
export async function finishTalk(id: number, transcript: TalkTurn[]): Promise<TalkDetail> {
  const { data } = await apiClient.post<TalkDetail>(`/talk/${id}/finish/`, { transcript })
  return data
}

export async function fetchTalks(): Promise<TalkSummary[]> {
  const { data } = await apiClient.get<TalkSummary[]>("/talk/")
  return data
}

export async function fetchTalk(id: number): Promise<TalkDetail> {
  const { data } = await apiClient.get<TalkDetail>(`/talk/${id}/`)
  return data
}

/** Remove talks for good (their transcripts and reports are deleted). */
export async function removeTalks(ids: number[]): Promise<{ removed: number }> {
  const { data } = await apiClient.post<{ removed: number }>("/talk/remove/", { ids })
  return data
}
