import type { ActivityDay, StreakStatus } from "@/types"
import { StreakFlame } from "@/components/lektion/StreakFlame"
import { streakMilestone } from "@/components/lektion/streak"

const DAYS = ["Sun", "Mon", "Tue", "Wed", "Thu", "Fri", "Sat"]
/** The flame is earned: it only appears from this many days on. */
const FLAME_FROM = 3

/*
 * Current streak and the last 7 days. No streak: an invitation to start one.
 * 1-2 days: just the number and how far the flame is. 3+ days: the animated
 * flame, plus a milestone badge at a week, a month, 100 days and a year.
 */
export function StreakCard({ streak, activity }: { streak: StreakStatus; activity: ActivityDay[] }) {
  // Parse YYYY-MM-DD as local time so the weekday is correct.
  const weekday = (iso: string) => DAYS[new Date(`${iso}T00:00:00`).getDay()]
  const days = streak.current_streak
  const milestone = streakMilestone(days)

  return (
    <section className="d-card flex flex-col justify-between gap-4 p-5 sm:p-6" aria-label="Streak">
      <div className="flex items-center justify-between gap-2">
        <p className="d-kicker">Streak</p>
        {milestone && (
          <span className="rounded-full bg-[var(--d-red-soft)] px-2.5 py-1 text-xs font-semibold text-[var(--d-red)]">
            {milestone}
          </span>
        )}
      </div>

      {days === 0 ? (
        <div>
          <p className="text-[22px] font-bold leading-tight">Start a streak today</p>
          <p className="mt-1 text-sm text-[var(--d-muted)]">
            Finish a lesson or a review to count today.
          </p>
        </div>
      ) : (
        <div className="flex items-end gap-3">
          {days >= FLAME_FROM && <StreakFlame size={52} className="-mb-1 shrink-0" />}
          <span className="d-num text-[56px] leading-none">{days}</span>
          <span className="pb-1.5 text-[var(--d-muted)]">{days === 1 ? "day" : "days"}</span>
        </div>
      )}

      {activity.length > 0 && (
        <div className="flex gap-1.5" aria-label="Days you reviewed this week">
          {activity.map((d) => (
            <span key={d.date} className="flex-1 text-center text-[11px] font-semibold text-[var(--d-muted)]">
              <i
                className={`mb-1 block h-2 rounded ${d.count > 0 ? "bg-[var(--d-red)]" : "bg-[var(--d-fill)]"}`}
              />
              {weekday(d.date).slice(0, 2)}
            </span>
          ))}
        </div>
      )}

      <p className="text-[13px] text-[var(--d-muted)]">
        {days > 0 && days < FLAME_FROM
          ? `${FLAME_FROM - days} more ${FLAME_FROM - days === 1 ? "day" : "days"} to light the flame · `
          : ""}
        {streak.longest_streak > days && `Best ${streak.longest_streak} · `}
        {streak.freeze_tokens} {streak.freeze_tokens === 1 ? "freeze" : "freezes"} save a missed day
      </p>
    </section>
  )
}
