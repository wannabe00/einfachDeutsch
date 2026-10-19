import { useState } from "react"
import { Link, useSearchParams } from "react-router-dom"
import { useQuery } from "@tanstack/react-query"

import { useAuth } from "@/contexts/AuthContext"
import { fetchPremiumStatus, openPortal } from "@/api/premium"
import { Button } from "@/components/ui/button"
import { Msg, Section } from "./primitives"

/** The plan, and the Stripe portal to cancel or change it. Stripe sends the user
    back here after checkout; the webhook may need a moment to turn premium on. */
export function PremiumSection() {
  const { user } = useAuth()
  const [params] = useSearchParams()
  const [msg, setMsg] = useState("")
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
          Thanks! Premium turns on in a moment. Refresh the page if it doesn’t.
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
