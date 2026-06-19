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

export async function createGrammarRule(payload: {
  chapter: number
  title: string
  category: GrammarCategory
  content: string
  example_sentences: string
}): Promise<GrammarRule> {
  const { data } = await apiClient.post<GrammarRule>("/grammar/rules/", payload)
  return data
}
