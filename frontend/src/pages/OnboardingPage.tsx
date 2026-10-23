import { useState } from "react"
import { useNavigate } from "react-router-dom"
import { useMutation, useQuery } from "@tanstack/react-query"

import { useAuth } from "@/contexts/AuthContext"
import { fetchPlacementTest, setLevel, submitPlacementTest } from "@/api/leveling"
import type { CEFRLevel, PlacementResult } from "@/types"
import { ArrowRight, CaseSensitive, ClipboardCheck, Sprout } from "lucide-react"

import { Button } from "@/components/ui/button"
import { cn } from "@/lib/utils"
import { PlacementTestForm } from "@/components/onboarding/PlacementTestForm"
import { AuthShell, AuthWordmark } from "@/components/auth/AuthShell"
import { AUTH_CARD } from "@/lib/authCard"
import { COURSE_LEVELS } from "@/lib/site"

const LEVELS: CEFRLevel[] = [...COURSE_LEVELS]

type Phase = "choose" | "test" | "result"

export default function OnboardingPage() {
  const { refreshUser } = useAuth()
  const navigate = useNavigate()
  const [phase, setPhase] = useState<Phase>("choose")
  const [result, setResult] = useState<PlacementResult | null>(null)
  const [chosen, setChosen] = useState<CEFRLevel>("A1")

  const { data: test } = useQuery({
    queryKey: ["placement-test"],
    queryFn: fetchPlacementTest,
    enabled: phase === "test",
  })

  const save = useMutation({
    // `to`: complete beginners land on the path, where Grundlagen comes first.
    mutationFn: ({ level }: { level: CEFRLevel; to: string }) => setLevel(level),
    onSuccess: async (_, { to }) => {
      await refreshUser()
      navigate(to)
    },
  })

  const grade = useMutation({
    mutationFn: (vars: { answers: Record<string, string>; writing: string }) =>
      submitPlacementTest(vars.answers, vars.writing),
    onSuccess: (r) => {
      setResult(r)
      setChosen(r.suggested_level)
      setPhase("result")
    },
  })

  // Suggested level ±1, so the user can nudge the AI's call.
  function adjustOptions(level: CEFRLevel): CEFRLevel[] {
    const i = LEVELS.indexOf(level)
    const out: CEFRLevel[] = []
    if (i > 0) out.push(LEVELS[i - 1])
    out.push(level)
    if (i < LEVELS.length - 1) out.push(LEVELS[i + 1])
    return out
  }

  return (
    <AuthShell maxWidth="max-w-lg">
      <div>
        <AuthWordmark />

        {/* Step 1: Grundlagen, A1 or the test. There's no free choice of level. */}
        {phase === "choose" && (
          <div className="mt-6 lg:mt-0">
            <h1 className="text-center text-3xl font-extrabold lg:text-left">What's your German level?</h1>
            <p className="mt-1 text-center text-muted-foreground lg:text-left">
              New to German? Start at A1. Already know some? The placement test sets your level. The course goes up to B1.
            </p>
            <div className="mt-8 flex flex-col gap-3">
              <LevelChoice
                icon={CaseSensitive}
                color="hsl(var(--section-2))"
                title="I'm completely new"
                body="Start with Grundlagen: letters, sounds, numbers and first words. Free, no energy."
                disabled={save.isPending}
                onClick={() => save.mutate({ level: "A1", to: "/path" })}
              />
              <LevelChoice
                icon={Sprout}
                color="hsl(var(--section-4))"
                title={save.isPending ? "Starting…" : "I'm a beginner"}
                body="Start at A1 with the very first Lektion."
                disabled={save.isPending}
                onClick={() => save.mutate({ level: "A1", to: "/" })}
              />
              <LevelChoice
                icon={ClipboardCheck}
                color="hsl(var(--section-1))"
                title="I know some German"
                body="Take the placement test and we'll set your level."
                disabled={save.isPending}
                onClick={() => setPhase("test")}
              />
            </div>
          </div>
        )}

        {/* Step 2: the placement test */}
        {phase === "test" &&
          (test ? (
            <PlacementTestForm
              test={test}
              submitting={grade.isPending}
              onSubmit={(answers, writing) => grade.mutate({ answers, writing })}
            />
          ) : (
            <p className="mt-8 text-center text-sm text-muted-foreground">Loading…</p>
          ))}

        {/* Step 3: the result, which the user can nudge up or down */}
        {phase === "result" && result && (
          <div className={`mt-8 text-center ${AUTH_CARD}`}>
            <p className="text-sm text-muted-foreground">
              You got {result.correct} of {result.total} right. We suggest:
            </p>
            <p className="mx-auto mt-4 flex size-28 items-center justify-center rounded-full bg-primary/10 font-grotesk text-5xl font-extrabold text-primary animate-in zoom-in-50 fade-in-0 duration-500">
              {result.suggested_level}
            </p>
            {result.source === "ai" && result.rationale && (
              <p className="mx-auto mt-2 max-w-sm text-xs text-muted-foreground">
                {result.rationale}
              </p>
            )}
            <p className="mt-6 text-sm text-muted-foreground">Adjust if it feels off:</p>
            <div className="mt-2 flex justify-center gap-2">
              {adjustOptions(result.suggested_level).map((lvl) => (
                <button
                  key={lvl}
                  onClick={() => setChosen(lvl)}
                  className={cn(
                    "min-h-[48px] min-w-[64px] rounded-2xl px-4 text-base font-bold transition-colors",
                    chosen === lvl
                      ? "bg-primary text-primary-foreground"
                      : "bg-surface-2 hover:bg-border",
                  )}
                >
                  {lvl}
                </button>
              ))}
            </div>
            <Button
              size="lg"
              className="mt-7 w-full"
              disabled={save.isPending}
              onClick={() => save.mutate({ level: chosen, to: "/" })}
            >
              {save.isPending ? "Saving…" : `Start at ${chosen}`}
            </Button>
          </div>
        )}
      </div>
    </AuthShell>
  )
}

function LevelChoice({
  icon: Icon,
  color,
  title,
  body,
  disabled,
  onClick,
}: {
  icon: typeof Sprout
  color: string
  title: string
  body: string
  disabled: boolean
  onClick: () => void
}) {
  return (
    <button
      onClick={onClick}
      disabled={disabled}
      className="lift flex w-full items-center gap-4 rounded-[24px] bg-surface p-5 text-left shadow-card disabled:opacity-60"
    >
      <span
        className="flex size-14 shrink-0 items-center justify-center rounded-2xl text-white"
        style={{ background: color }}
      >
        <Icon className="size-7" aria-hidden="true" />
      </span>
      <span className="min-w-0 flex-1">
        <span className="block text-lg font-bold">{title}</span>
        <span className="block text-muted-foreground">{body}</span>
      </span>
      <ArrowRight className="size-5 shrink-0 text-muted-foreground" aria-hidden="true" />
    </button>
  )
}
