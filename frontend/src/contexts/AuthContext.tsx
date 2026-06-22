import {
  createContext,
  useCallback,
  useContext,
  useEffect,
  useState,
  type ReactNode,
} from "react"

import { TOKEN_KEY } from "@/api/client"
import {
  completeOnboarding,
  fetchCurrentUser,
  loginUser,
  logoutUser,
  socialLogin,
  type OnboardingPayload,
  type SocialProvider,
} from "@/api/auth"
import type { User } from "@/types"

interface AuthContextValue {
  user: User | null
  loading: boolean
  login: (username: string, password: string) => Promise<void>
  loginWithCode: (provider: SocialProvider, code: string) => Promise<void>
  completeProfile: (payload: OnboardingPayload) => Promise<void>
  logout: () => Promise<void>
  refreshUser: () => Promise<void>
}

const AuthContext = createContext<AuthContextValue | null>(null)

export function AuthProvider({ children }: { children: ReactNode }) {
  const [user, setUser] = useState<User | null>(null)
  const [loading, setLoading] = useState(true)

  // On mount, if a token exists, resolve the current user.
  useEffect(() => {
    let active = true
    async function bootstrap() {
      if (!localStorage.getItem(TOKEN_KEY)) {
        setLoading(false)
        return
      }
      try {
        const u = await fetchCurrentUser()
        if (active) setUser(u)
      } catch {
        localStorage.removeItem(TOKEN_KEY)
      } finally {
        if (active) setLoading(false)
      }
    }
    bootstrap()
    return () => {
      active = false
    }
  }, [])

  // The Axios 401 interceptor fires this when a token goes stale.
  useEffect(() => {
    const onLogout = () => setUser(null)
    window.addEventListener("auth:logout", onLogout)
    return () => window.removeEventListener("auth:logout", onLogout)
  }, [])

  const login = useCallback(async (username: string, password: string) => {
    await loginUser(username, password)
    setUser(await fetchCurrentUser())
  }, [])

  const loginWithCode = useCallback(
    async (provider: SocialProvider, code: string) => {
      await socialLogin(provider, code)
      setUser(await fetchCurrentUser())
    },
    [],
  )

  const completeProfile = useCallback(async (payload: OnboardingPayload) => {
    const updated = await completeOnboarding(payload)
    setUser(updated)
  }, [])

  const logout = useCallback(async () => {
    await logoutUser()
    setUser(null)
  }, [])

  const refreshUser = useCallback(async () => {
    setUser(await fetchCurrentUser())
  }, [])

  return (
    <AuthContext.Provider
      value={{ user, loading, login, loginWithCode, completeProfile, logout, refreshUser }}
    >
      {children}
    </AuthContext.Provider>
  )
}

// eslint-disable-next-line react-refresh/only-export-components
export function useAuth() {
  const ctx = useContext(AuthContext)
  if (!ctx) throw new Error("useAuth must be used within AuthProvider")
  return ctx
}
