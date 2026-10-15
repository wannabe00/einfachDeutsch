import { useState, type FormEvent } from "react"
import { Link, useNavigate } from "react-router-dom"
import { isAxiosError } from "axios"

import { useAuth } from "@/contexts/AuthContext"
import { isProviderConfigured, startOAuth } from "@/lib/oauth"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { AuthShell, AuthWordmark } from "@/components/auth/AuthShell"
import { AUTH_CARD } from "@/lib/authCard"

export default function AuthPage() {
  const { login } = useAuth()
  const navigate = useNavigate()
  const [username, setUsername] = useState("")
  const [password, setPassword] = useState("")
  const [error, setError] = useState("")
  const [pending, setPending] = useState(false)

  async function handleSubmit(e: FormEvent) {
    e.preventDefault()
    setError("")
    setPending(true)
    try {
      await login(username, password)
      navigate("/")
    } catch (err) {
      let msg = "Unable to log in. Check your username and password."
      if (isAxiosError(err) && err.response?.data) {
        const data = err.response.data as Record<string, unknown>
        const first = Object.values(data)[0]
        if (Array.isArray(first)) msg = String(first[0])
        else if (typeof first === "string") msg = first
      }
      setError(msg)
    } finally {
      setPending(false)
    }
  }

  return (
    <AuthShell maxWidth="max-w-sm">
      <div>
        <AuthWordmark />
        <h1 className="mt-6 text-center text-3xl font-extrabold lg:mt-0 lg:text-left">Willkommen!</h1>
        <p className="mt-1 text-center text-muted-foreground lg:text-left">
          Sign in or create your account.
        </p>

        <div className={`mt-8 flex flex-col gap-3 ${AUTH_CARD}`}>
          {/* Social sign-in (also creates the account on first use) */}
          <SocialButton
            provider="google"
            label="Continue with Google"
            onClick={() => startOAuth("google")}
          />
          <SocialButton
            provider="github"
            label="Continue with GitHub"
            onClick={() => startOAuth("github")}
          />

          <div className="my-2 flex items-center gap-3 text-sm text-muted-foreground">
            <span className="h-px flex-1 bg-border" />
            or log in with username
            <span className="h-px flex-1 bg-border" />
          </div>

          <form onSubmit={handleSubmit} className="flex flex-col gap-3">
            <Input
              value={username}
              onChange={(e) => setUsername(e.target.value)}
              placeholder="Username"
              aria-label="Username"
              autoComplete="username"
              required
            />
            <Input
              type="password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              placeholder="Password"
              aria-label="Password"
              autoComplete="current-password"
              required
            />
            {error && (
              <p className="rounded-xl bg-danger-bg px-3.5 py-2.5 text-sm font-medium text-danger" role="alert">
                {error}
              </p>
            )}
            <Button type="submit" size="lg" disabled={pending}>
              {pending ? "Please wait…" : "Log in"}
            </Button>
            <Link to="/forgot-password" className="self-center text-sm font-semibold text-primary hover:underline">
              Forgot password?
            </Link>
          </form>
        </div>

        <p className="mt-5 text-center text-sm text-muted-foreground">
          New here? Continue with Google or GitHub and we'll set up your
          profile next.
        </p>
      </div>
    </AuthShell>
  )
}

function SocialButton({
  provider,
  label,
  onClick,
}: {
  provider: "google" | "github"
  label: string
  onClick: () => void
}) {
  const configured = isProviderConfigured(provider)
  return (
    <button
      type="button"
      onClick={onClick}
      disabled={!configured}
      title={configured ? undefined : "Sign-in not configured yet"}
      className="flex h-12 items-center justify-center gap-3 rounded-full bg-surface-2 text-[15px] font-semibold transition-colors hover:bg-border disabled:cursor-not-allowed disabled:opacity-50"
    >
      {provider === "google" ? <GoogleMark /> : <GitHubMark />}
      {label}
    </button>
  )
}

function GoogleMark() {
  return (
    <svg className="size-5" viewBox="0 0 24 24" aria-hidden="true">
      <path
        fill="#4285F4"
        d="M22.56 12.25c0-.78-.07-1.53-.2-2.25H12v4.26h5.92a5.06 5.06 0 0 1-2.2 3.32v2.76h3.56c2.08-1.92 3.28-4.74 3.28-8.09Z"
      />
      <path
        fill="#34A853"
        d="M12 23c2.97 0 5.46-.98 7.28-2.66l-3.56-2.76c-.98.66-2.23 1.06-3.72 1.06-2.86 0-5.29-1.93-6.16-4.53H2.18v2.84A11 11 0 0 0 12 23Z"
      />
      <path
        fill="#FBBC05"
        d="M5.84 14.1a6.6 6.6 0 0 1 0-4.2V7.06H2.18a11 11 0 0 0 0 9.88l3.66-2.84Z"
      />
      <path
        fill="#EA4335"
        d="M12 5.38c1.62 0 3.06.56 4.21 1.64l3.15-3.15C17.45 2.09 14.97 1 12 1A11 11 0 0 0 2.18 7.06l3.66 2.84C6.71 7.31 9.14 5.38 12 5.38Z"
      />
    </svg>
  )
}

function GitHubMark() {
  return (
    <svg className="size-5 fill-foreground" viewBox="0 0 24 24" aria-hidden="true">
      <path d="M12 .5A11.5 11.5 0 0 0 .5 12a11.5 11.5 0 0 0 7.86 10.92c.58.1.79-.25.79-.56v-2c-3.2.7-3.88-1.54-3.88-1.54-.53-1.34-1.3-1.7-1.3-1.7-1.06-.72.08-.71.08-.71 1.17.08 1.79 1.2 1.79 1.2 1.04 1.78 2.73 1.27 3.4.97.1-.75.41-1.27.74-1.56-2.56-.29-5.26-1.28-5.26-5.7 0-1.26.45-2.29 1.19-3.1-.12-.29-.52-1.46.11-3.05 0 0 .97-.31 3.18 1.18a11 11 0 0 1 5.8 0c2.2-1.49 3.17-1.18 3.17-1.18.63 1.59.23 2.76.11 3.05.74.81 1.19 1.84 1.19 3.1 0 4.43-2.7 5.41-5.27 5.69.42.36.8 1.08.8 2.18v3.23c0 .31.21.67.8.56A11.5 11.5 0 0 0 23.5 12 11.5 11.5 0 0 0 12 .5Z" />
    </svg>
  )
}
