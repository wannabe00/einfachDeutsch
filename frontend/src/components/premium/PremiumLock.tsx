import { useState } from "react"
import { useQuery, useQueryClient } from "@tanstack/react-query"
import { Check, Crown } from "lucide-react"

import { fetchPremiumStatus, startTrial } from "@/api/premium"
import { useAuth } from "@/contexts/AuthContext"
import { Button } from "@/components/ui/button"
import { Card } from "@/components/ui/card"

/**
 * Shown in place of a premium-only page (AI Assistant, Recite) for free users.
 * The API returns 403 for these anyway; this just explains why and offers the
 * trial.
 */
export function PremiumLock() {
  const { user, refreshUser } = useAuth()
  const qc = useQueryClient()
  const [busy, setBusy] = useState(false)
  const [error, setError] = useState<string | null>(null)

  const { data: status } = useQuery({
    queryKey: ["premium-status"],
    queryFn: fetchPremiumStatus,
    enabled: !!user,
  })

  async function handleTrial() {
    setBusy(true)
    setError(null)
    try {
      await startTrial()
      await refreshUser()
      qc.invalidateQueries({ queryKey: ["premium-status"] })
      qc.invalidateQueries({ queryKey: ["energy"] })
    } catch {
      setError("Couldn’t start your trial. It may already have been used.")
    } finally {
      setBusy(false)
    }
  }

  return (
    <div className="flex justify-center pt-10">
      <Card className="w-full max-w-md rounded-[28px] p-8 text-center">
        <span className="mx-auto flex size-16 items-center justify-center rounded-2xl bg-primary text-primary-foreground">
          <Crown className="size-8" aria-hidden="true" />
        </span>
        <h2 className="mt-5 text-3xl font-extrabold">This is a Premium feature</h2>
        <ul className="mt-6 flex flex-col gap-2.5 rounded-2xl bg-surface-2/70 p-4 text-left text-[15px]">
          {[
            "Unlimited energy on the path",
            "The AI Assistant and AI explanations",
            "AI feedback on your Schreiben texts",
            "Recite: read a text, retell it aloud, get feedback",
          ].map((perk) => (
            <li key={perk} className="flex items-start gap-2.5">
              <Check className="mt-0.5 size-[18px] shrink-0 text-success" aria-hidden="true" />
              {perk}
            </li>
          ))}
        </ul>

        {status?.trial_available ? (
          <>
            <Button size="lg" className="mt-6 w-full" disabled={busy} onClick={handleTrial}>
              {busy ? "Starting…" : `Start ${status.trial_days}-day free trial`}
            </Button>
            <p className="mt-2 text-xs text-muted-foreground">
              No card needed. Payments aren’t live yet.
            </p>
          </>
        ) : (
          <p className="mt-6 text-sm text-muted-foreground">
            Paid plans aren’t live yet. Premium is granted manually for now.
          </p>
        )}

        {error && <p className="mt-3 text-sm font-medium text-danger">{error}</p>}
      </Card>
    </div>
  )
}
