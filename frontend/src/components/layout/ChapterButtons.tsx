import type { Book } from "@/types"
import { cn } from "@/lib/utils"

type Selected = number | "all"

interface ChapterButtonsProps {
  books: Book[]
  selected: Selected
  onSelect: (value: Selected) => void
  includeAll?: boolean
  /** Optional per-chapter badge text (e.g. due counts). */
  badge?: (chapterId: number) => string | number | undefined
}

const GRID = "grid grid-cols-2 gap-3 sm:grid-cols-3"

export function ChapterButtons({
  books,
  selected,
  onSelect,
  includeAll = true,
  badge,
}: ChapterButtonsProps) {
  const tile = (active: boolean) =>
    cn(
      "lift flex min-h-[96px] flex-col gap-0.5 rounded-2xl p-4 text-left shadow-card",
      active ? "bg-primary text-primary-foreground" : "bg-surface text-foreground",
    )

  return (
    <div className="flex flex-col gap-4">
      {includeAll && (
        <div className={GRID}>
          <button
            onClick={() => onSelect("all")}
            className={tile(selected === "all")}
          >
            <span className="text-sm font-semibold leading-tight">
              All chapters
            </span>
            <span className="text-xs opacity-70">Every lesson</span>
          </button>
        </div>
      )}
      {books.map((book) => (
        <div key={book.id}>
          <p className="mb-2 px-1 text-[13px] font-semibold uppercase tracking-[0.04em] text-muted-foreground">
            {book.title}
          </p>
          <div className={GRID}>
            {book.chapters.map((c) => {
              const b = badge?.(c.id)
              const active = selected === c.id
              return (
                <button
                  key={c.id}
                  onClick={() => onSelect(c.id)}
                  className={tile(active)}
                  title={c.title}
                >
                  <span className="text-xs font-semibold uppercase tracking-[0.04em] opacity-70">
                    Lektion {c.number}
                  </span>
                  <span className="line-clamp-2 text-[15px] font-semibold leading-snug">{c.title}</span>
                  {b !== undefined && b !== 0 ? (
                    <span className="mt-auto w-fit rounded-full bg-primary/10 px-2 py-0.5 pt-0.5 text-xs font-semibold text-primary">
                      {b} due
                    </span>
                  ) : null}
                </button>
              )
            })}
          </div>
        </div>
      ))}
    </div>
  )
}
