import { apiClient } from "./client"
import type {
  HistoryCard,
  HistoryCompleteResult,
  HistoryLessonDetail,
  HistoryLessonSummary,
  LessonGuideReply,
} from "@/types"

export async function fetchHistoryLessons(): Promise<HistoryLessonSummary[]> {
  const { data } = await apiClient.get<HistoryLessonSummary[]>("/history/")
  return data
}

export async function fetchHistoryLesson(
  id: number,
): Promise<HistoryLessonDetail> {
  const { data } = await apiClient.get<HistoryLessonDetail>(`/history/${id}/`)
  return data
}

export async function completeHistoryLesson(
  id: number,
  answers: Record<string, string>,
): Promise<HistoryCompleteResult> {
  const { data } = await apiClient.post<HistoryCompleteResult>(
    `/history/${id}/complete/`,
    { answers },
  )
  return data
}

/* ---- AI-written lessons (premium) ---- */

const CUSTOM = "/history/custom/"

export async function fetchCustomLessons(): Promise<HistoryCard[]> {
  const { data } = await apiClient.get<HistoryCard[]>(CUSTOM)
  return data
}

export async function fetchCustomLesson(id: number): Promise<HistoryLessonDetail> {
  const { data } = await apiClient.get<HistoryLessonDetail>(`${CUSTOM}${id}/`)
  return data
}

/** One turn of the topic conversation; send the whole chat so far. */
export async function askLessonGuide(
  messages: { role: "user" | "assistant"; content: string }[],
): Promise<LessonGuideReply> {
  const { data } = await apiClient.post<LessonGuideReply>(`${CUSTOM}chat/`, { messages })
  return data
}

/** Have the AI write a lesson on the agreed topic (takes a little while). */
export async function createCustomLesson(topic: string): Promise<HistoryLessonDetail> {
  const { data } = await apiClient.post<HistoryLessonDetail>(CUSTOM, { topic })
  return data
}

export async function completeCustomLesson(
  id: number,
  answers: Record<string, string>,
): Promise<HistoryCompleteResult> {
  const { data } = await apiClient.post<HistoryCompleteResult>(`${CUSTOM}${id}/complete/`, {
    answers,
  })
  return data
}

export async function deleteCustomLesson(id: number): Promise<void> {
  await apiClient.delete(`${CUSTOM}${id}/`)
}
