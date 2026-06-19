import { useState } from "react"
import { Shield, Hammer, Shuffle, Zap, ArrowUpDown, Link2, Lock } from "lucide-react"
import type { LucideIcon } from "lucide-react"

import { GenderTriage } from "@/components/drills/GenderTriage"
import { BlindForge } from "@/components/drills/BlindForge"
import { Unscramble } from "@/components/drills/Unscramble"
import { FlashRecall } from "@/components/drills/FlashRecall"
import { SentenceShuffle } from "@/components/drills/SentenceShuffle"
import { MatchPairs } from "@/components/drills/MatchPairs"
import { LockedFeature } from "@/components/auth/LockedFeature"
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
  codename: string
  tagline: string
  icon: LucideIcon
  /** Playable without an account (a free taste of the drills). */
  guest?: boolean
}

const DRILLS: DrillDef[] = [
  {
    id: "gender",
    name: "Gender Triage",
    codename: "der · die · das",
    tagline: "Snap each noun to its article before the round runs out.",
    icon: Shield,
    guest: true,
  },
  {
    id: "forge",
    name: "Blind Forge",
    codename: "no hints",
    tagline: "Type the exact German. No options, no mercy.",
    icon: Hammer,
  },
  {
    id: "unscramble",
    name: "Unscramble",
    codename: "rebuild",
    tagline: "The letters are jumbled. Put the word back together.",
    icon: Shuffle,
  },
  {
    id: "flash",
    name: "Flash Recall",
    codename: "3 seconds",
    tagline: "The sentence flashes, then vanishes. Rebuild it from memory.",
    icon: Zap,
  },
  {
    id: "shuffle",
    name: "Sentence Shuffle",
    codename: "reorder",
    tagline: "The sentence is scrambled. Put the words back in order.",
    icon: ArrowUpDown,
  },
  {
    id: "match",
    name: "Match Pairs",
    codename: "connect",
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
        title="This drill is members-only"
        description="Gender Triage is free to try — create a free account to unlock the rest."
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
    <div>
      <h1 className="text-2xl font-semibold tracking-tight">Drills</h1>
      <p className="mt-1 text-sm text-muted-foreground">
        Fast, focused practice built from your own words. Pick a drill.
      </p>

      <div className="mt-6 grid gap-4 sm:grid-cols-2">
        {DRILLS.map((d) => {
          const locked = !user && !d.guest
          return (
            <button
              key={d.id}
              onClick={() => setActive(d.id)}
              className="group relative flex flex-col items-start gap-3 rounded-xl border border-border bg-surface p-5 text-left shadow-sm transition-all hover:border-accent hover:shadow-md"
            >
              <div className="flex size-10 items-center justify-center rounded-lg bg-accent/10 text-accent">
                <d.icon className="size-5" />
              </div>
              <div>
                <div className="flex items-center gap-2">
                  <h2 className="text-base font-semibold text-foreground">{d.name}</h2>
                  <span className="rounded-full bg-muted px-2 py-0.5 text-xs font-medium text-muted-foreground">
                    {d.codename}
                  </span>
                </div>
                <p className="mt-1 text-sm text-muted-foreground">{d.tagline}</p>
              </div>
              <span className="mt-1 text-sm font-medium text-accent group-hover:underline">
                {locked ? "Members only" : "Play →"}
              </span>
              {locked && (
                <span
                  className="absolute right-4 top-4 text-muted-foreground"
                  title="Members only"
                >
                  <Lock className="size-4" aria-hidden="true" />
                </span>
              )}
            </button>
          )
        })}
      </div>
    </div>
  )
}
