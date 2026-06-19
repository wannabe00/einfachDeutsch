import ReactMarkdown from "react-markdown"
import remarkGfm from "remark-gfm"

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
    <article className="rounded-xl border border-border bg-surface p-5 shadow-sm transition-shadow hover:shadow-md">
      <header className="mb-3 flex items-start justify-between gap-3">
        <h3 className="text-base font-semibold tracking-tight text-foreground">
          {rule.title}
        </h3>
        <span className="shrink-0 rounded-full bg-muted px-2.5 py-0.5 text-xs font-medium text-muted-foreground">
          {grammarCategoryLabel(rule.category)}
        </span>
      </header>

      <div
        className="prose-grammar text-sm leading-relaxed text-foreground
          [&_code]:rounded [&_code]:bg-background [&_code]:px-1 [&_code]:py-0.5 [&_code]:font-mono [&_code]:text-[0.85em]
          [&_p]:my-2
          [&_strong]:font-semibold [&_strong]:text-foreground
          [&_table]:my-3 [&_table]:w-full [&_table]:border-collapse
          [&_th]:border [&_th]:border-border [&_th]:bg-background [&_th]:px-2 [&_th]:py-1 [&_th]:text-left [&_th]:font-medium
          [&_td]:border [&_td]:border-border [&_td]:px-2 [&_td]:py-1
          [&_ul]:my-2 [&_ul]:list-disc [&_ul]:pl-5 [&_li]:my-1"
      >
        <ReactMarkdown remarkPlugins={[remarkGfm]}>{rule.content}</ReactMarkdown>
      </div>

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
