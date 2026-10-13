import { useEffect, useRef, useState } from "react"
import { Link, useNavigate, useParams, useSearchParams } from "react-router-dom"

import { Loader2 } from "lucide-react"

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
    <div className="flex min-h-screen items-center justify-center bg-background px-4 text-center">
      {error ? (
        <div className="w-full max-w-sm rounded-[28px] bg-surface p-8 shadow-card">
          <p className="text-lg font-bold">Couldn’t sign you in</p>
          <p className="mt-1 text-muted-foreground">{error}</p>
          <Link
            to="/login"
            className="mt-6 inline-flex h-11 items-center rounded-full bg-primary px-6 font-semibold text-primary-foreground transition hover:brightness-110"
          >
            Back to sign in
          </Link>
        </div>
      ) : (
        <p className="flex items-center gap-3 font-medium text-muted-foreground">
          <Loader2 className="size-5 animate-spin" aria-hidden="true" /> Signing you in…
        </p>
      )}
    </div>
  )
}
