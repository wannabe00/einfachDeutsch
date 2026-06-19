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

const GRID = "grid grid-cols-2 gap-2.5 sm:grid-cols-3 md:grid-cols-4"

export function ChapterButtons({
  books,
  selected,
  onSelect,
  includeAll = true,
  badge,
}: ChapterButtonsProps) {
  const tile = (active: boolean) =>
    cn(
      "flex aspect-square flex-col justify-between rounded-xl border p-3 text-left transition-colors",
      active
        ? "border-accent bg-accent text-accent-foreground shadow-sm"
        : "border-border bg-surface text-foreground hover:border-accent hover:shadow-sm",
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
            <span className="text-xs opacity-70">Everything</span>
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
                  <span className="line-clamp-3 text-sm font-semibold leading-tight">
                    {c.title.replace(/ —.*/, "")}
                  </span>
                  {b !== undefined && b !== 0 ? (
                    <span className="leading-none">
                      <span className="text-xl font-bold">{b}</span>{" "}
                      <span className="text-xs opacity-70">due</span>
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
