import { useQuery } from "@tanstack/react-query"
import { Link } from "react-router-dom"
import {
  CalendarClock,
  GraduationCap,
  Repeat,
  BookMarked,
  BookOpen,
  NotebookPen,
} from "lucide-react"

import { fetchStats, fetchActivity } from "@/api/stats"
import { fetchBooks } from "@/api/books"
import { fetchDueCounts } from "@/api/vocabulary"
import { StatCard } from "@/components/ui/StatCard"
import { Button } from "@/components/ui/button"
import { ReviewActivityChart } from "@/components/charts/ReviewActivityChart"

export default function Dashboard() {
  const { data: stats } = useQuery({ queryKey: ["stats"], queryFn: fetchStats })
  const { data: books } = useQuery({ queryKey: ["books"], queryFn: fetchBooks })
  const { data: counts } = useQuery({
    queryKey: ["due-counts"],
    queryFn: fetchDueCounts,
  })
  const { data: activity } = useQuery({
    queryKey: ["activity"],
    queryFn: fetchActivity,
  })

  const dueToday = stats?.due_today ?? 0

  return (
    <div>
      <div className="flex items-center justify-between">
        <h1 className="text-2xl font-semibold tracking-tight">Dashboard</h1>
        {dueToday > 0 ? (
          <Button asChild>
            <Link to="/review">Start Review · {dueToday} due</Link>
          </Button>
        ) : (
          <Button disabled>Nothing due</Button>
        )}
      </div>

      {/* Stat cards */}
      <div className="mt-6 grid grid-cols-2 gap-4 sm:grid-cols-3">
        <StatCard icon={CalendarClock} value={dueToday} label="Due today" accent={dueToday > 0} />
        <StatCard icon={GraduationCap} value={stats?.learned_total ?? 0} label="Words learned" />
        <StatCard icon={Repeat} value={stats?.reviewed_today ?? 0} label="Reviewed today" />
        <StatCard icon={BookMarked} value={stats?.total_words ?? 0} label="Total words" />
        <StatCard icon={BookOpen} value={stats?.total_grammar_rules ?? 0} label="Grammar rules" />
        <StatCard icon={NotebookPen} value={stats?.total_exercises ?? 0} label="Exercises" />
      </div>

      {/* Activity chart */}
      {activity && activity.length > 0 && (
        <div className="mt-8">
          <ReviewActivityChart data={activity} />
        </div>
      )}

      {/* Chapters with per-chapter word counts */}
      <div className="mt-10">
        <h2 className="text-xs font-semibold uppercase tracking-wide text-muted-foreground">
          Chapters
        </h2>
        <div className="mt-3 flex flex-col gap-4">
          {books?.map((book) => (
            <div key={book.id}>
              <h3 className="mb-2 text-sm font-medium text-foreground">
                {book.title}
              </h3>
              <div className="overflow-hidden rounded-xl border border-border">
                {book.chapters.map((c, i) => {
                  const due = counts?.per_chapter[c.id] ?? 0
                  return (
                    <div
                      key={c.id}
                      className={
                        "flex items-center justify-between bg-surface px-4 py-2.5 text-sm" +
                        (i > 0 ? " border-t border-border" : "")
                      }
                    >
                      <span className="text-foreground">{c.title}</span>
                      {due > 0 ? (
                        <Link
                          to="/review"
                          className="rounded-full bg-accent/10 px-2 py-0.5 text-xs font-medium text-accent hover:bg-accent/20"
                        >
                          {due} due
                        </Link>
                      ) : (
                        <span className="text-xs text-muted-foreground">
                          done
                        </span>
                      )}
                    </div>
                  )
                })}
              </div>
            </div>
          ))}
        </div>
      </div>
    </div>
  )
}
