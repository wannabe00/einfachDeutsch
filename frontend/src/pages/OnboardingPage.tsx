import { useState } from "react"
import { useNavigate } from "react-router-dom"
import { useMutation, useQuery } from "@tanstack/react-query"

import { useAuth } from "@/contexts/AuthContext"
import {
  fetchPlacementTest,
  setLevel,
  submitPlacementTest,
} from "@/api/leveling"
import type { CEFRLevel, PlacementResult } from "@/types"
import { SITE_NAME } from "@/lib/site"
import { Button } from "@/components/ui/button"
import { cn } from "@/lib/utils"

const LEVELS: CEFRLevel[] = ["A1", "A2", "B1", "B2", "C1", "C2"]

type Phase = "choose" | "test" | "result"

export default function OnboardingPage() {
  const { refreshUser } = useAuth()
  const navigate = useNavigate()
  const [phase, setPhase] = useState<Phase>("choose")
  const [answers, setAnswers] = useState<Record<string, string>>({})
  const [result, setResult] = useState<PlacementResult | null>(null)
  const [chosen, setChosen] = useState<CEFRLevel>("A1")

  const { data: questions } = useQuery({
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
    mutationFn: () => submitPlacementTest(answers),
    onSuccess: (r) => {
      setResult(r)
      setChosen(r.suggested_level)
      setPhase("result")
    },
  })

  function adjustOptions(level: CEFRLevel): CEFRLevel[] {
    const i = LEVELS.indexOf(level)
    const out: CEFRLevel[] = []
    if (i > 0) out.push(LEVELS[i - 1])
    out.push(level)
    if (i < LEVELS.length - 1) out.push(LEVELS[i + 1])
    return out
  }

  const allAnswered =
    !!questions && questions.every((q) => answers[q.id] !== undefined)

  return (
    <div className="flex min-h-screen items-center justify-center bg-background px-4 py-10">
      <div className="w-full max-w-lg">
        <h1 className="text-center text-2xl font-semibold tracking-tight">
          {SITE_NAME}
        </h1>

        {/* Step 1 — choose: start at A1, or take the test (no free level pick) */}
        {phase === "choose" && (
          <div className="mt-8 rounded-xl border border-border bg-surface p-6">
            <h2 className="text-lg font-semibold">What's your German level?</h2>
            <p className="mt-1 text-sm text-muted-foreground">
              New to German? Start at A1. Already know some? Take the placement
              test and we'll set your level for you.
            </p>
            <div className="mt-5 flex flex-col gap-3">
              <Button
                size="lg"
                disabled={save.isPending}
                onClick={() => save.mutate("A1")}
              >
                {save.isPending ? "Starting…" : "Start at A1 — I'm a beginner"}
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

        {/* Step 2 — test */}
        {phase === "test" && (
          <div className="mt-8 rounded-xl border border-border bg-surface p-6">
            <h2 className="text-lg font-semibold">Placement test</h2>
            <p className="mt-1 text-sm text-muted-foreground">
              Pick the best answer. Skip any you don't know.
            </p>
            {!questions ? (
              <p className="mt-6 text-sm text-muted-foreground">Loading…</p>
            ) : (
              <div className="mt-5 flex flex-col gap-5">
                {questions.map((q, idx) => (
                  <div key={q.id}>
                    <p className="text-sm font-medium">
                      {idx + 1}. {q.prompt}
                    </p>
                    <div className="mt-2 flex flex-wrap gap-2">
                      {q.options.map((opt) => (
                        <button
                          key={opt}
                          onClick={() =>
                            setAnswers((a) => ({ ...a, [q.id]: opt }))
                          }
                          className={cn(
                            "rounded-lg border px-3 py-1.5 text-sm transition-colors",
                            answers[q.id] === opt
                              ? "border-accent bg-accent text-accent-foreground"
                              : "border-border bg-background hover:border-accent",
                          )}
                        >
                          {opt}
                        </button>
                      ))}
                    </div>
                  </div>
                ))}
                <Button
                  className="mt-2"
                  disabled={!allAnswered || grade.isPending}
                  onClick={() => grade.mutate()}
                >
                  {grade.isPending ? "Scoring…" : "See my level"}
                </Button>
              </div>
            )}
          </div>
        )}

        {/* Step 3 — result + adjust */}
        {phase === "result" && result && (
          <div className="mt-8 rounded-xl border border-border bg-surface p-6 text-center">
            <p className="text-sm text-muted-foreground">
              You got {result.correct} of {result.total} right. We suggest:
            </p>
            <p className="mt-2 text-4xl font-bold text-accent">
              {result.suggested_level}
            </p>
            <p className="mt-4 text-sm text-muted-foreground">
              Adjust if it feels off:
            </p>
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
    </div>
  )
}
