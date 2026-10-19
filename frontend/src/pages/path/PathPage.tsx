import { Link } from "react-router-dom"
import { useQuery } from "@tanstack/react-query"
import { ArrowRight, Award, Check, ChevronDown, Lock, PartyPopper } from "lucide-react"

import { fetchPath, fetchExamStatus } from "@/api/curriculum"
import type { PathUnit } from "@/types"
import { cn } from "@/lib/utils"
import { LektionCover } from "@/components/lektion/LektionCover"
import { ModulTests } from "@/components/checks/CheckCards"
import { LessonRows } from "@/components/lektion/LessonRows"
import { ProgressRing } from "@/components/lektion/ProgressRing"
import { lektionColor } from "@/components/lektion/lektionColor"

type UnitStatus = "done" | "current" | "open" | "locked"

const MODUL_SIZE = 3 // Lektionen per Modul, like the books (backend curriculum/checks.py)

function unitStatus(unit: PathUnit): UnitStatus {
  const states = unit.lessons.map((l) => l.state)
  if (states.length > 0 && states.every((s) => s === "completed")) return "done"
  if (states.includes("current")) return "current"
  if (states.length > 0 && states.every((s) => s === "locked")) return "locked"
  return "open"
}

/*
 * The learning path, like the chapters of a book: the Lektion you're on is
 * opened up with its lessons, the rest are listed by Modul (folded, except the
 * Modul you're in) with a cover and progress.
 * Future Lektionen are locked and blurred. The API only returns units at or
 * below your level.
 */
export default function PathPage() {
  const { data, isLoading, isError } = useQuery({ queryKey: ["path"], queryFn: fetchPath })
  const { data: exam } = useQuery({ queryKey: ["exam"], queryFn: fetchExamStatus })

  if (isLoading) return <PathSkeleton />
  if (isError || !data) return <Message>Couldn’t load your path. Try again.</Message>

  const { level, next_up, units } = data
  const lessons = units.flatMap((u) => u.lessons)
  const done = lessons.filter((l) => l.state === "completed").length
  const pct = lessons.length > 0 ? done / lessons.length : 0

  const current = units.find((u) => unitStatus(u) === "current")
  const finishedUnits = units.filter((u) => unitStatus(u) === "done").length

  return (
    <div className="flex flex-col gap-8">
      <header className="flex flex-col gap-2">
        <p className="text-[13px] font-semibold uppercase tracking-[0.04em] text-muted-foreground">
          Level {level} · {units.length} Lektionen
        </p>
        <h1 className="text-[34px] font-extrabold leading-tight sm:text-[40px]">Dein Lernpfad</h1>
        <p className="text-muted-foreground">
          {done} of {lessons.length} lessons done · {finishedUnits}{" "}
          {finishedUnits === 1 ? "Lektion" : "Lektionen"} finished
        </p>
        <div
          className="mt-1 h-2 max-w-md overflow-hidden rounded-full bg-surface-2"
          role="progressbar"
          aria-label={`Level ${level} progress`}
          aria-valuemin={0}
          aria-valuemax={100}
          aria-valuenow={Math.round(pct * 100)}
        >
          <div
            className="h-full rounded-full bg-primary transition-[width] duration-700"
            style={{ width: `${pct * 100}%` }}
          />
        </div>
      </header>

      {exam?.unlocked && <ExamCard level={exam.level} nextLevel={exam.next_level} />}

      {current ? (
        <CurrentUnit unit={current} nextLessonId={next_up?.lesson_id ?? null} />
      ) : (
        lessons.length > 0 &&
        !next_up && (
          <p className="flex items-center gap-3 rounded-2xl bg-[hsl(var(--success-bg))] p-5 font-medium">
            <PartyPopper className="size-5 text-[hsl(var(--success))]" aria-hidden="true" />
            You’ve finished every lesson on this level.
          </p>
        )
      )}

      {units.length === 0 && <Message>No Lektionen for your level yet.</Message>}

      <ModulTests level={level} />

      <ModulList units={units} current={current} />
    </div>
  )
}

