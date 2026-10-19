import { useEffect, useState } from "react"
import { Link, useSearchParams } from "react-router-dom"
import { useQuery, useQueryClient } from "@tanstack/react-query"

import { useAuth } from "@/contexts/AuthContext"
import { confirmCheckout, fetchPremiumStatus, openPortal } from "@/api/premium"
import { Button } from "@/components/ui/button"
import { Msg, Section } from "./primitives"

/** The plan, and the Stripe portal to cancel or change it. Stripe sends the user
    back here after checkout with its session id, which turns premium on at once. */
export function PremiumSection() {
  const { user, refreshUser } = useAuth()
  const qc = useQueryClient()
  const [params] = useSearchParams()
  const [msg, setMsg] = useState("")
  const sessionId = params.get("session_id")
  const { data: confirmed, isError: confirmFailed } = useQuery({
    queryKey: ["billing-confirm", sessionId],
    queryFn: () => confirmCheckout(sessionId!),
    enabled: !!sessionId,
    staleTime: Infinity,
    retry: 2,
  })
  useEffect(() => {
    if (!confirmed) return
    void refreshUser()
    qc.invalidateQueries({ queryKey: ["premium-status"] })
    qc.invalidateQueries({ queryKey: ["energy"] })
  }, [confirmed, refreshUser, qc])
  const { data: status } = useQuery({
    queryKey: ["premium-status"],
    queryFn: fetchPremiumStatus,
    enabled: !!user,
  })

  async function manage() {
    setMsg("")
    try {
      window.location.assign(await openPortal())
    } catch {
      setMsg("Couldn’t open the billing page. Try again.")
    }
  }

  const until = status?.premium_until ? new Date(status.premium_until).toLocaleDateString() : null
  return (
    <Section title="Premium">
      {params.get("billing") === "success" && !user?.has_premium && (
        <p className="-mt-2 mb-3 text-sm text-muted-foreground">
          {confirmFailed
            ? "Payment received. Premium turns on within a minute; refresh then."
            : "Thanks! Turning Premium on…"}
        </p>
      )}
      <p className="text-sm text-muted-foreground">
        {user?.has_premium
          ? until
            ? `You have Premium until ${until}. It renews unless you cancel.`
            : "You have Premium."
          : "You’re on the free plan."}
      </p>
      <div className="mt-3 flex flex-wrap gap-2">
        {status?.has_subscription && (
          <Button variant="outline" onClick={manage}>
            Manage subscription
          </Button>
        )}
        {!user?.has_premium && (
          <Button asChild>
            <Link to="/ai">Get Premium</Link>
          </Button>
        )}
      </div>
      {msg && <Msg tone="danger">{msg}</Msg>}
    </Section>
  )
}
