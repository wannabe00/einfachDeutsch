import { apiClient as client } from "./client"
import type { SavedWord, Word, WordProgress, ReviewQuality } from "@/types"

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

/** Words for the drills: learned words only, weak ones more often. Guests get
    a random set from the lowest level. */
export async function fetchDrillWords(): Promise<Word[]> {
  const { data } = await client.get<Word[]>("/vocabulary/words/drill/")
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

/* ---- The learner's own words ---- */

export async function fetchSavedWords(): Promise<SavedWord[]> {
  const { data } = await client.get<SavedWord[]>("/vocabulary/saved/")
  return data
}

export async function saveWord(word: { german: string; english?: string; notes?: string }): Promise<SavedWord> {
  const { data } = await client.post<SavedWord>("/vocabulary/saved/", word)
  return data
}

export async function deleteSavedWord(id: number): Promise<void> {
  await client.delete(`/vocabulary/saved/${id}/`)
}
