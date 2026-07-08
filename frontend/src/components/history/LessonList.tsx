import { Check, Landmark } from "lucide-react"

import type { HistoryLessonSummary } from "@/types"

/** Era-grouped grid of history lessons; a completed lesson shows a check. */
export function LessonList({
  lessons,
  onOpen,
}: {
  lessons: HistoryLessonSummary[]
  onOpen: (id: number) => void
}) {
  const eras: string[] = []
  for (const l of lessons) if (!eras.includes(l.era)) eras.push(l.era)

  return (
    <div className="mt-6 flex flex-col gap-8">
      {eras.map((era) => (
        <section key={era}>
          <h2 className="mb-3 text-xs font-semibold uppercase tracking-wide text-muted-foreground">
            {era}
          </h2>
          <div className="grid gap-4 sm:grid-cols-2">
            {lessons
              .filter((l) => l.era === era)
              .map((l) => (
                <button
                  key={l.id}
                  onClick={() => onOpen(l.id)}
                  className="group flex items-center justify-between gap-3 rounded-xl border border-border bg-surface p-5 text-left shadow-sm transition-all hover:border-accent hover:shadow-md"
                >
                  <div className="flex items-center gap-3">
                    <div className="flex size-9 items-center justify-center rounded-lg bg-accent/10 text-accent">
                      <Landmark className="size-5" />
                    </div>
                    <span className="font-semibold text-foreground">{l.title}</span>
                  </div>
                  {l.completed && (
                    <Check className="size-5 shrink-0 text-[hsl(var(--success))]" />
                  )}
                </button>
              ))}
          </div>
        </section>
      ))}
    </div>
  )
}
