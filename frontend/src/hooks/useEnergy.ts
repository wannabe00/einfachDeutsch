import { useEffect, useState } from "react"
import { useQuery, useQueryClient } from "@tanstack/react-query"

import { fetchEnergy } from "@/api/curriculum"
import { useAuth } from "@/contexts/AuthContext"

/*
 * Live energy for the global meter (Phase 23.6).
 *
 * The server computes regen on read (no background job), so the client only
 * needs to tick the countdown locally and refetch when it reaches zero — that's
 * the moment a new bolt has actually regenerated. Premium users are unlimited,
 * so they never tick.
 */
export function useEnergy() {
  const { user } = useAuth()
  const qc = useQueryClient()

  const { data } = useQuery({
    queryKey: ["energy"],
    queryFn: fetchEnergy,
    enabled: !!user,
    // Cheap safety net if a tab sits idle or the clock drifts.
    refetchInterval: 5 * 60 * 1000,
    refetchOnWindowFocus: true,
  })

  const serverSeconds = data?.seconds_until_next ?? null
  const [remaining, setRemaining] = useState<number | null>(serverSeconds)
  const [seenSeconds, setSeenSeconds] = useState<number | null>(serverSeconds)

  // Restart the countdown whenever the server hands us a fresh value (adjust-
  // state-on-change during render — the lint config forbids setState in effects).
  if (seenSeconds !== serverSeconds) {
    setSeenSeconds(serverSeconds)
    setRemaining(serverSeconds)
  }

  useEffect(() => {
    if (remaining === null || data?.premium) return
    if (remaining <= 0) {
      // A bolt just refilled — ask the server for the authoritative state.
      qc.invalidateQueries({ queryKey: ["energy"] })
      qc.invalidateQueries({ queryKey: ["path"] })
      return
    }
    const id = window.setInterval(() => setRemaining((s) => (s === null ? null : s - 1)), 1000)
    return () => window.clearInterval(id)
  }, [remaining, data?.premium, qc])

  return {
    energy: data,
    /** Ticks down every second; null when full or premium. */
    secondsUntilNext: data?.premium ? null : remaining,
  }
}
