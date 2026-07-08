import { apiClient } from "./client"
import type { AIResponse } from "@/types"

export interface ChatTurn {
  role: "user" | "assistant"
  content: string
}

export async function aiChat(
  message: string,
  history: ChatTurn[] = [],
): Promise<string> {
  const { data } = await apiClient.post<AIResponse>("/ai/chat/", {
    message,
    history,
  })
  return data.content
}

export async function aiCheckAnswer(
  prompt: string,
  correctAnswer: string,
  userAnswer: string,
): Promise<string> {
  const { data } = await apiClient.post<AIResponse>("/ai/check-answer/", {
    prompt,
    correct_answer: correctAnswer,
    user_answer: userAnswer,
  })
  return data.content
}
