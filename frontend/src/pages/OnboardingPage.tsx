import { useState } from "react"
import { useNavigate } from "react-router-dom"
import { useMutation, useQuery } from "@tanstack/react-query"

import { useAuth } from "@/contexts/AuthContext"
import { fetchPlacementTest, setLevel, submitPlacementTest } from "@/api/leveling"
import type { CEFRLevel, PlacementResult } from "@/types"
import { Button } from "@/components/ui/button"
import { cn } from "@/lib/utils"
import { PlacementTestForm } from "@/components/onboarding/PlacementTestForm"
import { AuthShell, AuthWordmark } from "@/components/auth/AuthShell"
import { AUTH_CARD } from "@/lib/authCard"

const LEVELS: CEFRLevel[] = ["A1", "A2", "B1", "B2", "C1", "C2"]

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
    mutationFn: (level: CEFRLevel) => setLevel(level),
    onSuccess: async () => {
      await refreshUser()
      navigate("/")
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

        {/* Step 1: start at A1 or take the test. There's no free choice of level. */}
        {phase === "choose" && (
          <div className={`mt-8 ${AUTH_CARD}`}>
            <h2 className="text-lg font-semibold">What's your German level?</h2>
            <p className="mt-1 text-sm text-muted-foreground">
              New to German? Start at A1. Already know some? Take the placement
              test and we'll set your level for you.
            </p>
            <div className="mt-5 flex flex-col gap-3">
              <Button size="lg" disabled={save.isPending} onClick={() => save.mutate("A1")}>
                {save.isPending ? "Starting…" : "I'm a beginner, start at A1"}
              </Button>
              <Button
                variant="outline"
                size="lg"
                disabled={save.isPending}
                onClick={() => setPhase("test")}
              >
                Take the placement test
              </Button>
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
            <p className="mt-2 text-4xl font-bold text-accent">{result.suggested_level}</p>
            {result.source === "ai" && result.rationale && (
              <p className="mx-auto mt-2 max-w-sm text-xs text-muted-foreground">
                {result.rationale}
              </p>
            )}
            <p className="mt-4 text-sm text-muted-foreground">Adjust if it feels off:</p>
            <div className="mt-2 flex justify-center gap-2">
              {adjustOptions(result.suggested_level).map((lvl) => (
                <button
                  key={lvl}
                  onClick={() => setChosen(lvl)}
                  className={cn(
                    "rounded-lg border px-4 py-2 text-sm font-medium transition-colors",
                    chosen === lvl
                      ? "border-accent bg-accent text-accent-foreground"
                      : "border-border bg-background hover:border-accent",
                  )}
                >
                  {lvl}
                </button>
              ))}
            </div>
            <Button
              className="mt-6 w-full"
              disabled={save.isPending}
              onClick={() => save.mutate(chosen)}
            >
              {save.isPending ? "Saving…" : `Start at ${chosen}`}
            </Button>
          </div>
        )}
      </div>
    </AuthShell>
  )
}
