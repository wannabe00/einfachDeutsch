import { useEffect, useRef, useState } from "react"
import { Link, useNavigate, useParams, useSearchParams } from "react-router-dom"

import { useAuth } from "@/contexts/AuthContext"
import { consumeState } from "@/lib/oauth"
import type { SocialProvider } from "@/api/auth"

/** Landing spot after Google/GitHub redirect back: trade the `code` for a token. */
export default function OAuthCallbackPage() {
  const { provider } = useParams<{ provider: string }>()
  const [params] = useSearchParams()
  const { loginWithCode } = useAuth()
  const navigate = useNavigate()
  const [error, setError] = useState("")
  const ran = useRef(false)

  useEffect(() => {
    // Guard against React StrictMode double-invoke (the code is single-use).
    if (ran.current) return
    ran.current = true

    const p = provider as SocialProvider
    const code = params.get("code")
    const state = params.get("state")
    const denied = params.get("error")

    async function run() {
      if (denied) return setError("Sign-in was cancelled.")
      if (p !== "google" && p !== "github")
        return setError("Unknown sign-in provider.")
      if (!code) return setError("No authorization code was returned.")
      if (!consumeState(p, state))
        return setError("Sign-in could not be verified. Please try again.")
      try {
        await loginWithCode(p, code)
        navigate("/", { replace: true })
      } catch {
        setError("Sign-in failed. Please try again.")
      }
    }

    void run()
  }, [provider, params, loginWithCode, navigate])

  return (
    <div className="flex min-h-screen items-center justify-center px-4 text-center">
      {error ? (
        <div>
          <p className="text-sm text-[hsl(var(--danger))]">{error}</p>
          <Link
            to="/login"
            className="mt-3 inline-block text-sm font-medium text-accent hover:underline"
          >
            Back to sign in
          </Link>
        </div>
      ) : (
        <p className="text-sm text-muted-foreground">Signing you in…</p>
      )}
    </div>
  )
}
