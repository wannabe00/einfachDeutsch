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

  if (!article) return null

  const colorClass =
    article === "der"
      ? "bg-article-der/15 text-article-der"
      : article === "die"
        ? "bg-article-die/15 text-article-die"
        : article === "das"
          ? "bg-article-das/15 text-article-das"
          : "bg-muted text-muted-foreground"

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
