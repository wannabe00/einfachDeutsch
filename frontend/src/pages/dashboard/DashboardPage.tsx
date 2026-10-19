import { useQuery } from "@tanstack/react-query"
import { Link } from "react-router-dom"

import { fetchStats, fetchActivity } from "@/api/stats"
import { fetchChecks, fetchGamification, fetchPath } from "@/api/curriculum"
import { fetchStreak } from "@/api/leveling"
import { useAuth } from "@/contexts/AuthContext"
import { Hero } from "./Hero"
import { TodayRings } from "./TodayRings"
import { StreakCard } from "./StreakCard"
import { TotalsCard } from "./TotalsCard"
import { ContinueCard, ReviewLastUnitCard } from "./NextUpCards"
import { ActivityCard } from "./ActivityCard"
import "./dashboard.css"

/*
 * The signed-in home page. Everything it draws lives in src/pages/dashboard
 * (components + scoped tokens in dashboard.css), so it can be redesigned
 * without touching other pages. Direction: DESIGN.md.
 */
export default function DashboardPage() {
  const { user } = useAuth()
  const signedIn = !!user

  const { data: stats } = useQuery({ queryKey: ["stats"], queryFn: fetchStats })
  const { data: activity } = useQuery({ queryKey: ["activity"], queryFn: fetchActivity })
  const { data: game } = useQuery({
    queryKey: ["gamification"],
    queryFn: fetchGamification,
    enabled: signedIn,
  })
  const { data: streak } = useQuery({ queryKey: ["streak"], queryFn: fetchStreak, enabled: signedIn })
  const { data: path } = useQuery({ queryKey: ["path"], queryFn: fetchPath, enabled: signedIn })
  const { data: checks } = useQuery({ queryKey: ["checks"], queryFn: fetchChecks, enabled: signedIn })

  const level = game?.level ?? user?.cefr_level ?? "A1"
  const dueToday = stats?.due_today ?? 0
  const reviewedToday = stats?.reviewed_today ?? 0
  const wordsLearned = stats?.words_learned ?? 0
  const mastered = stats?.mastered_total ?? 0
  const lessonsDone = game?.level_lessons_done ?? 0
  const lessonsTotal = game?.level_lessons_total ?? 0

  const nextUp = path?.next_up ?? null
  const nextUnit = nextUp
    ? path?.units.find((u) => u.lessons.some((l) => l.id === nextUp.lesson_id))
    : undefined
  const continueHref =
    nextUp && nextUnit ? `/path/${nextUnit.id}/lesson/${nextUp.lesson_id}` : "/path"

  // The daily goal from Settings (reviews per day).
  const dailyGoal = Number(user?.preferences?.daily_goal) || 20
  const rings = [
    {
      label: "Daily goal",
      value: `${reviewedToday}/${dailyGoal}`,
      pct: Math.min(1, reviewedToday / dailyGoal),
      color: "var(--d-red)",
    },
    {
      label: `${level} lessons`,
      value: `${lessonsDone}/${lessonsTotal}`,
      pct: lessonsTotal > 0 ? lessonsDone / lessonsTotal : 0,
      color: "var(--d-u1)",
    },
    {
      label: "Words known",
      value: `${mastered}/${wordsLearned}`,
      pct: wordsLearned > 0 ? mastered / wordsLearned : 0,
      color: "var(--d-u4)",
    },
  ]

  const lastUnit = checks?.last_unit ?? null
  const nextCount = (nextUp && nextUnit ? 1 : 0) + (lastUnit ? 1 : 0)

  return (
    <div className="dash flex flex-col gap-5 sm:gap-6">
      <Hero
        name={user?.username || user?.first_name || null}
        level={level}
        lektion={nextUnit?.order ?? null}
        dueToday={dueToday}
        continueHref={continueHref}
      />

      <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-[1.3fr_1fr_1fr] lg:gap-5">
        <TodayRings rings={rings} />
        {streak && <StreakCard streak={streak} activity={activity ?? []} />}
        <TotalsCard
          className={streak ? "md:col-span-2 md:grid-cols-4 lg:col-span-1 lg:grid-cols-2" : ""}
          items={[
            { label: "Words learned", value: wordsLearned },
            { label: "Known", value: mastered },
            { label: "Total XP", value: game?.total_xp ?? 0 },
            { label: game?.crowns === 1 ? "Crown" : "Crowns", value: game?.crowns ?? 0 },
          ]}
        />
      </div>

      {nextCount > 0 && (
        <section className="flex flex-col gap-3">
          <div className="flex items-baseline justify-between">
            <h2 className="text-[22px] font-bold">Pick up where you left off</h2>
            <Link
              to="/path"
              className="py-2 text-[15px] font-semibold text-[var(--d-red)] hover:underline"
            >
              See path
            </Link>
          </div>
          <div
            className={`grid gap-4 lg:gap-5 ${nextCount === 2 ? "lg:grid-cols-[1.4fr_1fr]" : ""}`}
          >
            {nextUp && nextUnit && (
              <ContinueCard nextUp={nextUp} unit={nextUnit} href={continueHref} />
            )}
            {lastUnit && <ReviewLastUnitCard unit={lastUnit} />}
          </div>
        </section>
      )}

      {activity && activity.length > 0 && (
        <ActivityCard
          activity={activity}
          level={level}
          lessonsDone={lessonsDone}
          lessonsTotal={lessonsTotal}
        />
      )}
    </div>
  )
}
