import { apiClient } from "./client"
import type { AIResponse, AISettings, ChatStarter } from "@/types"

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


/** How the AI talks to this learner (premium). */
export async function fetchAISettings(): Promise<AISettings> {
  const { data } = await apiClient.get<AISettings>("/ai/settings/")
  return data
}

export async function saveAISettings(settings: AISettings): Promise<AISettings> {
  const { data } = await apiClient.put<AISettings>("/ai/settings/", settings)
  return data
}

/** Chat starters built from the learner's progress. */
export async function fetchStarters(): Promise<ChatStarter[]> {
  const { data } = await apiClient.get<ChatStarter[]>("/ai/starters/")
  return data
}

/** The mic: a short recording -> what was said (Gemini, premium). */
export async function transcribe(audio: Blob): Promise<string> {
  const form = new FormData()
  form.append("audio", audio, "voice")
  // No Content-Type: the browser adds the multipart boundary (see uploadAvatar).
  const { data } = await apiClient.post<AIResponse>("/ai/transcribe/", form, {
    headers: { "Content-Type": undefined },
  })
  return data.content
}

/** The speaker button: an MP3 of `text` (Azure, premium). */
export async function readAloud(text: string): Promise<Blob> {
  const { data } = await apiClient.post<Blob>("/ai/read-aloud/", { text }, { responseType: "blob" })
  return data
}
