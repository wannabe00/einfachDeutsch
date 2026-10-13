import { useQuery } from "@tanstack/react-query"

import { useAuth } from "@/contexts/AuthContext"
import { fetchGamification } from "@/api/curriculum"
import { fetchStats } from "@/api/stats"
import { StatCard } from "@/components/ui/StatCard"

/** Avatar, name, level and a few headline numbers, shown at the top of Settings. */
export function ProfileHeader() {
  const { user } = useAuth()
  const { data: game } = useQuery({
    queryKey: ["gamification"],
    queryFn: fetchGamification,
    enabled: !!user,
  })
  const { data: stats } = useQuery({ queryKey: ["stats"], queryFn: fetchStats, enabled: !!user })

  if (!user) return null

  const fullName = [user.first_name, user.last_name].filter(Boolean).join(" ")
  const displayName = fullName || user.username || "Learner"
  const initial = (user.username || user.first_name || "?").charAt(0).toUpperCase()

  return (
    <section className="flex flex-col gap-6 rounded-xl border border-border bg-surface p-6 sm:flex-row sm:items-center">
      <div className="flex min-w-0 items-center gap-4">
        <div className="flex size-16 shrink-0 items-center justify-center overflow-hidden rounded-full bg-muted text-2xl font-bold">
          {user.avatar_url ? (
            <img src={user.avatar_url} alt="" className="size-full object-cover" />
          ) : (
            initial
          )}
        </div>
        <div className="min-w-0">
          <h2 className="truncate text-xl font-bold sm:text-2xl">{displayName}</h2>
          <div className="mt-1 flex flex-wrap items-center gap-2 text-sm text-muted-foreground">
            {user.username && <span className="truncate">@{user.username}</span>}
            <span className="rounded-md border border-border px-1.5 py-0.5 text-xs font-semibold text-foreground">
              {user.cefr_level}
            </span>
          </div>
        </div>
      </div>

      <div className="grid flex-1 grid-cols-2 gap-3 sm:ml-auto sm:max-w-md sm:grid-cols-4">
        <StatCard value={game?.total_xp ?? 0} label="XP" className="bg-background" />
        <StatCard value={game?.crowns ?? 0} label="Crowns" className="bg-background" />
        <StatCard value={game?.lessons_completed ?? 0} label="Lessons" className="bg-background" />
        <StatCard value={stats?.words_learned ?? 0} label="Words" className="bg-background" />
      </div>
    </section>
  )
}
