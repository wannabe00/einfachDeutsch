import { useState } from "react"
import { ArrowLeftRight, Eye, Hammer, Link2, Lock, Shuffle, Tags, type LucideIcon } from "lucide-react"

import { GenderTriage } from "@/components/drills/GenderTriage"
import { BlindForge } from "@/components/drills/BlindForge"
import { Unscramble } from "@/components/drills/Unscramble"
import { FlashRecall } from "@/components/drills/FlashRecall"
import { SentenceShuffle } from "@/components/drills/SentenceShuffle"
import { MatchPairs } from "@/components/drills/MatchPairs"
import { LockedFeature } from "@/components/auth/LockedFeature"
import { PageHeader } from "@/components/layout/PageHeader"
import { useAuth } from "@/contexts/AuthContext"

type DrillId =
  | "gender"
  | "forge"
  | "unscramble"
  | "flash"
  | "shuffle"
  | "match"

interface DrillDef {
  id: DrillId
  name: string
  tag: string
  tagline: string
  icon: LucideIcon
  /** Playable without an account (a free taste of the drills). */
  guest?: boolean
}

const DRILLS: DrillDef[] = [
  {
    id: "gender",
    name: "der, die, das",
    tag: "articles",
    tagline: "Pick the right article for the nouns you've learned. Mistakes come back at the end.",
    icon: Tags,
    guest: true,
  },
  {
    id: "forge",
    name: "Blind Forge",
    tag: "no hints",
    tagline: "Type the exact German, with no options to pick from.",
    icon: Hammer,
  },
  {
    id: "unscramble",
    name: "Unscramble",
    tag: "rebuild",
    tagline: "The letters are jumbled. Put the word back together.",
    icon: Shuffle,
  },
  {
    id: "flash",
    name: "Flash Recall",
    tag: "3 seconds",
    tagline: "The sentence flashes, then vanishes. Rebuild it from memory.",
    icon: Eye,
  },
  {
    id: "shuffle",
    name: "Sentence Shuffle",
    tag: "reorder",
    tagline: "The sentence is scrambled. Put the words back in order.",
    icon: ArrowLeftRight,
  },
  {
    id: "match",
    name: "Match Pairs",
    tag: "connect",
    tagline: "Link each German word to its English meaning.",
    icon: Link2,
  },
]

export default function DrillsPage() {
  const { user } = useAuth()
  const [active, setActive] = useState<DrillId | null>(null)

  const activeDef = DRILLS.find((d) => d.id === active)
  // A guest opening a members-only drill sees it locked instead of playing.
  if (activeDef && !user && !activeDef.guest) {
    return (
      <LockedFeature
        title="This drill needs an account"
        description="der, die, das is free to try. Sign in to play the others."
      />
    )
  }

  if (active === "gender") return <GenderTriage onExit={() => setActive(null)} />
  if (active === "forge") return <BlindForge onExit={() => setActive(null)} />
  if (active === "unscramble") return <Unscramble onExit={() => setActive(null)} />
  if (active === "flash") return <FlashRecall onExit={() => setActive(null)} />
  if (active === "shuffle") return <SentenceShuffle onExit={() => setActive(null)} />
  if (active === "match") return <MatchPairs onExit={() => setActive(null)} />

  return (
    <div className="flex flex-col gap-6">
      <PageHeader
        title="Drills"
        subtitle="Short games built from your own words."
      />

      <div className="grid gap-4 sm:grid-cols-2 lg:grid-cols-3">
        {DRILLS.map((d, i) => {
          const locked = !user && !d.guest
          return (
            <button
              key={d.id}
              onClick={() => setActive(d.id)}
              className="lift flex flex-col items-start gap-4 rounded-[24px] bg-surface p-5 text-left shadow-card sm:p-6"
            >
              <span
                className="flex size-12 items-center justify-center rounded-2xl text-white"
                style={{ background: `hsl(var(--section-${(i % 6) + 1}))` }}
              >
                <d.icon className="size-6" aria-hidden="true" />
              </span>
              <span className="flex-1">
                <span className="flex flex-wrap items-center gap-2">
                  <span className="text-lg font-bold text-foreground">{d.name}</span>
                  <span className="rounded-full bg-surface-2 px-2.5 py-0.5 text-xs font-semibold text-muted-foreground">
                    {d.tag}
                  </span>
                </span>
                <span className="mt-1 block text-muted-foreground">{d.tagline}</span>
              </span>
              <span className="inline-flex items-center gap-1.5 text-[15px] font-semibold text-primary">
                {locked ? (
                  <>
                    <Lock className="size-4" aria-hidden="true" /> Needs an account
                  </>
                ) : (
                  "Play"
                )}
              </span>
            </button>
          )
        })}
      </div>
    </div>
  )
}
