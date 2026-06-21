import { useQuery } from "@tanstack/react-query"
import { ExternalLink, Lock, Tv } from "lucide-react"

import { fetchVideoSuggestions } from "@/api/videos"
import type { CEFRLevel, ShowSuggestion } from "@/types"

const LEVEL_ORDER: CEFRLevel[] = ["A1", "A2", "B1", "B2", "C1", "C2"]

export default function VideosPage() {
  const { data, isLoading } = useQuery({
    queryKey: ["video-suggestions"],
    queryFn: fetchVideoSuggestions,
  })

  return (
    <div>
      <h1 className="text-2xl font-semibold tracking-tight">Videos & shows</h1>
      <p className="mt-1 text-sm text-muted-foreground">
        Hand-picked German videos, channels, and shows to learn from — matched to
        your level.
      </p>

      {isLoading && (
        <p className="mt-6 text-sm text-muted-foreground">Loading…</p>
      )}

      {data && !data.unlocked && (
        <div className="mt-8 flex flex-col items-center rounded-xl border border-border bg-surface p-8 text-center">
          <div className="flex size-12 items-center justify-center rounded-full bg-accent/10 text-accent">
            <Lock className="size-6" />
          </div>
          <h2 className="mt-4 text-lg font-semibold">
            Video suggestions unlock at {data.unlock_level}
          </h2>
          <p className="mt-2 max-w-sm text-sm text-muted-foreground">
            You're at {data.current_level} — keep learning and they'll open up
            once you reach {data.unlock_level}. Reviews and lessons all count.
          </p>
        </div>
      )}

      {data && data.unlocked && (
        <div className="mt-6 flex flex-col gap-8">
          {LEVEL_ORDER.map((level) => {
            const items = data.suggestions.filter((s) => s.cefr_level === level)
            if (items.length === 0) return null
            return (
              <section key={level}>
                <h2 className="mb-3 text-xs font-semibold uppercase tracking-wide text-muted-foreground">
                  {level}
                </h2>
                <div className="grid gap-4 sm:grid-cols-2">
                  {items.map((s) => (
                    <SuggestionCard key={s.id} suggestion={s} />
                  ))}
                </div>
              </section>
            )
          })}
        </div>
      )}
    </div>
  )
}

function SuggestionCard({ suggestion }: { suggestion: ShowSuggestion }) {
  return (
    <a
      href={suggestion.url}
      target="_blank"
      rel="noopener noreferrer"
      className="group flex flex-col gap-2 rounded-xl border border-border bg-surface p-5 shadow-sm transition-all hover:border-accent hover:shadow-md"
    >
      <div className="flex items-center justify-between gap-2">
        <div className="flex size-9 items-center justify-center rounded-lg bg-accent/10 text-accent">
          <Tv className="size-5" />
        </div>
        {suggestion.platform && (
          <span className="rounded-full bg-muted px-2 py-0.5 text-xs font-medium text-muted-foreground">
            {suggestion.platform}
          </span>
        )}
      </div>
      <div className="flex items-center gap-1.5">
        <h3 className="text-base font-semibold text-foreground">
          {suggestion.title}
        </h3>
        <ExternalLink className="size-3.5 text-muted-foreground opacity-0 transition-opacity group-hover:opacity-100" />
      </div>
      <p className="text-sm text-muted-foreground">{suggestion.description}</p>
    </a>
  )
}
