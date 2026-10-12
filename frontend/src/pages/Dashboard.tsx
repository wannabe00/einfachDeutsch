import { useEffect, useRef, useState } from "react"
import { useQuery } from "@tanstack/react-query"
import { Link } from "react-router-dom"

import { fetchStats, fetchActivity } from "@/api/stats"
import { useAuth } from "@/contexts/AuthContext"
import { StatCard } from "@/components/ui/StatCard"
import { Button } from "@/components/ui/button"
import { ReviewActivityChart } from "@/components/charts/ReviewActivityChart"
import { StreakBanner } from "@/components/dashboard/StreakBanner"
import { GamificationRow } from "@/components/dashboard/GamificationRow"
import { ContinuePath } from "@/components/dashboard/ContinuePath"

// Replace with an image in /public whenever you like. If it fails to load,
// the hero falls back to a plain dark surface.
const HERO_IMG =
  "https://images.unsplash.com/photo-1595867818082-083862f3d630?auto=format&fit=crop&w=2400&q=80"

const SHORTCUTS = [
  { to: "/review", label: "Review", tagline: "Your due flashcards" },
  { to: "/words", label: "Word Bank", tagline: "Browse and add vocabulary" },
  { to: "/grammar", label: "Grammar", tagline: "Rules and topics" },
  { to: "/exercises", label: "Exercises", tagline: "Practice sets" },
  { to: "/drills", label: "Drills", tagline: "Short timed games" },
  { to: "/speak", label: "Recite", tagline: "Speak and get feedback" },
  { to: "/videos", label: "Videos", tagline: "Shows for your level" },
  { to: "/history", label: "History", tagline: "Short reads on German history" },
]

export default function Dashboard() {
  const { user } = useAuth()
  const imgRef = useRef<HTMLImageElement>(null)
  const [imgOk, setImgOk] = useState(true)

  const { data: stats } = useQuery({ queryKey: ["stats"], queryFn: fetchStats })
  const { data: activity } = useQuery({ queryKey: ["activity"], queryFn: fetchActivity })

  // Slow parallax on the hero photo.
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
  const name = user?.username || user?.first_name || null
  const secondary =
    dueToday > 0
      ? { to: "/review", label: `Start review (${dueToday} due)` }
      : { to: "/words", label: "Browse the Word Bank" }

  return (
    <div className="flex flex-col gap-8">
      <section className="relative h-60 overflow-hidden rounded-xl border border-border bg-surface-2 sm:h-72">
        {imgOk && (
          <img
            ref={imgRef}
            src={HERO_IMG}
            alt="Munich"
            onError={() => setImgOk(false)}
            className="absolute inset-0 h-[140%] w-full object-cover"
          />
        )}
        {/* Darken the bottom of the photo so the text stays readable. */}
        <div className="absolute inset-0 bg-gradient-to-t from-black/80 via-black/45 to-black/25" />
        <div className="relative flex h-full flex-col justify-center px-6 text-white sm:px-10">
          <h1 className="text-2xl font-bold sm:text-3xl">
            Willkommen zurück{name ? `, ${name}` : ""}!
          </h1>
          <p className="mt-1 text-sm text-white/85">
            {dueToday > 0
              ? `You have ${dueToday} ${dueToday === 1 ? "word" : "words"} due for review.`
              : "Nothing due for review right now."}
          </p>
          <div className="mt-4 flex flex-wrap gap-3">
            <Button asChild>
              <Link to="/path">Continue your path</Link>
            </Button>
            <Button
              asChild
              variant="outline"
              className="border-white/50 bg-transparent text-white hover:bg-white/10"
            >
              <Link to={secondary.to}>{secondary.label}</Link>
            </Button>
          </div>
        </div>
      </section>

      <ContinuePath />

      <section>
        <h2 className="mb-3 text-sm font-semibold uppercase tracking-wide text-muted-foreground">
          Your progress
        </h2>
        <StreakBanner />
        <GamificationRow />
        <div className="mt-3 grid grid-cols-2 gap-3 sm:grid-cols-4">
          <StatCard value={dueToday} label="Due today" highlight={dueToday > 0} />
          <StatCard value={stats?.learned_total ?? 0} label="Words learned" />
          <StatCard value={stats?.reviewed_today ?? 0} label="Reviewed today" />
          <StatCard value={stats?.total_words ?? 0} label="Words in the bank" />
        </div>
        {activity && activity.length > 0 && (
          <div className="mt-4">
            <ReviewActivityChart data={activity} />
          </div>
        )}
      </section>

      <section>
        <h2 className="mb-3 text-sm font-semibold uppercase tracking-wide text-muted-foreground">
          Jump back in
        </h2>
        <div className="grid grid-cols-2 gap-3 sm:grid-cols-3 lg:grid-cols-4">
          {SHORTCUTS.map((s) => (
            <Link
              key={s.to}
              to={s.to}
              className="rounded-xl border border-border bg-surface p-4 transition-colors hover:bg-surface-2"
            >
              <div className="flex items-center gap-2">
                <span className="font-semibold">{s.label}</span>
                {s.to === "/review" && dueToday > 0 && (
                  <span className="rounded-full bg-primary px-2 py-0.5 text-xs font-semibold text-primary-foreground">
                    {dueToday}
                  </span>
                )}
              </div>
              <p className="mt-0.5 text-sm text-muted-foreground">{s.tagline}</p>
            </Link>
          ))}
        </div>
      </section>
    </div>
  )
}
