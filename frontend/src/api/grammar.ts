import { apiClient } from "./client"
import type { GrammarRule, GrammarCategory } from "@/types"

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
