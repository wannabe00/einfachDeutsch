import { apiClient } from "./client"
import type { AIResponse } from "@/types"

interface ChatTurn {
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

