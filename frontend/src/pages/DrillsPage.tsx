import { useState } from "react"

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
  /** Playable without an account (a free taste of the drills). */
  guest?: boolean
}

const DRILLS: DrillDef[] = [
  {
    id: "gender",
    name: "Gender Triage",
    tag: "der · die · das",
    tagline: "Snap each noun to its article before the round runs out.",
    guest: true,
  },
  {
    id: "forge",
    name: "Blind Forge",
    tag: "no hints",
    tagline: "Type the exact German, with no options to pick from.",
  },
  {
    id: "unscramble",
    name: "Unscramble",
    tag: "rebuild",
    tagline: "The letters are jumbled. Put the word back together.",
  },
  {
    id: "flash",
    name: "Flash Recall",
    tag: "3 seconds",
    tagline: "The sentence flashes, then vanishes. Rebuild it from memory.",
  },
  {
    id: "shuffle",
    name: "Sentence Shuffle",
    tag: "reorder",
    tagline: "The sentence is scrambled. Put the words back in order.",
  },
  {
    id: "match",
    name: "Match Pairs",
    tag: "connect",
    tagline: "Link each German word to its English meaning.",
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
        description="Gender Triage is free to try. Sign in to play the others."
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

      <div className="grid gap-4 sm:grid-cols-2">
        {DRILLS.map((d) => {
          const locked = !user && !d.guest
          return (
            <button
              key={d.id}
              onClick={() => setActive(d.id)}
              className="group flex flex-col items-start gap-2 rounded-xl border border-border bg-surface p-5 text-left transition-colors hover:bg-surface-2"
            >
              <div>
                <div className="flex items-center gap-2">
                  <h2 className="text-base font-semibold text-foreground">{d.name}</h2>
                  <span className="text-xs text-muted-foreground">{d.tag}</span>
                </div>
                <p className="mt-1 text-sm text-muted-foreground">{d.tagline}</p>
              </div>
              <span className="mt-1 text-sm font-medium text-primary group-hover:underline">
                {locked ? "Needs an account" : "Play"}
              </span>
            </button>
          )
        })}
      </div>
    </div>
  )
}
