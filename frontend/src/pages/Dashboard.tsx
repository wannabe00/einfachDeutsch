import { useEffect, useRef, useState } from "react"
import { useQuery } from "@tanstack/react-query"
import { Link } from "react-router-dom"
import {
  BookMarked,
  BookOpen,
  CalendarClock,
  GraduationCap,
  Landmark,
  type LucideIcon,
  Mic,
  NotebookPen,
  Repeat,
  Sparkles,
  Swords,
  Tv,
} from "lucide-react"

import { fetchStats, fetchActivity } from "@/api/stats"
import { useAuth } from "@/contexts/AuthContext"
import { StatCard } from "@/components/ui/StatCard"
import { Button } from "@/components/ui/button"
import { ReviewActivityChart } from "@/components/charts/ReviewActivityChart"
import { StreakBanner } from "@/components/dashboard/StreakBanner"
import { GamificationRow } from "@/components/dashboard/GamificationRow"

// Swap for your own image in /public anytime; a gradient shows if it fails.
const HERO_IMG =
  "https://images.unsplash.com/photo-1595867818082-083862f3d630?auto=format&fit=crop&w=2400&q=80"

const SHORTCUTS: { to: string; label: string; tagline: string; icon: LucideIcon }[] = [
  { to: "/review", label: "Review", tagline: "Your due flashcards", icon: GraduationCap },
  { to: "/words", label: "Word Bank", tagline: "Browse & add vocab", icon: BookMarked },
  { to: "/grammar", label: "Grammar", tagline: "Rules & topics", icon: BookOpen },
  { to: "/exercises", label: "Exercises", tagline: "Practice sets", icon: NotebookPen },
  { to: "/drills", label: "Drills", tagline: "Fast focused games", icon: Swords },
  { to: "/speak", label: "Recite", tagline: "Speak & get scored", icon: Mic },
  { to: "/videos", label: "Videos", tagline: "Shows for your level", icon: Tv },
  { to: "/history", label: "History", tagline: "German history", icon: Landmark },
]

export default function Dashboard() {
  const { user } = useAuth()
  const imgRef = useRef<HTMLImageElement>(null)
  const [imgOk, setImgOk] = useState(true)

  const { data: stats } = useQuery({ queryKey: ["stats"], queryFn: fetchStats })
  const { data: activity } = useQuery({
    queryKey: ["activity"],
    queryFn: fetchActivity,
  })

  useEffect(() => {
    function onScroll() {
      if (imgRef.current) {
        imgRef.current.style.transform = `translateY(${window.scrollY * 0.3}px)`
      }
    }
    window.addEventListener("scroll", onScroll, { passive: true })
    return () => window.removeEventListener("scroll", onScroll)
  }, [])

  const dueToday = stats?.due_today ?? 0
  // Use the live username (falls back to first name); updates after the user
  // changes it in Settings, since useAuth refreshes the cached user.
  const name = user?.username || user?.first_name || null

  return (
    <div className="flex flex-col gap-8">
      {/* Hero */}
      <section className="relative h-60 overflow-hidden rounded-2xl sm:h-72">
        <div className="absolute inset-0 bg-gradient-to-br from-[#1b2a4a] via-[#24304d] to-[#3a2a4d]" />
        {imgOk && (
          <img
            ref={imgRef}
            src={HERO_IMG}
            alt="Munich"
            onError={() => setImgOk(false)}
            className="absolute inset-0 h-[140%] w-full object-cover"
          />
        )}
        <div className="absolute inset-0 bg-black/55" />
        <div className="relative flex h-full flex-col justify-center px-6 text-white sm:px-10">
          <h1 className="text-2xl font-bold tracking-tight sm:text-3xl">
            Willkommen zurück{name ? `, ${name}` : ""}!
          </h1>
          <p className="mt-1 text-sm text-white/85">
            {dueToday > 0
              ? `You have ${dueToday} ${dueToday === 1 ? "word" : "words"} due for review.`
              : "You're all caught up — keep exploring."}
          </p>
          <div className="mt-4 flex flex-wrap gap-3">
            {dueToday > 0 ? (
              <Button asChild>
                <Link to="/review">Start review · {dueToday} due</Link>
              </Button>
            ) : (
              <Button asChild variant="outline" className="border-white/40 bg-white/10 text-white hover:bg-white/20">
                <Link to="/words">Browse the Word Bank</Link>
              </Button>
            )}
          </div>
        </div>
      </section>

      {/* Progress */}
      <section>
        <h2 className="mb-3 text-sm font-semibold uppercase tracking-wide text-muted-foreground">
          Your progress
        </h2>
        <StreakBanner />
        {/* Path gamification — XP / crowns / lessons (Phase 23.15). */}
        <GamificationRow />
        <div className="mt-4 grid grid-cols-2 gap-4 sm:grid-cols-4">
          <StatCard icon={CalendarClock} value={dueToday} label="Due today" accent={dueToday > 0} />
          <StatCard icon={GraduationCap} value={stats?.learned_total ?? 0} label="Words learned" />
          <StatCard icon={Repeat} value={stats?.reviewed_today ?? 0} label="Reviewed today" />
          <StatCard icon={Sparkles} value={stats?.total_words ?? 0} label="Total words" />
        </div>
        {activity && activity.length > 0 && (
          <div className="mt-4">
            <ReviewActivityChart data={activity} />
          </div>
        )}
      </section>

      {/* Quick launch */}
      <section>
        <h2 className="mb-3 text-sm font-semibold uppercase tracking-wide text-muted-foreground">
          Jump back in
        </h2>
        <div className="grid grid-cols-2 gap-4 sm:grid-cols-3 lg:grid-cols-4">
          {SHORTCUTS.map((s) => (
            <Link
              key={s.to}
              to={s.to}
              className="group flex flex-col gap-3 rounded-xl border border-border bg-surface p-5 shadow-sm transition-all hover:border-accent hover:shadow-md"
            >
              <div className="flex size-10 items-center justify-center rounded-lg bg-accent/10 text-accent">
                <s.icon className="size-5" />
              </div>
              <div>
                <div className="flex items-center gap-2">
                  <span className="font-semibold text-foreground">{s.label}</span>
                  {s.to === "/review" && dueToday > 0 && (
                    <span className="rounded-full bg-accent px-2 py-0.5 text-xs font-semibold text-accent-foreground">
                      {dueToday}
                    </span>
                  )}
                </div>
                <p className="mt-0.5 text-sm text-muted-foreground">{s.tagline}</p>
              </div>
            </Link>
          ))}
        </div>
      </section>
    </div>
  )
}
