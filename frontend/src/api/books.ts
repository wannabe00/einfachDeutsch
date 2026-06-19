import { apiClient } from "./client"
import type { Book, Chapter } from "@/types"

export async function fetchBooks(): Promise<Book[]> {
  const { data } = await apiClient.get<Book[]>("/books/")
  return data
}

export interface NewChapter {
  number: number
  title: string
  description?: string
}

export async function createChapter(
  bookId: number,
  payload: NewChapter
): Promise<Chapter> {
  const { data } = await apiClient.post<Chapter>(
    `/books/${bookId}/chapters/`,
    payload
  )
  return data
}
