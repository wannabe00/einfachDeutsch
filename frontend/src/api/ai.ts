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

export async function aiSuggestWords(
  chapterTitle: string,
  description = "",
  count = 10,
): Promise<string> {
  const { data } = await apiClient.post<AIResponse>("/ai/suggest-words/", {
    chapter_title: chapterTitle,
    description,
    count,
  })
  return data.content
}

export async function aiExplainGrammar(topic: string): Promise<string> {
  const { data } = await apiClient.post<AIResponse>("/ai/explain-grammar/", {
    topic,
  })
  return data.content
}

export async function aiGenerateExercises(
  chapterTitle: string,
  wordList = "",
): Promise<string> {
  const { data } = await apiClient.post<AIResponse>("/ai/generate-exercises/", {
    chapter_title: chapterTitle,
    word_list: wordList,
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
