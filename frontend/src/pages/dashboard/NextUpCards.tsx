import { Link } from "react-router-dom"

import type { PathNextUp, PathUnit } from "@/types"
import { LektionCover } from "@/components/lektion/LektionCover"
import { lektionColor } from "@/components/lektion/lektionColor"

/** "Continue" with the next lesson's Lektion cover. */
export function ContinueCard({
  nextUp,
  unit,
  href,
}: {
  nextUp: PathNextUp
  unit: PathUnit
  href: string
}) {
  const color = lektionColor(unit.order)
  const done = unit.lessons.filter((l) => l.state === "completed").length
  const pct = unit.lessons.length > 0 ? (done / unit.lessons.length) * 100 : 0

  return (
    <Link to={href} className="d-card d-lift flex overflow-hidden">
      <LektionCover order={unit.order} level={unit.cefr_level} className="min-h-[160px] w-[38%] shrink-0 sm:w-[42%]" />
      <div className="flex min-w-0 flex-col justify-center gap-1.5 p-4 sm:p-5">
        <p className="d-kicker" style={{ color }}>
          Continue · Lektion {unit.order}
        </p>
        <h3 className="text-lg font-bold leading-snug sm:text-[22px]">{nextUp.lesson_title}</h3>
        <p className="truncate text-sm text-[var(--d-muted)]">{unit.title}</p>
        <div
          className="mt-2.5 h-2 overflow-hidden rounded bg-[var(--d-fill)]"
          role="progressbar"
          aria-label={`Lektion ${unit.order} progress`}
          aria-valuemin={0}
          aria-valuemax={100}
          aria-valuenow={Math.round(pct)}
        >
          <i className="block h-full rounded" style={{ width: `${pct}%`, background: color }} />
        </div>
        <p className="text-xs text-[var(--d-muted)]">
          {done} of {unit.lessons.length} lessons
        </p>
      </div>
    </Link>
  )
}

/** "Review last unit": a short flashcard session over the last finished Lektion. */
export function ReviewLastUnitCard({
  unit,
  level,
  wordCount,
}: {
  unit: { order: number; title: string }
  level: string
  wordCount: number
}) {
  return (
    <Link to="/review?scope=last-unit" className="d-card d-lift flex overflow-hidden">
      <LektionCover order={unit.order} level={level} className="min-h-[160px] w-[34%] shrink-0" />
      <div className="flex min-w-0 flex-col justify-center gap-1.5 p-4 sm:p-5">
        <p className="d-kicker" style={{ color: lektionColor(unit.order) }}>
          Review last unit
        </p>
        <h3 className="text-lg font-bold leading-snug">
          Lektion {unit.order}: {unit.title}
        </h3>
        <p className="text-sm text-[var(--d-muted)]">
          {wordCount} {wordCount === 1 ? "word" : "words"}
        </p>
        <span className="mt-2 w-fit rounded-full bg-[var(--d-fill)] px-4 py-2 text-sm font-semibold">
          Start review
        </span>
      </div>
    </Link>
  )
}
