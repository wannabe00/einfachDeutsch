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

const GRID = "grid grid-cols-2 gap-2.5 sm:grid-cols-3"

export function ChapterButtons({
  books,
  selected,
  onSelect,
  includeAll = true,
  badge,
}: ChapterButtonsProps) {
  const tile = (active: boolean) =>
    cn(
      "flex min-h-[78px] flex-col gap-0.5 rounded-xl border p-3 text-left transition-colors",
      active
        ? "border-accent bg-accent text-accent-foreground"
        : "border-border bg-surface text-foreground hover:bg-surface-2",
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
          <p className="mb-2 text-xs font-semibold uppercase tracking-wide text-muted-foreground">
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
                  <span className="text-sm font-semibold leading-tight">
                    Lektion {c.number}
                  </span>
                  <span className="line-clamp-2 text-xs opacity-70">{c.title}</span>
                  {b !== undefined && b !== 0 ? (
                    <span className="mt-auto pt-1 text-xs">
                      <span className="font-bold">{b}</span> due
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
