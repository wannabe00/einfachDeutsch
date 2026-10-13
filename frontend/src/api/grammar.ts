import { apiClient } from "./client"
import type { GrammarCategory, GrammarNext, GrammarRule } from "@/types"

/** Grammar topics; for a signed-in user only the ones they have learned. */
export async function fetchGrammarRules(
  chapter?: number,
  category?: GrammarCategory,
): Promise<GrammarRule[]> {
  const params: Record<string, string | number> = {}
  if (chapter) params.chapter = chapter
  if (category) params.category = category
  const { data } = await apiClient.get<GrammarRule[]>("/grammar/rules/", { params })
  return data
}

/** The next topic on your path, or null when there's none left. */
export async function fetchNextGrammarTopic(): Promise<GrammarNext | null> {
  const { data } = await apiClient.get<{ next: GrammarNext | null }>("/grammar/rules/next/")
  return data.next
}
