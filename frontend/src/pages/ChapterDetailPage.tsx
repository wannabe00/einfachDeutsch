import { useQuery } from "@tanstack/react-query"
import { Link, useParams } from "react-router-dom"
import { ArrowLeft, BookMarked, BookOpen, NotebookPen } from "lucide-react"

import { fetchBooks } from "@/api/books"
import { fetchWords } from "@/api/vocabulary"
import { fetchGrammarRules } from "@/api/grammar"
import { fetchExercises } from "@/api/exercises"
import { ArticleBadge } from "@/components/vocabulary/ArticleBadge"

export default function ChapterDetailPage() {
  const { chapterId } = useParams<{ chapterId: string }>()
  const id = Number(chapterId)

  const { data: books } = useQuery({ queryKey: ["books"], queryFn: fetchBooks })
  const { data: words } = useQuery({
    queryKey: ["words", id],
    queryFn: () => fetchWords(id),
  })
  const { data: grammar } = useQuery({
    queryKey: ["grammar", id, undefined],
    queryFn: () => fetchGrammarRules(id),
  })
  const { data: exercises } = useQuery({
    queryKey: ["exercises", id, undefined],
    queryFn: () => fetchExercises(id),
  })

  const book = books?.find((b) => b.chapters.some((c) => c.id === id))
  const chapter = book?.chapters.find((c) => c.id === id)

  return (
    <div>
      <Link
        to="/books"
        className="inline-flex items-center gap-1.5 text-sm text-muted-foreground hover:text-accent"
      >
        <ArrowLeft className="size-4" /> Books
      </Link>

      <h1 className="mt-3 text-2xl font-semibold tracking-tight">
        {chapter?.title ?? "Chapter"}
      </h1>
      {book && (
        <p className="mt-1 text-sm text-muted-foreground">{book.title}</p>
      )}
      {chapter?.description && (
        <p className="mt-2 text-sm text-muted-foreground">{chapter.description}</p>
      )}

      {/* Quick counts */}
      <div className="mt-6 grid grid-cols-3 gap-4">
        {[
          { icon: BookMarked, label: "Words", value: words?.length ?? 0 },
          { icon: BookOpen, label: "Grammar rules", value: grammar?.length ?? 0 },
          { icon: NotebookPen, label: "Exercises", value: exercises?.length ?? 0 },
        ].map(({ icon: Icon, label, value }) => (
          <div
            key={label}
            className="flex flex-col gap-1.5 rounded-xl border border-border bg-surface p-4"
          >
            <Icon className="size-5 text-muted-foreground" aria-hidden="true" />
            <span className="text-2xl font-bold text-foreground">{value}</span>
            <span className="text-sm text-muted-foreground">{label}</span>
          </div>
        ))}
      </div>

      {/* Words in this chapter */}
      <div className="mt-8">
        <h2 className="text-xs font-semibold uppercase tracking-wide text-muted-foreground">
          Words
        </h2>
        {words && words.length > 0 ? (
          <div className="mt-3 overflow-hidden rounded-xl border border-border">
            {words.map((w, i) => (
              <div
                key={w.id}
                className={
                  "flex items-center justify-between bg-surface px-4 py-2 text-sm" +
                  (i > 0 ? " border-t border-border" : "")
                }
              >
                <span className="text-muted-foreground">{w.english}</span>
                <span className="flex items-center gap-2">
                  <ArticleBadge german={w.german} />
                  <span className="font-medium text-foreground">{w.german}</span>
                </span>
              </div>
            ))}
          </div>
        ) : (
          <p className="mt-3 text-sm text-muted-foreground">No words yet.</p>
        )}
      </div>

      {/* Placeholder for future book content / teacher assignment */}
      <div className="mt-8 rounded-xl border border-dashed border-border p-5 text-sm text-muted-foreground">
        Chapter reading content and teacher assignment will appear here once the
        book text is imported.
      </div>
    </div>
  )
}
