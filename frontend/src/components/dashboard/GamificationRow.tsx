import { useQuery } from "@tanstack/react-query"
import { Crown, GraduationCap, Star, Zap } from "lucide-react"

import { fetchGamification } from "@/api/curriculum"
import { useAuth } from "@/contexts/AuthContext"

/*
 * XP / crowns / lessons summary for the Dashboard (Phase 23.15). Pure read-out
 * of what the lesson player already awards — no new data. The path/exam are
 * per-user, so this only renders for a signed-in user.
 */
export function GamificationRow() {
  const { user } = useAuth()
  const { data } = useQuery({
    queryKey: ["gamification"],
    queryFn: fetchGamification,
    enabled: !!user,
  })

  if (!user || !data) return null

  return (
    <div className="mt-4 grid grid-cols-2 gap-4 sm:grid-cols-4">
      <Tile icon={Zap} label="Total XP" value={data.total_xp} accent="hsl(var(--brand))" />
      <Tile
        icon={Crown}
        label={data.crowns === 1 ? "Crown" : "Crowns"}
        value={data.crowns}
        accent="hsl(var(--section-4))"
      />
      <Tile
        icon={GraduationCap}
        label="Lessons done"
        value={data.lessons_completed}
        accent="hsl(var(--section-2))"
      />
      <Tile
        icon={Star}
        label={`${data.level} progress`}
        value={`${data.level_lessons_done}/${data.level_lessons_total}`}
        accent="hsl(var(--section-3))"
      />
    </div>
  )
}

function Tile({
  icon: Icon,
  label,
  value,
  accent,
}: {
  icon: typeof Zap
  label: string
  value: number | string
  accent: string
}) {
  return (
    <div className="flex items-center gap-3 rounded-xl border border-white/10 bg-gradient-to-b from-surface-2 to-surface p-4 shadow-lg shadow-black/30">
      <span
        className="flex size-9 shrink-0 items-center justify-center rounded-lg bg-white/5"
        style={{ color: accent }}
      >
        <Icon className="size-5" />
      </span>
      <div className="min-w-0">
        <p className="text-lg font-bold leading-none">{value}</p>
        <p className="mt-1 truncate text-xs text-muted-foreground">{label}</p>
      </div>
    </div>
  )
}
