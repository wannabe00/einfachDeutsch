import type { ActivityDay } from "@/types"

/** Reviews over the last 7 days as bars, plus the level's path progress. */
export function ActivityCard({
  activity,
  level,
  lessonsDone,
  lessonsTotal,
}: {
  activity: ActivityDay[]
  level: string
  lessonsDone: number
  lessonsTotal: number
}) {
  const total = activity.reduce((sum, d) => sum + d.count, 0)
  const max = Math.max(1, ...activity.map((d) => d.count))
  const pathPct = lessonsTotal > 0 ? (lessonsDone / lessonsTotal) * 100 : 0
  const weekday = (iso: string) =>
    new Date(`${iso}T00:00:00`).toLocaleDateString("en-US", { weekday: "short" })

  return (
    <section className="d-card p-5 sm:p-6" aria-label="Activity">
      <div className="flex items-start justify-between gap-4">
        <div>
          <p className="d-kicker">Last 7 days</p>
          <p className="d-num mt-0.5 text-[28px] leading-tight">
            {total} {total === 1 ? "review" : "reviews"}
          </p>
        </div>
        {lessonsTotal > 0 && (
          <div className="text-right">
            <p className="d-kicker">{level} path</p>
            <p className="d-num mt-0.5 text-[28px] leading-tight">
              {lessonsDone}/{lessonsTotal}
            </p>
          </div>
        )}
      </div>

      {lessonsTotal > 0 && (
        <div
          className="mt-3.5 h-2 overflow-hidden rounded bg-[var(--d-fill)]"
          role="progressbar"
          aria-label={`${level} path progress`}
          aria-valuemin={0}
          aria-valuemax={100}
          aria-valuenow={Math.round(pathPct)}
        >
          <i className="block h-full rounded bg-[var(--d-red)]" style={{ width: `${pathPct}%` }} />
        </div>
      )}

      <div className="mt-5 flex h-36 items-end gap-2 sm:gap-3">
        {activity.map((d, i) => {
          const today = i === activity.length - 1
          return (
            <div key={d.date} className="flex h-full flex-1 flex-col items-center justify-end gap-2">
              <span className="text-xs font-semibold tabular-nums text-[var(--d-muted)]">
                {d.count > 0 ? d.count : ""}
              </span>
              <div className="flex w-full flex-1 items-end justify-center">
                <i
                  className={`d-grow block w-full max-w-11 rounded-lg ${today ? "bg-[var(--d-red)]" : "bg-[var(--d-fill)]"}`}
                  style={{ height: `${Math.max((d.count / max) * 100, 3)}%` }}
                  title={`${d.count} reviews`}
                />
              </div>
              <span className="text-xs font-semibold text-[var(--d-muted)]">{weekday(d.date)}</span>
            </div>
          )
        })}
      </div>
    </section>
  )
}
