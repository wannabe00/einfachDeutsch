import { apiClient } from "./client"
import type {
  HistoryCompleteResult,
  HistoryLessonDetail,
  HistoryLessonSummary,
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
