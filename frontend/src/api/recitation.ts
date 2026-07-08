import { apiClient } from "./client"
import type { RecitationResult } from "@/types"

export async function submitRecitation(
  sourceText: string,
  audio: Blob,
): Promise<RecitationResult> {
  const form = new FormData()
  form.append("source_text", sourceText)
  form.append("audio", audio, "recitation.webm")
  // Leave Content-Type unset so the browser adds the multipart boundary
  // (hardcoding it omits the boundary and the server can't parse the upload).
  const { data } = await apiClient.post<RecitationResult>(
    "/recitation/attempt/",
    form,
    { headers: { "Content-Type": undefined } },
  )
  return data
}
