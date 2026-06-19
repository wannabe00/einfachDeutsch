import { useMemo, useState } from "react"
import { useQuery } from "@tanstack/react-query"

import { fetchWords } from "@/api/vocabulary"
import { fetchBooks } from "@/api/books"
import type { Chapter } from "@/types"
import { WordRow } from "@/components/vocabulary/WordRow"
import { WordForm } from "@/components/vocabulary/WordForm"
import { CSVImportButton } from "@/components/vocabulary/CSVImportButton"
import { PasteWordsButton } from "@/components/vocabulary/PasteWordsButton"
import { WordOverview } from "@/components/vocabulary/WordOverview"
import { ChapterButtons } from "@/components/layout/ChapterButtons"
import { Button } from "@/components/ui/button"
import { useAIPanel } from "@/contexts/AIPanelContext"
import { Sparkles, ChevronLeft, ChevronRight, Plus } from "lucide-react"

const PAGE_SIZE = 15
type Selection = number | "all"

export default function WordBankPage() {
  const [selection, setSelection] = useState<Selection>("all")
  const [showForm, setShowForm] = useState(false)
  const [page, setPage] = useState(0)

  const { openPanel } = useAIPanel()
  const { data: books } = useQuery({ queryKey: ["books"], queryFn: fetchBooks })
  const { data: words, isLoading } = useQuery({
    queryKey: ["words", selection],
    queryFn: () => fetchWords(selection === "all" ? undefined : selection),
  })

  const allChapters: Chapter[] = books?.flatMap((b) => b.chapters) ?? []
  const chapterTitle = (id: number) =>
    allChapters.find((c) => c.id === id)?.title ?? "—"
  const defaultChapterId =
    selection === "all" ? allChapters[0]?.id : selection

  // Reset to first page whenever the filter changes (render-time, not an effect).
  const [pagedFor, setPagedFor] = useState<Selection>(selection)
  if (pagedFor !== selection) {
    setPagedFor(selection)
    setPage(0)
  }

  const totalPages = words ? Math.ceil(words.length / PAGE_SIZE) : 0
  const pageWords = useMemo(
    () => (words ?? []).slice(page * PAGE_SIZE, page * PAGE_SIZE + PAGE_SIZE),
    [words, page],
  )

  return (
    <div>
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-2xl font-semibold tracking-tight">Word Bank</h1>
          <p className="mt-1 text-sm text-muted-foreground">
            {words?.length ?? 0} words
            {selection !== "all" && ` · ${chapterTitle(selection)}`}
          </p>
        </div>
        <div className="flex gap-2">
          <Button
            variant="secondary"
            onClick={() =>
              openPanel(
                "AI · Generate words",
                `Suggest 10 vocabulary words for chapter: ${
                  selection === "all" ? "beginner German" : chapterTitle(selection)
                }. Give German (with article) and English.`,
              )
            }
          >
            <Sparkles className="mr-2 size-4" /> Generate with AI
          </Button>
          <Button variant="default" onClick={() => setShowForm((v) => !v)}>
            {showForm ? "Cancel" : <><Plus className="mr-2 size-4" /> Add Words</>}
          </Button>
        </div>
      </div>

      {/* Add Words popup — single form + paste list + CSV together */}
      {showForm && allChapters.length > 0 && (
        <div className="mt-4 flex flex-col gap-4 rounded-xl border border-border bg-surface p-4">
          <WordForm
            chapters={allChapters}
            defaultChapterId={defaultChapterId}
            onDone={() => setShowForm(false)}
          />
          <div className="flex flex-wrap gap-2 border-t border-border pt-4">
            <PasteWordsButton chapters={allChapters} defaultChapterId={defaultChapterId} />
            <CSVImportButton chapters={allChapters} defaultChapterId={defaultChapterId} />
          </div>
        </div>
      )}

      {/* Overview */}
      {words && words.length > 0 && (
        <div className="mt-6">
          <WordOverview words={words} />
        </div>
      )}

      {/* Chapter buttons */}
      {books && (
        <div className="mt-6">
          <ChapterButtons books={books} selected={selection} onSelect={setSelection} />
        </div>
      )}

      {/* Word table (paginated) */}
      <div className="mt-6">
        {isLoading ? (
          <p className="text-sm text-muted-foreground">Loading…</p>
        ) : !words?.length ? (
          <p className="text-sm text-muted-foreground">No words yet. Add some above.</p>
        ) : (
          <>
            <table className="w-full">
              <thead>
                <tr className="border-b border-border">
                  {["English", "German", "Chapter", "Next review", "Progress"].map(
                    (h) => (
                      <th
                        key={h}
                        className="pb-2 pr-4 text-left text-xs font-medium uppercase tracking-wide text-muted-foreground"
                      >
                        {h}
                      </th>
                    ),
                  )}
                </tr>
              </thead>
              <tbody>
                {pageWords.map((w) => (
                  <WordRow key={w.id} word={w} chapterTitle={chapterTitle(w.chapter)} />
                ))}
              </tbody>
            </table>

            {totalPages > 1 && (
              <div className="mt-4 flex items-center justify-between">
                <span className="text-sm text-muted-foreground">
                  Page {page + 1} of {totalPages}
                </span>
                <div className="flex gap-2">
                  <Button
                    variant="secondary"
                    onClick={() => setPage((p) => Math.max(0, p - 1))}
                    disabled={page === 0}
                  >
                    <ChevronLeft className="size-4" /> Prev
                  </Button>
                  <Button
                    variant="secondary"
                    onClick={() => setPage((p) => Math.min(totalPages - 1, p + 1))}
                    disabled={page >= totalPages - 1}
                  >
                    Next <ChevronRight className="size-4" />
                  </Button>
                </div>
              </div>
            )}
          </>
        )}
      </div>
    </div>
  )
}
