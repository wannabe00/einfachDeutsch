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
    <article className="rounded-xl border border-border bg-surface p-5 transition-shadow">
      <header className="mb-3 flex items-start justify-between gap-3">
        <h3 className="text-base font-semibold tracking-tight text-foreground">
          {rule.title}
        </h3>
        <span className="shrink-0 rounded-full bg-muted px-2.5 py-0.5 text-xs font-medium text-muted-foreground">
          {grammarCategoryLabel(rule.category)}
        </span>
      </header>

      <Markdown className="text-foreground">{rule.content}</Markdown>

      {examples.length > 0 && (
        <div className="mt-4 border-l-2 border-accent bg-background/60 py-2 pl-3">
          {examples.map((ex, i) => (
            <p key={i} className="text-sm font-medium text-foreground">
              {ex}
            </p>
          ))}
        </div>
      )}
    </article>
  )
}
