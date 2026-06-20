import { useQuery } from "@tanstack/react-query"
import { CalendarCheck, CalendarClock, Flame, Snowflake } from "lucide-react"

import { useAuth } from "@/contexts/AuthContext"
import { fetchStreak } from "@/api/leveling"

const DAYS = ["Sun", "Mon", "Tue", "Wed", "Thu", "Fri", "Sat"]

export function StreakBanner() {
  const { user } = useAuth()
  const { data } = useQuery({
    queryKey: ["streak"],
    queryFn: fetchStreak,
    enabled: !!user,
  })

  if (!user || !data) return null

  // Parse the YYYY-MM-DD as local time so the weekday is correct.
  const next = new Date(`${data.next_unlock_date}T00:00:00`)
  const nextDay = DAYS[next.getDay()]

  return (
    <div className="mt-6 flex flex-wrap items-center gap-x-6 gap-y-3 rounded-xl border border-border bg-surface p-4">
      <div className="flex items-center gap-2">
        <Flame className="size-5 text-[hsl(var(--article-die))]" aria-hidden="true" />
        <span className="text-lg font-semibold">{data.current_streak}</span>
        <span className="text-sm text-muted-foreground">
          day streak{data.longest_streak > data.current_streak && (
            <span className="ml-1 opacity-70">· best {data.longest_streak}</span>
          )}
        </span>
      </div>

      <div className="flex items-center gap-2">
        <Snowflake className="size-5 text-accent" aria-hidden="true" />
        <span className="font-medium">{data.freeze_tokens}</span>
        <span className="text-sm text-muted-foreground">
          {data.freeze_tokens === 1 ? "freeze" : "freezes"}
        </span>
      </div>

      <div className="ml-auto flex items-center gap-2 text-sm">
        {data.today_is_unlock_day ? (
          <>
            <CalendarCheck
              className="size-4 text-[hsl(var(--success))]"
              aria-hidden="true"
            />
            <span className="text-foreground">New lesson available today</span>
          </>
        ) : (
          <>
            <CalendarClock className="size-4 text-muted-foreground" aria-hidden="true" />
            <span className="text-muted-foreground">Next new lesson: {nextDay}</span>
          </>
        )}
      </div>
    </div>
  )
}
