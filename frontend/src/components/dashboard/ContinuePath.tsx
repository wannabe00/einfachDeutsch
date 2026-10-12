import { useQuery } from "@tanstack/react-query"

import { fetchPath } from "@/api/curriculum"
import { useAuth } from "@/contexts/AuthContext"
import { resolveAccent } from "@/lib/sections"
import { NextUp } from "@/components/path/NextUp"

/*
 * "Continue where you left off" on the Dashboard. Uses the path's `next_up` and
 * links to the unit that holds that lesson. Renders nothing when there's no next
 * lesson (all caught up, or no path for this level yet).
 */
export function ContinuePath() {
  const { user } = useAuth()
  const { data } = useQuery({ queryKey: ["path"], queryFn: fetchPath, enabled: !!user })

  const next = data?.next_up
  if (!user || !next) return null

  const unitId = data.units.find((u) => u.lessons.some((l) => l.id === next.lesson_id))?.id

  return (
    <NextUp
      kicker="Continue learning"
      title={next.lesson_title}
      subtitle={next.unit_title}
      href={unitId ? `/path/${unitId}` : "/path"}
      accent={resolveAccent(undefined, 0)}
    />
  )
}
