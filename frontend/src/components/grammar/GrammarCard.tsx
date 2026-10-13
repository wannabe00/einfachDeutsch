import { Markdown } from "@/components/ui/Markdown"

import type { GrammarRule } from "@/types"
import { grammarCategoryLabel } from "@/lib/labels"

interface GrammarCardProps {
  rule: GrammarRule
}

export function GrammarCard({ rule }: GrammarCardProps) {
  const examples = rule.example_sentences
    .split("\n")
    .map((s) => s.trim())
    .filter(Boolean)

  return (
    <article className="rounded-[24px] bg-surface p-6 shadow-card sm:p-7">
      <header className="mb-4 flex items-start justify-between gap-3">
        <h3 className="text-2xl font-extrabold text-foreground">{rule.title}</h3>
        <span className="mt-1 shrink-0 rounded-full bg-surface-2 px-3 py-1 text-xs font-semibold text-muted-foreground">
          {grammarCategoryLabel(rule.category)}
        </span>
      </header>

      <Markdown className="text-foreground">{rule.content}</Markdown>

      {examples.length > 0 && (
        <div className="mt-5 space-y-1.5 rounded-2xl bg-surface-2/70 p-4">
          <p className="mb-1 text-xs font-semibold uppercase tracking-[0.04em] text-muted-foreground">Beispiele</p>
          {examples.map((ex, i) => (
            <p key={i} className="text-[15px] font-medium text-foreground">
              {ex}
            </p>
          ))}
        </div>
      )}
    </article>
  )
}
