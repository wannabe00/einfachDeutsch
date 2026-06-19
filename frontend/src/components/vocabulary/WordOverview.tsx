import type { Word } from "@/types"
import { ArticleBadge } from "./ArticleBadge"

interface WordOverviewProps {
  words: Word[]
}

function stage(w: Word): "new" | "learning" | "review" | "learned" {
  const p = w.progress
  if (!p || p.repetitions === 0) return "new"
  if (p.interval <= 6) return "learning"
  if (p.interval <= 21) return "review"
  return "learned"
}

export function WordOverview({ words }: WordOverviewProps) {
  const counts = { new: 0, learning: 0, review: 0, learned: 0 }
  let correct = 0
  let wrong = 0
  for (const w of words) {
    counts[stage(w)] += 1
    correct += w.progress?.times_correct ?? 0
    wrong += w.progress?.times_wrong ?? 0
  }
  const answered = correct + wrong
  const accuracy = answered ? Math.round((correct / answered) * 100) : null

  const mostMissed = [...words]
    .filter((w) => (w.progress?.times_wrong ?? 0) > 0)
    .sort((a, b) => (b.progress?.times_wrong ?? 0) - (a.progress?.times_wrong ?? 0))
    .slice(0, 5)

  const chips = [
    { label: "New", value: counts.new, color: "text-muted-foreground" },
    { label: "Learning", value: counts.learning, color: "text-[hsl(var(--article-das))]" },
    { label: "Review", value: counts.review, color: "text-[hsl(var(--article-der))]" },
    { label: "Learned", value: counts.learned, color: "text-[hsl(var(--success))]" },
  ]

  return (
    <div className="rounded-xl border border-border bg-surface p-5">
      <div className="flex flex-wrap items-end justify-between gap-4">
        <div className="grid grid-cols-4 gap-5">
          {chips.map((c) => (
            <div key={c.label} className="flex flex-col">
              <span className={`text-2xl font-bold ${c.color}`}>{c.value}</span>
              <span className="text-xs text-muted-foreground">{c.label}</span>
            </div>
          ))}
        </div>
        <div className="flex gap-5">
          <div className="flex flex-col">
            <span className="text-2xl font-bold text-foreground">
              {accuracy === null ? "—" : `${accuracy}%`}
            </span>
            <span className="text-xs text-muted-foreground">Accuracy</span>
          </div>
          <div className="flex flex-col">
            <span className="text-2xl font-bold text-[hsl(var(--danger))]">{wrong}</span>
            <span className="text-xs text-muted-foreground">Mistakes</span>
          </div>
          <div className="flex flex-col">
            <span className="text-2xl font-bold text-[hsl(var(--success))]">{correct}</span>
            <span className="text-xs text-muted-foreground">Correct</span>
          </div>
        </div>
      </div>

      {mostMissed.length > 0 && (
        <div className="mt-4 border-t border-border pt-4">
          <p className="mb-2 text-xs font-semibold uppercase tracking-wide text-muted-foreground">
            Most missed
          </p>
          <div className="flex flex-wrap gap-2">
            {mostMissed.map((w) => (
              <span
                key={w.id}
                className="inline-flex items-center gap-1.5 rounded-full border border-border bg-background px-2.5 py-1 text-sm"
                title={`${w.english} · missed ${w.progress?.times_wrong}×`}
              >
                <ArticleBadge german={w.german} />
                <span className="font-medium text-foreground">{w.german}</span>
                <span className="text-xs text-[hsl(var(--danger))]">
                  ×{w.progress?.times_wrong}
                </span>
              </span>
            ))}
          </div>
        </div>
      )}
    </div>
  )
}
