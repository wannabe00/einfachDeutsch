import { Link } from "react-router-dom"
import { useQuery } from "@tanstack/react-query"
import { ChevronRight, GraduationCap, Lock } from "lucide-react"

import { fetchPath, fetchExamStatus } from "@/api/curriculum"
import type { PathUnit } from "@/types"
import { resolveAccent } from "@/lib/sections"
import { PageHeader } from "@/components/layout/PageHeader"
import { SectionCard } from "@/components/ui/SectionCard"
import { NextUp } from "@/components/path/NextUp"

/*
 * The learning path (Phase 23.4) — an overview of the units for your level,
 * stacked one under another. Each card opens that unit's page, where the
 * winding lesson road and its review material live. Level-gating is
 * server-side: the API only returns units at or below the user's level.
 */
export default function PathPage() {
  const { data, isLoading, isError } = useQuery({ queryKey: ["path"], queryFn: fetchPath })
  const { data: exam } = useQuery({ queryKey: ["exam"], queryFn: fetchExamStatus })

  if (isLoading) return <Centered>Loading your path…</Centered>
  if (isError || !data) return <Centered>Couldn’t load your path. Try again.</Centered>

  const { level, next_up, units } = data

  return (
    <div className="flex flex-col gap-6">
      {/* The energy meter lives in the top bar now (global + live), so it isn't
          repeated here. */}
      <PageHeader
        title="Your path"
        subtitle={`Level ${level} · ${units.length} ${units.length === 1 ? "unit" : "units"}`}
      />

      {next_up && (
        <NextUp
          title={next_up.lesson_title}
          subtitle={next_up.unit_title}
          href={`/path/${nextUnitId(units, next_up.lesson_id) ?? ""}`}
          accent={resolveAccent(undefined, 0)}
        />
      )}

      {exam?.unlocked && <ExamBanner level={exam.level} nextLevel={exam.next_level} />}

      {units.length === 0 ? (
        <Centered>No units for your level yet.</Centered>
      ) : (
        <div className="flex flex-col gap-4">
          {units.map((unit, i) => (
            <UnitCard key={unit.id} unit={unit} index={i} />
          ))}
        </div>
      )}
    </div>
  )
}

/** The checkpoint exam, shown once the level's path is essentially done. */
function ExamBanner({ level, nextLevel }: { level: string; nextLevel: string | null }) {
  return (
    <Link
      to="/path/exam"
      className="group flex items-center gap-4 rounded-2xl border border-white/10 bg-gradient-to-b from-surface-2 to-surface p-4 shadow-lg shadow-black/40 transition-transform hover:-translate-y-0.5"
    >
      <span
        className="flex size-12 shrink-0 items-center justify-center rounded-xl text-white"
        style={{ background: "hsl(var(--brand))", boxShadow: "0 8px 20px -6px hsl(var(--brand))" }}
      >
        <GraduationCap className="size-6" />
      </span>
      <div className="min-w-0">
        <p className="text-xs font-semibold uppercase tracking-wider text-muted-foreground">
          Checkpoint unlocked
        </p>
        <p className="truncate font-bold">{level} exam</p>
        <p className="truncate text-sm text-muted-foreground">
          {nextLevel ? `Pass to advance to ${nextLevel}` : "Pass to complete this level"}
        </p>
      </div>
    </Link>
  )
}

function UnitCard({ unit, index }: { unit: PathUnit; index: number }) {
  const accent = resolveAccent(unit.accent_color, index)
  const done = unit.lessons.filter((l) => l.state === "completed").length
  const locked = unit.lessons.length > 0 && unit.lessons.every((l) => l.state === "locked")
  const active = unit.lessons.some((l) => l.state === "current")

  return (
    <Link to={`/path/${unit.id}`} className="block transition-transform hover:-translate-y-0.5">
      <SectionCard accent={accent} glow={active}>
        <div className="flex items-center gap-4 p-5">
          <div className="min-w-0 flex-1">
            <p className="text-xs font-semibold uppercase tracking-wider text-muted-foreground">
              Unit {unit.order} · {unit.cefr_level}
            </p>
            <h2 className="mt-1 text-xl font-bold">{unit.title}</h2>
            {unit.theme && <p className="mt-0.5 text-sm text-muted-foreground">{unit.theme}</p>}
            <p className="mt-2 flex items-center gap-1.5 text-xs text-muted-foreground">
              {locked && <Lock className="size-3" />}
              {done}/{unit.lessons.length} lessons
              {active && <span style={{ color: accent }}> · in progress</span>}
            </p>
          </div>
          <ChevronRight className="size-5 shrink-0 text-muted-foreground" />
        </div>
      </SectionCard>
    </Link>
  )
}

/** Which unit holds the next lesson, so "Continue" deep-links to its page. */
function nextUnitId(units: PathUnit[], lessonId: number): number | undefined {
  return units.find((u) => u.lessons.some((l) => l.id === lessonId))?.id
}

function Centered({ children }: { children: React.ReactNode }) {
  return (
    <div className="flex h-64 items-center justify-center">
      <p className="text-sm text-muted-foreground">{children}</p>
    </div>
  )
}