/** The Lektion you're on: big cover, its lessons, and Continue. */
function CurrentUnit({ unit, nextLessonId }: { unit: PathUnit; nextLessonId: number | null }) {
  const color = lektionColor(unit.order)
  const href = nextLessonId ? `/path/${unit.id}/lesson/${nextLessonId}` : `/path/${unit.id}`

  return (
    <section className="grid overflow-hidden rounded-[24px] bg-surface shadow-card md:grid-cols-[280px_1fr]">
      <LektionCover order={unit.order} level={unit.cefr_level} className="h-44 md:h-full md:min-h-[280px]" />
      <div className="flex min-w-0 flex-col gap-1.5 p-5 sm:p-6">
        <p className="text-[13px] font-semibold uppercase tracking-[0.04em]" style={{ color }}>
          Lektion {unit.order} · You are here
        </p>
        <h2 className="text-2xl font-extrabold leading-tight sm:text-[28px]">{unit.title}</h2>
        {unit.theme && <p className="text-muted-foreground">{unit.theme}</p>}
        <div className="mt-3">
          <LessonRows lessons={unit.lessons} unitId={unit.id} />
        </div>
        <div className="mt-3 flex flex-wrap gap-2.5">
          <Link
            to={href}
            className="inline-flex h-12 items-center gap-2 rounded-full bg-primary px-6 font-semibold text-primary-foreground transition hover:brightness-110 active:scale-[0.97]"
          >
            Continue <ArrowRight className="size-[18px]" aria-hidden="true" />
          </Link>
          <Link
            to={`/path/${unit.id}`}
            className="inline-flex h-12 items-center rounded-full bg-surface-2 px-6 font-semibold transition-colors hover:bg-border"
          >
            Words &amp; grammar
          </Link>
        </div>
      </div>
    </section>
  )
}

/** The Lektionen in Moduls of three, like the books. Each Modul folds to one
    row; the one you're in starts open, so the page stays short as levels grow. */
function ModulList({ units, current }: { units: PathUnit[]; current?: PathUnit }) {
  const moduls: { key: string; level: string; modul: number; units: PathUnit[] }[] = []
  for (const unit of units) {
    const modul = Math.ceil(unit.order / MODUL_SIZE)
    const key = `${unit.cefr_level}-${modul}`
    const last = moduls[moduls.length - 1]
    if (last?.key === key) last.units.push(unit)
    else moduls.push({ key, level: unit.cefr_level, modul, units: [unit] })
  }
  const showLevel = new Set(moduls.map((m) => m.level)).size > 1
  const openKey = current
    ? `${current.cefr_level}-${Math.ceil(current.order / MODUL_SIZE)}`
    : moduls.find((m) => m.units.some((u) => unitStatus(u) !== "done"))?.key

  if (moduls.length === 0) return null
  return (
    <section>
      <h2 className="mb-2 px-1 text-[22px] font-bold">Moduls</h2>
      <div className="flex flex-col gap-2.5">
        {moduls.map((m) => {
          const statuses = m.units.map(unitStatus)
          const finished = statuses.filter((st) => st === "done").length
          const locked = statuses.every((st) => st === "locked")
          const first = m.units[0].order
          const last = m.units[m.units.length - 1].order
          return (
            <details
              key={m.key}
              open={m.key === openKey}
              className="group overflow-hidden rounded-[20px] bg-surface shadow-card"
            >
              <summary className="flex min-h-[64px] cursor-pointer list-none items-center gap-3 px-4 py-3 transition-colors hover:bg-surface-2 [&::-webkit-details-marker]:hidden">
                <span className={cn("min-w-0 flex-1", locked && "opacity-60")}>
                  <span className="block font-bold">
                    {showLevel && `${m.level} · `}Modul {m.modul}
                  </span>
                  <span className="block text-sm text-muted-foreground">
                    Lektion {first}–{last}
                    {m.key === openKey && current ? " · You are here" : ""}
                  </span>
                </span>
                {locked ? (
                  <Lock className="size-5 shrink-0 text-muted-foreground" aria-label="Locked" />
                ) : finished === m.units.length ? (
                  <span className="flex size-8 shrink-0 items-center justify-center rounded-full bg-[hsl(var(--success-bg))] text-[hsl(var(--success))]">
                    <Check className="size-4" aria-label="Finished" />
                  </span>
                ) : (
                  <span className="shrink-0 text-sm tabular-nums text-muted-foreground">
                    {finished}/{m.units.length}
                  </span>
                )}
                <ChevronDown
                  className="size-5 shrink-0 text-muted-foreground transition-transform group-open:rotate-180"
                  aria-hidden="true"
                />
              </summary>
              <ul className="border-t border-border/70 p-1.5">
                {m.units.map((unit, i) => (
                  <li key={unit.id}>
                    {i > 0 && <div className="ml-[92px] h-px bg-border/70" aria-hidden="true" />}
                    <ChapterRow unit={unit} />
                  </li>
                ))}
              </ul>
            </details>
          )
        })}
      </div>
    </section>
  )
}

