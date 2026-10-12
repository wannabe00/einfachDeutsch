import { useState, type FormEvent } from "react"
import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query"
import { Link } from "react-router-dom"
import { ChevronRight } from "lucide-react"

import { createChapter, fetchBooks } from "@/api/books"
import type { Book } from "@/types"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { PageHeader } from "@/components/layout/PageHeader"

export default function BooksPage() {
  const {
    data: books,
    isLoading,
    isError,
  } = useQuery({ queryKey: ["books"], queryFn: fetchBooks })

  return (
    <div className="flex flex-col gap-6">
      <PageHeader
        title="Books"
        subtitle="Your books and the chapters you're working through."
      />

      {isLoading && <p className="text-muted-foreground">Loading books…</p>}

      {isError && (
        <p className="text-danger">
          Couldn't load books. Is the backend running on port 8000?
        </p>
      )}

      <div className="flex flex-col gap-4">
        {books?.map((book) => (
          <BookCard key={book.id} book={book} />
        ))}
        {books?.length === 0 && (
          <p className="text-muted-foreground">
            No books yet. Add one in the Django admin.
          </p>
        )}
      </div>
    </div>
  )
}

function BookCard({ book }: { book: Book }) {
  const nextNumber =
    book.chapters.reduce((max, ch) => Math.max(max, ch.number), 0) + 1

  return (
    <div className="rounded-xl border border-border bg-surface p-6">
      <h2 className="text-lg font-bold tracking-tight">{book.title}</h2>
      {book.description && (
        <p className="mt-1 text-sm text-muted-foreground">{book.description}</p>
      )}
      <ul className="mt-4 flex flex-col gap-1">
        {book.chapters.map((ch) => (
          <li key={ch.id}>
            <Link
              to={`/chapters/${ch.id}`}
              className="flex items-center justify-between rounded-lg px-3 py-2 text-sm transition-colors hover:bg-muted"
            >
              <span>
                <span className="font-medium">Chapter {ch.number}:</span>{" "}
                {ch.title}
              </span>
              <ChevronRight className="size-4 text-muted-foreground" />
            </Link>
          </li>
        ))}
        {book.chapters.length === 0 && (
          <li className="px-3 text-sm text-muted-foreground">No chapters yet.</li>
        )}
      </ul>
      <AddChapterForm bookId={book.id} nextNumber={nextNumber} />
    </div>
  )
}

function AddChapterForm({
  bookId,
  nextNumber,
}: {
  bookId: number
  nextNumber: number
}) {
  const queryClient = useQueryClient()
  const [title, setTitle] = useState("")
  const [number, setNumber] = useState(String(nextNumber))

  const mutation = useMutation({
    mutationFn: () =>
      createChapter(bookId, { title: title.trim(), number: Number(number) }),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ["books"] })
      setTitle("")
    },
  })

  const handleSubmit = (event: FormEvent<HTMLFormElement>) => {
    event.preventDefault()
    if (!title.trim() || !number) return
    mutation.mutate()
  }

  return (
    <form
      onSubmit={handleSubmit}
      className="mt-4 flex flex-wrap items-center gap-2 border-t border-border pt-4"
    >
      <Input
        type="number"
        min={1}
        aria-label="Chapter number"
        value={number}
        onChange={(e) => setNumber(e.target.value)}
        className="w-20"
      />
      <Input
        aria-label="Chapter title"
        placeholder="Chapter title"
        value={title}
        onChange={(e) => setTitle(e.target.value)}
        className="min-w-40 flex-1"
      />
      <Button type="submit" disabled={mutation.isPending}>
        {mutation.isPending ? "Adding…" : "Add Chapter"}
      </Button>
      {mutation.isError && (
        <span className="text-sm text-danger">Failed to add chapter.</span>
      )}
    </form>
  )
}
