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

export function ChapterButtons({
  books,
  selected,
  onSelect,
  includeAll = true,
  badge,
}: ChapterButtonsProps) {
  const pill = (active: boolean) =>
    cn(
      "inline-flex items-center gap-1.5 rounded-full border px-3 py-1.5 text-sm font-medium transition-colors",
      active
        ? "border-accent bg-accent text-accent-foreground"
        : "border-border bg-surface text-foreground hover:border-accent",
    )

  return (
    <div className="flex flex-col gap-3">
      {includeAll && (
        <div>
          <button onClick={() => onSelect("all")} className={pill(selected === "all")}>
            All chapters
          </button>
        </div>
      )}
      {books.map((book) => (
        <div key={book.id}>
          <p className="mb-1.5 text-xs font-semibold uppercase tracking-wide text-muted-foreground">
            {book.title}
          </p>
          <div className="flex flex-wrap gap-2">
            {book.chapters.map((c) => {
              const b = badge?.(c.id)
              return (
                <button
                  key={c.id}
                  onClick={() => onSelect(c.id)}
                  className={pill(selected === c.id)}
                  title={c.title}
                >
                  {c.title.replace(/ —.*/, "")}
                  {b !== undefined && b !== 0 && (
                    <span
                      className={cn(
                        "rounded-full px-1.5 text-xs",
                        selected === c.id
                          ? "bg-white/20"
                          : "bg-muted text-muted-foreground",
                      )}
                    >
                      {b}
                    </span>
                  )}
                </button>
              )
            })}
          </div>
        </div>
      ))}
    </div>
  )
}