function ChapterRow({ unit }: { unit: PathUnit }) {
  const status = unitStatus(unit)
  const locked = status === "locked"
  const color = lektionColor(unit.order)
  const done = unit.lessons.filter((l) => l.state === "completed").length
  const total = unit.lessons.length

  const body = (
    <>
      <LektionCover
        order={unit.order}
        level={unit.cefr_level}
        size="sm"
        className={cn("h-[76px] w-[60px] shrink-0 rounded-[10px]", locked && "opacity-50 blur-[2px] grayscale")}
      />
      <span className={cn("min-w-0 flex-1", locked && "select-none opacity-60")}>
        <span
          className="block text-xs font-semibold uppercase tracking-[0.04em]"
          style={{ color: locked ? undefined : color }}
        >
          Lektion {unit.order}
        </span>
        <span className={cn("block truncate font-semibold", locked && "blur-[3px]")}>{unit.title}</span>
        {unit.theme && (
          <span className={cn("block truncate text-sm text-muted-foreground", locked && "blur-[3px]")}>
            {unit.theme}
          </span>
        )}
      </span>
      {locked ? (
        <Lock className="mr-2 size-5 shrink-0 text-muted-foreground" aria-hidden="true" />
      ) : status === "done" ? (
        <span className="mr-1 flex size-9 shrink-0 items-center justify-center rounded-full bg-[hsl(var(--success-bg))] text-[hsl(var(--success))]">
          <Check className="size-[18px]" aria-label="Finished" />
        </span>
      ) : (
        <span className="mr-1 flex shrink-0 items-center gap-2">
          <span className="text-xs tabular-nums text-muted-foreground">
            {done}/{total}
          </span>
          <ProgressRing pct={total > 0 ? done / total : 0} color={color} />
        </span>
      )}
    </>
  )

  const cls = "flex min-h-[92px] w-full items-center gap-4 rounded-2xl px-2.5 py-2"
  if (locked) {
    return (
      <div className={cls} aria-label={`Lektion ${unit.order}, locked`}>
        {body}
      </div>
    )
  }
  return (
    <Link to={`/path/${unit.id}`} className={cn(cls, "transition-colors hover:bg-surface-2")}>
      {body}
    </Link>
  )
}

/** The checkpoint exam, shown once the level's path is essentially done. */
function ExamCard({ level, nextLevel }: { level: string; nextLevel: string | null }) {
  return (
    <section className="flex flex-col gap-4 rounded-[24px] bg-surface p-5 shadow-card ring-2 ring-primary/60 sm:flex-row sm:items-center sm:p-6">
      <span className="flex size-12 shrink-0 items-center justify-center rounded-2xl bg-primary text-primary-foreground">
        <Award className="size-6" aria-hidden="true" />
      </span>
      <div className="min-w-0 flex-1">
        <p className="text-lg font-bold">{level} checkpoint exam unlocked</p>
        <p className="text-muted-foreground">
          {nextLevel ? `Pass it to move up to ${nextLevel}.` : "Pass it to complete this level."}
        </p>
      </div>
      <Link
        to="/path/exam"
        className="inline-flex h-12 shrink-0 items-center justify-center rounded-full bg-primary px-6 font-semibold text-primary-foreground transition hover:brightness-110"
      >
        Take the exam
      </Link>
    </section>
  )
}

function Message({ children }: { children: React.ReactNode }) {
  return (
    <div className="flex h-64 items-center justify-center">
      <p className="text-muted-foreground">{children}</p>
    </div>
  )
}

function PathSkeleton() {
  return (
    <div className="flex flex-col gap-8" aria-busy="true" aria-label="Loading your path">
      <div className="h-24 w-72 animate-pulse rounded-2xl bg-surface-2" />
      <div className="h-72 animate-pulse rounded-[24px] bg-surface-2" />
      <div className="h-64 animate-pulse rounded-[20px] bg-surface-2" />
    </div>
  )
}
