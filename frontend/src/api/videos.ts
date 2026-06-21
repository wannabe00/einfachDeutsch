import { apiClient } from "./client"
import type { VideoSuggestionsResponse } from "@/types"

export async function fetchVideoSuggestions(): Promise<VideoSuggestionsResponse> {
  const { data } = await apiClient.get<VideoSuggestionsResponse>("/videos/")
  return data
}
