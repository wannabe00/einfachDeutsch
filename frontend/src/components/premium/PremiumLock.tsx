import { useState } from "react"
import { useQuery, useQueryClient } from "@tanstack/react-query"

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
      <Card className="w-full max-w-md p-8 text-center">
        <h2 className="text-2xl font-bold">This is a Premium feature</h2>
        <p className="mt-2 text-sm text-muted-foreground">Premium includes:</p>

        <ul className="mx-auto mt-3 w-fit list-disc space-y-1 pl-5 text-left text-sm">
          <li>Unlimited energy on the path</li>
          <li>The AI Assistant and AI explanations</li>
          <li>Recite: read a text, retell it aloud, get feedback</li>
        </ul>

        {status?.trial_available ? (
          <>
            <Button className="mt-6 w-full" disabled={busy} onClick={handleTrial}>
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

        {error && <p className="mt-3 text-sm text-danger">{error}</p>}
      </Card>
    </div>
  )
}
