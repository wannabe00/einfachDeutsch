import { useQuery } from "@tanstack/react-query"
import { ClipboardCheck, Lock, RotateCcw } from "lucide-react"

import { fetchChecks } from "@/api/curriculum"
import type { CheckUnit, ModulTest } from "@/types"
import { errorText } from "@/lib/apiError"
import { cn } from "@/lib/utils"
import { useStartCheck } from "@/hooks/useStartCheck"
import { LektionCover } from "@/components/lektion/LektionCover"

/*
 * Where checks are started: the Lektion page offers a warm-up review of the
 * Lektion before it (or a check of this one once it's finished), and the path
 * lists the Modul tests.
 */

/** On a Lektion page: review the previous Lektion before starting, or this
    one once it's finished. Nothing when neither is available. */
export function LektionCheckCard({ unitId, level, order }: { unitId: number; level: string; order: number }) {
  const { data } = useQuery({ queryKey: ["checks"], queryFn: fetchChecks })
  const start = useStartCheck()
  if (!data) return null

  const self = data.units.find((u) => u.id === unitId)
  const previous = data.units.find((u) => u.cefr_level === level && u.order === order - 1)
  const target: CheckUnit | undefined = self ?? previous
  if (!target) return null
  const warmUp = !self

  return (
    <section className="flex items-center gap-4 rounded-[20px] bg-surface p-4 shadow-card sm:p-5">
      <LektionCover order={target.order} level={target.cefr_level} size="sm" className="h-[64px] w-[50px] shrink-0 rounded-[10px]" />
      <div className="min-w-0 flex-1">
        <p className="text-[13px] font-semibold uppercase tracking-[0.04em] text-muted-foreground">
          {warmUp ? "Warm-up" : "Check yourself"}
        </p>
        <p className="font-semibold">Wiederholung: Lektion {target.order}</p>
        <p className="text-sm text-muted-foreground">
          {warmUp
            ? "A quick check of the last Lektion before you start."
            : "Some of this Lektion's words in batches of five, then gaps and a translation."}
        </p>
        {start.isError && <p className="mt-1 text-sm text-[hsl(var(--danger))]">{errorText(start.error)}</p>}
      </div>
      <button
        type="button"
        disabled={start.isPending}
        onClick={() => start.mutate({ kind: "review", unit: target.id })}
        className="inline-flex h-11 shrink-0 items-center gap-2 rounded-full bg-surface-2 px-5 font-semibold transition-colors hover:bg-border disabled:opacity-50"
      >
        <RotateCcw className="size-4" aria-hidden="true" />
        {start.isPending ? "Starting…" : "Start"}
      </button>
    </section>
  )
}

/** On the path: a test after every three Lektionen, across everything so far. */
export function ModulTests({ level }: { level: string }) {
  const { data } = useQuery({ queryKey: ["checks"], queryFn: fetchChecks })
  const moduls = data?.moduls.filter((m) => m.cefr_level === level) ?? []
  if (moduls.length === 0) return null

  return (
    <section>
      <div className="mb-2 flex items-baseline justify-between px-1">
        <h2 className="text-[22px] font-bold">Modul tests</h2>
        <span className="text-sm text-muted-foreground">Everything so far, by skill</span>
      </div>
      <ul className="grid grid-cols-2 gap-3 sm:grid-cols-4">
        {moduls.map((m) => (
          <li key={m.modul}>
            <ModulCard test={m} />
          </li>
        ))}
      </ul>
    </section>
  )
}

function ModulCard({ test }: { test: ModulTest }) {
  const start = useStartCheck()
  const best = test.best_score === null ? null : Math.round(test.best_score * 100)
  const status = !test.unlocked
    ? `After Lektion ${test.last}`
    : test.in_progress
      ? "In progress"
      : best !== null
        ? `Best ${best}%`
        : "Ready"

  return (
    <button
      type="button"
      disabled={!test.unlocked || start.isPending}
      onClick={() => start.mutate({ kind: "modul", level: test.cefr_level, modul: test.modul })}
      aria-label={`Modul ${test.modul} test, Lektionen ${test.first} to ${test.last}: ${status}`}
      className={cn(
        "flex h-full w-full flex-col items-start gap-1 rounded-[20px] bg-surface p-4 text-left shadow-card transition-colors",
        test.unlocked ? "hover:bg-surface-2" : "cursor-not-allowed",
      )}
    >
      <span
        className={cn(
          "mb-1 flex size-10 items-center justify-center rounded-xl",
          test.unlocked ? "bg-primary text-primary-foreground" : "bg-surface-2 text-muted-foreground",
        )}
      >
        {test.unlocked ? <ClipboardCheck className="size-5" aria-hidden="true" /> : <Lock className="size-5" aria-hidden="true" />}
      </span>
      <span className="font-semibold">Modul {test.modul}</span>
      <span className="text-sm text-muted-foreground">
        Lektionen {test.first}–{test.last}
      </span>
      <span className={cn("mt-1 text-sm font-semibold", test.unlocked ? "text-foreground" : "text-muted-foreground")}>
        {start.isPending ? "Starting…" : status}
      </span>
      {start.isError && <span className="text-xs text-[hsl(var(--danger))]">{errorText(start.error)}</span>}
    </button>
  )
}
