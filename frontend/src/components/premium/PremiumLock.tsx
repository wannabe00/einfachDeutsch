import { useState, type ReactNode } from "react"
import { useQuery, useQueryClient } from "@tanstack/react-query"
import { Sparkles, Zap } from "lucide-react"

import { fetchPremiumStatus, startTrial } from "@/api/premium"
import { useAuth } from "@/contexts/AuthContext"
import { Button } from "@/components/ui/button"
import { SectionCard } from "@/components/ui/SectionCard"

/*
 * The premium upsell (Phase 23.7). Mirrors `LockedFeature` (which gates on
 * *login*) but gates on *premium*: AI Assistant, AI explanations and Recite are
 * the paid tier per Spec v3, since they spend the owner's Gemini quota.
 *
 * The backend is the real gate (`IsPremium` → 403); this is only the UI, so
 * showing the content blurred behind it is safe.
 */
export function PremiumLock({
  children,
  title = "Premium feature",
  description,
}: {
  /** Shown blurred behind the upsell, so users see what they're missing. */
  children?: ReactNode
  title?: string
  description?: string
}) {
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
    <div className="relative min-h-[60vh]">
      {children && (
        <div aria-hidden className="pointer-events-none select-none opacity-40 blur-[3px]">
          {children}
        </div>
      )}

      <div className="absolute inset-0 flex items-start justify-center pt-10">
        <div className="w-full max-w-md">
          <SectionCard accent="hsl(var(--brand))" glow>
            <div className="p-8 text-center">
              <span
                className="mx-auto flex size-12 items-center justify-center rounded-xl"
                style={{ background: "hsl(var(--brand)/0.15)", color: "hsl(var(--brand))" }}
              >
                <Sparkles className="size-6" />
              </span>
              <h2 className="mt-4 text-2xl font-bold">{title}</h2>
              <p className="mt-2 text-sm text-muted-foreground">
                {description ??
                  "The AI Assistant, AI explanations and Recite are part of Premium — along with unlimited energy."}
              </p>

              <ul className="mx-auto mt-5 w-fit space-y-1.5 text-left text-sm">
                <Perk icon={<Zap className="size-4" />}>Unlimited energy</Perk>
                <Perk icon={<Sparkles className="size-4" />}>AI Assistant &amp; explanations</Perk>
                <Perk icon={<Sparkles className="size-4" />}>Recite — speak &amp; get scored</Perk>
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
                  Paid plans aren’t live yet — premium is granted manually for now.
                </p>
              )}

              {error && <p className="mt-3 text-sm text-[hsl(var(--danger))]">{error}</p>}
            </div>
          </SectionCard>
        </div>
      </div>
    </div>
  )
}

function Perk({ icon, children }: { icon: ReactNode; children: ReactNode }) {
  return (
    <li className="flex items-center gap-2 text-muted-foreground">
      <span style={{ color: "hsl(var(--brand))" }}>{icon}</span>
      {children}
    </li>
  )
}
