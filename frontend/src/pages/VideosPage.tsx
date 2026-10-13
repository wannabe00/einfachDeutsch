import { useQuery } from "@tanstack/react-query"
import { ExternalLink, Lock } from "lucide-react"

import { fetchVideoSuggestions } from "@/api/videos"
import type { CEFRLevel, ShowSuggestion } from "@/types"
import { PageHeader } from "@/components/layout/PageHeader"
import { Card } from "@/components/ui/card"
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

function SuggestionCard({ suggestion: s }: { suggestion: ShowSuggestion }) {
  return (
    <Card className="flex h-full flex-col overflow-hidden">
      <a href={s.url} target="_blank" rel="noopener noreferrer" className="block aspect-video">
        <SourceArt platform={s.platform} imageUrl={s.image_url || undefined} title={s.title} />
      </a>
      <div className="flex flex-1 flex-col gap-3 p-5">
        <div>
          <h3 className="text-lg font-bold">{s.title}</h3>
          <p className="mt-1 text-xs text-muted-foreground">
            {[s.platform, s.cefr_level, s.cost].filter(Boolean).join(" · ")}
          </p>
        </div>
        <p className="text-sm">{s.description}</p>
        <dl className="grid gap-1 text-sm">
          {s.audience && (
            <div>
              <dt className="inline font-medium">For: </dt>
              <dd className="inline text-muted-foreground">{s.audience}</dd>
            </div>
          )}
          {s.format && (
            <div>
              <dt className="inline font-medium">Format: </dt>
              <dd className="inline text-muted-foreground">{s.format}</dd>
            </div>
          )}
        </dl>
        {s.tips.length > 0 && (
          <div>
            <p className="text-sm font-medium">How to learn with it</p>
            <ul className="mt-1 list-disc space-y-0.5 pl-5 text-sm text-muted-foreground">
              {s.tips.map((tip) => (
                <li key={tip}>{tip}</li>
              ))}
            </ul>
          </div>
        )}
        <a
          href={s.url}
          target="_blank"
          rel="noopener noreferrer"
          className="mt-auto inline-flex w-fit items-center gap-1.5 pt-1 text-sm font-medium text-foreground underline underline-offset-4 hover:text-primary"
        >
          Open on {s.platform} <ExternalLink className="size-3.5" />
        </a>
      </div>
    </Card>
  )
}
