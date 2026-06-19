import { apiClient as client } from "./client"
import type { Word, WordProgress, ReviewQuality } from "@/types"

export async function fetchWords(chapter?: number): Promise<Word[]> {
  const params = chapter ? { chapter } : {}
  const { data } = await client.get<Word[]>("/vocabulary/words/", { params })
  return data
}

export async function fetchDueWords(chapter?: number): Promise<Word[]> {
  const params = chapter ? { chapter } : {}
  const { data } = await client.get<Word[]>("/vocabulary/words/due/", { params })
  return data
}

export interface DueCounts {
  total: number
  per_chapter: Record<number, number>
}

export async function fetchDueCounts(): Promise<DueCounts> {
  const { data } = await client.get<DueCounts>("/vocabulary/words/due-counts/")
  return data
}

export async function createWord(payload: {
  english: string
  german: string
  chapter: number
  notes?: string
}): Promise<Word> {
  const { data } = await client.post<Word>("/vocabulary/words/", payload)
  return data
}

export async function importWordsCsv(
  file: File,
  chapterId: number,
): Promise<{ created: number; skipped: number }> {
  const form = new FormData()
  form.append("file", file)
  form.append("chapter_id", String(chapterId))
  const { data } = await client.post("/vocabulary/words/import/", form)
  return data
}

export async function bulkAddWords(
  chapterId: number,
  rows: { german: string; english: string; notes?: string }[],
): Promise<{ created: number; skipped: number }> {
  const { data } = await client.post("/vocabulary/words/bulk/", {
    chapter_id: chapterId,
    rows,
  })
  return data
}

export async function reviewWord(
  wordId: number,
  quality: ReviewQuality,
): Promise<WordProgress> {
  const { data } = await client.post<WordProgress>(
    `/vocabulary/words/${wordId}/review/`,
    { quality },
  )
  return data
}
