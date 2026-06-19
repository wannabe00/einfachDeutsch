import {
  createContext,
  useCallback,
  useContext,
  useState,
  type ReactNode,
} from "react"

import { useAuth } from "@/contexts/AuthContext"
import { guestLimitReached, recordGuestAction } from "@/lib/guestLimit"
import { SignUpWall } from "@/components/auth/SignUpWall"

interface GuestLimitContextValue {
  /**
   * Call before performing a counted action. Signed-in users are always
   * allowed. For a guest it records the action and returns true if they're
   * still under the daily cap; once the cap is hit it opens the sign-up wall
   * and returns false (the caller should abort the action).
   */
  guard: () => boolean
}

const GuestLimitContext = createContext<GuestLimitContextValue | null>(null)

export function GuestLimitProvider({ children }: { children: ReactNode }) {
  const { user } = useAuth()
  const [wallOpen, setWallOpen] = useState(false)

  const guard = useCallback(() => {
    if (user) return true // signed-in: unlimited
    if (guestLimitReached()) {
      setWallOpen(true)
      return false
    }
    recordGuestAction()
    return true
  }, [user])

  return (
    <GuestLimitContext.Provider value={{ guard }}>
      {children}
      <SignUpWall open={wallOpen} onClose={() => setWallOpen(false)} />
    </GuestLimitContext.Provider>
  )
}

// eslint-disable-next-line react-refresh/only-export-components
export function useGuestLimit() {
  const ctx = useContext(GuestLimitContext)
  if (!ctx) throw new Error("useGuestLimit must be used within GuestLimitProvider")
  return ctx
}
