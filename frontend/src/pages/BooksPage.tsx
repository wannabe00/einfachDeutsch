import { useQuery } from "@tanstack/react-query"
import { Link } from "react-router-dom"
import { ChevronRight, Library } from "lucide-react"

import { fetchBooks } from "@/api/books"
import type { Book } from "@/types"
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
        <p className="rounded-2xl bg-danger-bg p-4 font-medium text-danger">
          Couldn't load books. Try again in a moment.
        </p>
      )}

      <div className="flex flex-col gap-6">
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
  return (
    <section className="rounded-[24px] bg-surface p-5 shadow-card sm:p-6">
      <div className="flex items-start gap-4">
        <span className="flex size-14 shrink-0 items-center justify-center rounded-2xl bg-primary text-primary-foreground">
          <Library className="size-7" aria-hidden="true" />
        </span>
        <div className="min-w-0">
          <h2 className="text-2xl font-extrabold">{book.title}</h2>
          <p className="text-sm text-muted-foreground">
            {book.chapters.length} {book.chapters.length === 1 ? "chapter" : "chapters"}
            {book.description && ` · ${book.description}`}
          </p>
        </div>
      </div>
      <ul className="mt-5 overflow-hidden rounded-2xl bg-surface-2/60">
        {book.chapters.map((ch, i) => (
          <li key={ch.id}>
            {i > 0 && <div className="mx-4 h-px bg-border/70" aria-hidden="true" />}
            <Link
              to={`/chapters/${ch.id}`}
              className="flex min-h-[56px] items-center gap-4 px-4 py-2.5 transition-colors hover:bg-surface-2"
            >
              <span className="flex size-9 shrink-0 items-center justify-center rounded-full bg-surface text-sm font-bold tabular-nums shadow-card">
                {ch.number}
              </span>
              <span className="min-w-0 flex-1 truncate font-medium">{ch.title}</span>
              <ChevronRight className="size-5 shrink-0 text-muted-foreground" aria-hidden="true" />
            </Link>
          </li>
        ))}
        {book.chapters.length === 0 && (
          <li className="px-4 py-4 text-sm text-muted-foreground">No chapters yet.</li>
        )}
      </ul>
    </section>
  )
}
