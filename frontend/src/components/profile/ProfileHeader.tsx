import { useQuery } from "@tanstack/react-query"

import { useAuth } from "@/contexts/AuthContext"
import { fetchGamification } from "@/api/curriculum"
import { fetchStats } from "@/api/stats"

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
    <section className="flex flex-col gap-6 rounded-[24px] bg-surface p-6 shadow-card sm:p-7 lg:flex-row lg:items-center">
      <div className="flex min-w-0 items-center gap-4">
        <div className="flex size-20 shrink-0 items-center justify-center overflow-hidden rounded-full bg-primary text-3xl font-extrabold text-primary-foreground ring-4 ring-primary/15">
          {user.avatar_url ? (
            <img src={user.avatar_url} alt="" className="size-full object-cover" />
          ) : (
            initial
          )}
        </div>
        <div className="min-w-0">
          <h1 className="truncate text-2xl font-extrabold sm:text-3xl">{displayName}</h1>
          <div className="mt-1 flex flex-wrap items-center gap-2 text-muted-foreground">
            {user.username && <span className="truncate">@{user.username}</span>}
            <span className="rounded-full bg-primary/10 px-2.5 py-0.5 text-xs font-bold text-primary">
              Level {user.cefr_level}
            </span>
          </div>
        </div>
      </div>

      <dl className="grid flex-1 grid-cols-4 gap-2 rounded-2xl bg-surface-2/70 p-3 lg:ml-auto lg:max-w-md">
        {[
          { label: "XP", value: game?.total_xp ?? 0 },
          { label: "Crowns", value: game?.crowns ?? 0 },
          { label: "Lessons", value: game?.lessons_completed ?? 0 },
          { label: "Words", value: stats?.words_learned ?? 0 },
        ].map((it) => (
          <div key={it.label} className="flex flex-col items-center text-center">
            <dd className="font-grotesk text-xl font-extrabold tabular-nums sm:text-2xl">
              {it.value.toLocaleString("en-US")}
            </dd>
            <dt className="text-xs text-muted-foreground">{it.label}</dt>
          </div>
        ))}
      </dl>
    </section>
  )
}
