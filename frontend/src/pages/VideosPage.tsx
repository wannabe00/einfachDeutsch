import { useQuery } from "@tanstack/react-query"
import { ExternalLink, Lock } from "lucide-react"

import { fetchVideoSuggestions } from "@/api/videos"
import type { CEFRLevel, ShowSuggestion } from "@/types"
import { PageHeader } from "@/components/layout/PageHeader"
import { Card } from "@/components/ui/Card"
import { SourceArt } from "@/components/videos/SourceArt"

/*
 * Video suggestions, each with artwork for its source. The server applies two
 * rules: the page unlocks at VIDEO_UNLOCK_MIN_LEVEL (B1 by default), and after
 * that you still only see picks at or below your level.
 */
const LEVEL_ORDER: CEFRLevel[] = ["A1", "A2", "B1", "B2", "C1", "C2"]

export default function VideosPage() {
  const { data, isLoading } = useQuery({
    queryKey: ["video-suggestions"],
    queryFn: fetchVideoSuggestions,
  })

  return (
    <div className="flex flex-col gap-6">
      <PageHeader
        title="Videos & shows"
        subtitle="German videos, channels and shows picked for your level."
      />

      {isLoading && <p className="text-sm text-muted-foreground">Loading…</p>}

      {data && !data.unlocked && (
        <Card>
          <div className="flex flex-col items-center p-8 text-center">
            <span
              className="flex size-12 items-center justify-center rounded-xl"
              style={{ background: "hsl(var(--brand)/0.15)", color: "hsl(var(--brand))" }}
            >
              <Lock className="size-6" />
            </span>
            <h2 className="mt-4 text-xl font-bold">
              Video suggestions unlock at {data.unlock_level}
            </h2>
            <p className="mt-2 max-w-sm text-sm text-muted-foreground">
              You're at {data.current_level}. Videos open up once you reach{" "}
              {data.unlock_level}.
            </p>
          </div>
        </Card>
      )}

      {data?.unlocked &&
        LEVEL_ORDER.map((level) => {
          const items = data.suggestions.filter((s) => s.cefr_level === level)
          if (items.length === 0) return null
          return (
            <section key={level}>
              <div className="mb-3 flex items-baseline gap-3">
                <h2 className="text-xl font-bold">
                  {level}
                </h2>
                <span className="text-sm text-muted-foreground">
                  {items.length} {items.length === 1 ? "pick" : "picks"}
                </span>
              </div>
              <div className="grid gap-4 sm:grid-cols-2">
                {items.map((s) => (
                  <SuggestionCard key={s.id} suggestion={s} />
                ))}
              </div>
            </section>
          )
        })}
    </div>
  )
}

function SuggestionCard({ suggestion }: { suggestion: ShowSuggestion }) {
  return (
    <a
      href={suggestion.url}
      target="_blank"
      rel="noopener noreferrer"
      className="group block"
    >
      <Card className="h-full transition-colors group-hover:border-muted-foreground/50">
        <div className="flex h-full gap-4 p-4">
          <div className="size-20 shrink-0 overflow-hidden rounded-xl">
            <SourceArt
              platform={suggestion.platform}
              imageUrl={suggestion.image_url || undefined}
              title={suggestion.title}
            />
          </div>
          <div className="flex min-w-0 flex-col">
            <div className="flex items-center gap-1.5">
              <h3 className="truncate font-bold">{suggestion.title}</h3>
              <ExternalLink className="size-3.5 shrink-0 text-muted-foreground opacity-0 transition-opacity group-hover:opacity-100" />
            </div>
            {suggestion.platform && (
              <span className="mt-0.5 w-fit rounded-full bg-muted px-2 py-0.5 text-xs font-medium text-muted-foreground">
                {suggestion.platform}
              </span>
            )}
            <p className="mt-1.5 line-clamp-3 text-sm text-muted-foreground">
              {suggestion.description}
            </p>
          </div>
        </div>
      </Card>
    </a>
  )
}
