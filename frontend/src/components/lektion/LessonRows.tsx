import { Link } from "react-router-dom"
import { Check, Lock, Play } from "lucide-react"

import type { PathLesson } from "@/types"
import { cn } from "@/lib/utils"

/*
 * A Lektion's lessons as rows: done (green tick), next up (red play),
 * open (grey play) and locked. Unlocked rows open the lesson player.
 */
export function LessonRows({ lessons, unitId }: { lessons: PathLesson[]; unitId: number }) {
  return (
    <ul className="flex flex-col gap-2">
      {lessons.map((lesson, i) => (
        <li key={lesson.id}>
          <LessonRow lesson={lesson} index={i} unitId={unitId} />
        </li>
      ))}
    </ul>
  )
}

function LessonRow({ lesson, index, unitId }: { lesson: PathLesson; index: number; unitId: number }) {
  const { state } = lesson
  const now = state === "current"

  const dot = (
    <span
      className={cn(
        "flex size-9 shrink-0 items-center justify-center rounded-full",
        state === "completed" && "bg-[hsl(var(--success-bg))] text-[hsl(var(--success))]",
        now && "bg-primary text-primary-foreground",
        state === "available" && "bg-surface text-foreground",
        state === "locked" && "bg-surface text-muted-foreground",
      )}
    >
      {state === "completed" ? (
        <Check className="size-[18px]" aria-label="Done" />
      ) : state === "locked" ? (
        <Lock className="size-4" aria-label="Locked" />
      ) : (
        <Play className="size-4 fill-current" aria-hidden="true" />
      )}
    </span>
  )

  const body = (
    <>
      {dot}
      <span className="min-w-0 flex-1">
        <span className="block text-xs font-medium text-muted-foreground">Lesson {index + 1}</span>
        <span className={cn("block truncate font-medium", state === "locked" && "text-muted-foreground")}>
          {lesson.title}
        </span>
      </span>
      {now ? (
        <span className="shrink-0 text-sm font-semibold text-primary">Start</span>
      ) : (
        <span className="shrink-0 text-xs font-semibold tabular-nums text-muted-foreground">
          +{lesson.xp_reward} XP
        </span>
      )}
    </>
  )

  const cls = cn(
    "flex min-h-[60px] items-center gap-3 rounded-2xl px-3 py-2",
    now ? "bg-primary/10" : "bg-surface-2/70",
  )

  if (state === "locked") return <div className={cls}>{body}</div>
  return (
    <Link
      to={`/path/${unitId}/lesson/${lesson.id}`}
      className={cn(cls, "transition-colors", now ? "hover:bg-primary/15" : "hover:bg-surface-2")}
    >
      {body}
    </Link>
  )
}
