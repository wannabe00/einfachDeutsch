import { apiClient } from "./client"
import type { RecitationResult } from "@/types"

export async function submitRecitation(
  sourceText: string,
  audio: Blob,
): Promise<RecitationResult> {
  const form = new FormData()
  form.append("source_text", sourceText)
  form.append("audio", audio, "recitation.webm")
  const { data } = await apiClient.post<RecitationResult>(
    "/recitation/attempt/",
    form,
    { headers: { "Content-Type": "multipart/form-data" } },
  )
  return data
}
