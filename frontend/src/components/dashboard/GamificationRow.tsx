import { useQuery } from "@tanstack/react-query"

import { fetchGamification } from "@/api/curriculum"
import { useAuth } from "@/contexts/AuthContext"
import { StatCard } from "@/components/ui/StatCard"

/** XP, crowns and path progress. Signed-in users only (the path is per-user). */
export function GamificationRow() {
  const { user } = useAuth()
  const { data } = useQuery({
    queryKey: ["gamification"],
    queryFn: fetchGamification,
    enabled: !!user,
  })

  if (!user || !data) return null

  return (
    <div className="mt-4 grid grid-cols-2 gap-3 sm:grid-cols-4">
      <StatCard value={data.total_xp} label="Total XP" />
      <StatCard value={data.crowns} label={data.crowns === 1 ? "Crown" : "Crowns"} />
      <StatCard value={data.lessons_completed} label="Lessons done" />
      <StatCard
        value={`${data.level_lessons_done}/${data.level_lessons_total}`}
        label={`${data.level} lessons`}
      />
    </div>
  )
}
