import { cn } from "@/lib/utils"

const ARTICLES = ["der", "die", "das", "ein", "eine"] as const

function parseArticle(german: string): string | null {
  const first = german.trim().split(/\s+/)[0]?.toLowerCase()
  return ARTICLES.includes(first as (typeof ARTICLES)[number]) ? first : null
}

interface ArticleBadgeProps {
  german: string
  className?: string
}

export function ArticleBadge({ german, className }: ArticleBadgeProps) {
  const article = parseArticle(german)

  const colorClass =
    article === "der"
      ? "bg-blue-100 text-blue-700 dark:bg-blue-900/40 dark:text-blue-300"
      : article === "die"
        ? "bg-rose-100 text-rose-700 dark:bg-rose-900/40 dark:text-rose-300"
        : article === "das"
          ? "bg-amber-100 text-amber-700 dark:bg-amber-900/40 dark:text-amber-300"
          : "bg-muted text-muted-foreground"

  if (!article) return null

  return (
    <span
      className={cn(
        "inline-flex items-center rounded-full px-2 py-0.5 text-xs font-medium",
        colorClass,
        className,
      )}
    >
      {article}
    </span>
  )
}
