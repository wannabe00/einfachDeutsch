import { useState } from "react"
import { useQuery } from "@tanstack/react-query"
import { Check, Crown } from "lucide-react"

import { fetchPremiumStatus, startCheckout } from "@/api/premium"
import { useAuth } from "@/contexts/AuthContext"
import { PRICES } from "@/lib/site"
import { Button } from "@/components/ui/button"
import { Card } from "@/components/ui/card"

/**
 * Shown in place of a premium-only page (the four skills, AI Assistant) for free users.
 * The API returns 403 for these anyway; this just explains why and sends the
 * user to Stripe Checkout (with the one free trial if it's unused).
 */
export function PremiumLock() {
  const { user } = useAuth()
  const [busy, setBusy] = useState<"monthly" | "annual" | null>(null)
  const [error, setError] = useState<string | null>(null)

  const { data: status } = useQuery({
    queryKey: ["premium-status"],
    queryFn: fetchPremiumStatus,
    enabled: !!user,
  })

  async function subscribe(plan: "monthly" | "annual") {
    setBusy(plan)
    setError(null)
    try {
      window.location.assign(await startCheckout(plan))
    } catch {
      setError("Couldn’t open checkout. Please try again.")
      setBusy(null)
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
            "Lesen, Hören and Schreiben exam practice, with AI feedback on your texts",
            "Talk to AI: 5 five-minute talks a month with an AI partner, then a report",
          ].map((perk) => (
            <li key={perk} className="flex items-start gap-2.5">
              <Check className="mt-0.5 size-[18px] shrink-0 text-success" aria-hidden="true" />
              {perk}
            </li>
          ))}
        </ul>

        <div className="mt-6 flex flex-col gap-2.5">
          <Button size="lg" className="w-full" disabled={!!busy} onClick={() => subscribe("annual")}>
            {busy === "annual" ? "Opening…" : `Yearly · ${PRICES.annual}`}
          </Button>
          <Button
            size="lg"
            variant="outline"
            className="w-full"
            disabled={!!busy}
            onClick={() => subscribe("monthly")}
          >
            {busy === "monthly" ? "Opening…" : `Monthly · ${PRICES.monthly}`}
          </Button>
        </div>
        <p className="mt-2 text-xs text-muted-foreground">
          {status?.trial_available
            ? `${status.trial_days} days free, then billed. Cancel any time before.`
            : "Cancel any time."}
        </p>

        {error && <p className="mt-3 text-sm font-medium text-danger">{error}</p>}
      </Card>
    </div>
  )
}
