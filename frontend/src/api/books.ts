import { apiClient } from "./client"
import type { Book } from "@/types"

/** The books and their chapters. Read-only: books are added by the owner. */
export async function fetchBooks(): Promise<Book[]> {
  const { data } = await apiClient.get<Book[]>("/books/")
  return data
}
