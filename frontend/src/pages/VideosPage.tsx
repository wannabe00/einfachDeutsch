import { useQuery } from "@tanstack/react-query"
import { ExternalLink, Lightbulb, Lock } from "lucide-react"

import { fetchVideoSuggestions } from "@/api/videos"
import type { CEFRLevel, ShowSuggestion } from "@/types"
import { PageHeader } from "@/components/layout/PageHeader"
import { Card } from "@/components/ui/card"
import { SourceArt } from "@/components/videos/SourceArt"
import { cn } from "@/lib/utils"

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
          <div className="flex flex-col items-center px-6 py-12 text-center">
            <span className="flex size-16 items-center justify-center rounded-2xl bg-primary/10 text-primary">
              <Lock className="size-8" aria-hidden="true" />
            </span>
            <h2 className="mt-4 text-2xl font-extrabold">
              Video suggestions unlock at {data.unlock_level}
            </h2>
            <p className="mt-2 max-w-sm text-muted-foreground">
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
              <div className="mb-3 flex items-baseline gap-3 px-1">
                <h2 className="text-[22px] font-bold">{level}</h2>
                <span className="text-sm text-muted-foreground">
                  {items.length} {items.length === 1 ? "pick" : "picks"}
                </span>
              </div>
              <div className="grid gap-5 sm:grid-cols-2">
                {/* With an odd number of picks the first spans the row, so no row is half empty. */}
                {items.map((s, i) => (
                  <SuggestionCard key={s.id} suggestion={s} featured={items.length % 2 === 1 && i === 0} />
                ))}
              </div>
            </section>
          )
        })}
    </div>
  )
}

function SuggestionCard({ suggestion: s, featured }: { suggestion: ShowSuggestion; featured: boolean }) {
  return (
    <Card
      className={cn(
        "lift flex h-full flex-col overflow-hidden rounded-[24px]",
        featured && "sm:col-span-2 sm:grid sm:grid-cols-2",
      )}
    >
      <a
        href={s.url}
        target="_blank"
        rel="noopener noreferrer"
        className={cn("relative block aspect-video overflow-hidden", featured && "sm:aspect-auto sm:h-full sm:min-h-[280px]")}
        aria-label={`Open ${s.title} on ${s.platform}`}
      >
        <SourceArt platform={s.platform} imageUrl={s.image_url || undefined} title={s.title} />
        <span className="absolute left-3 top-3 rounded-full bg-black/55 px-2.5 py-1 text-xs font-semibold text-white backdrop-blur-md">
          {s.platform}
        </span>
      </a>
      <div className="flex flex-1 flex-col gap-3 p-5 sm:p-6">
        <div>
          <h3 className="text-xl font-bold">{s.title}</h3>
          <div className="mt-2 flex flex-wrap gap-1.5">
            {[s.cefr_level, s.cost].filter(Boolean).map((tag) => (
              <span key={tag} className="rounded-full bg-surface-2 px-2.5 py-0.5 text-xs font-semibold text-muted-foreground">
                {tag}
              </span>
            ))}
          </div>
        </div>
        <p>{s.description}</p>
        <dl className="grid gap-1 text-[15px]">
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
          <div className="rounded-2xl bg-surface-2/70 p-4">
            <p className="flex items-center gap-2 text-sm font-semibold">
              <Lightbulb className="size-4 text-[hsl(var(--warning))]" aria-hidden="true" /> How to learn with it
            </p>
            <ul className="mt-1.5 list-disc space-y-1 pl-5 text-sm text-muted-foreground">
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
          className="mt-auto inline-flex h-11 w-fit items-center gap-2 rounded-full bg-surface-2 px-5 text-[15px] font-semibold transition-colors hover:bg-border"
        >
          Open on {s.platform} <ExternalLink className="size-4" aria-hidden="true" />
        </a>
      </div>
    </Card>
  )
}
