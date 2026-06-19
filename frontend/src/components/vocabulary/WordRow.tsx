import { ArticleBadge } from "./ArticleBadge"
import type { Word } from "@/types"

function SrsDot({ interval, repetitions }: { interval: number; repetitions: number }) {
  const label =
    repetitions === 0
      ? "New"
      : interval <= 6
        ? "Learning"
        : interval <= 21
          ? "Review"
          : "Learned"

  const dotClass =
    repetitions === 0
      ? "bg-muted-foreground/40"
      : interval <= 6
        ? "bg-amber-400"
        : interval <= 21
          ? "bg-blue-500"
          : "bg-emerald-500"

  return (
    <span title={label} aria-label={label}>
      <span className={`inline-block size-2.5 rounded-full ${dotClass}`} />
    </span>
  )
}

function nounOnly(german: string): string {
  const parts = german.trim().split(/\s+/)
  const articles = ["der", "die", "das", "ein", "eine"]
  if (parts.length > 1 && articles.includes(parts[0].toLowerCase())) {
    return parts.slice(1).join(" ")
  }
  return german
}

interface WordRowProps {
  word: Word
  chapterTitle: string
}

export function WordRow({ word, chapterTitle }: WordRowProps) {
  return (
    <tr className="border-b border-border last:border-0">
      <td className="py-3 pr-4 text-sm text-foreground">{word.english}</td>
      <td className="py-3 pr-4">
        <span className="flex items-center gap-2">
          <ArticleBadge german={word.german} />
          <span className="text-sm font-medium text-foreground">
            {nounOnly(word.german)}
          </span>
        </span>
      </td>
      <td className="py-3 pr-4 text-sm text-muted-foreground">{chapterTitle}</td>
      <td className="py-3 pr-4 text-sm text-muted-foreground">
        {word.progress?.next_review ?? "—"}
      </td>
      <td className="py-3">
        {word.progress && (
          <SrsDot
            interval={word.progress.interval}
            repetitions={word.progress.repetitions}
          />
        )}
      </td>
    </tr>
  )
}
