import { useState, type FormEvent } from "react"
import { Link, useNavigate } from "react-router-dom"
import { isAxiosError } from "axios"

import { useAuth } from "@/contexts/AuthContext"
import { SITE_NAME } from "@/lib/site"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"

interface AuthPageProps {
  mode: "login" | "register"
}

export default function AuthPage({ mode }: AuthPageProps) {
  const { login, register } = useAuth()
  const navigate = useNavigate()
  const [email, setEmail] = useState("")
  const [password, setPassword] = useState("")
  const [username, setUsername] = useState("")
  const [firstName, setFirstName] = useState("")
  const [lastName, setLastName] = useState("")
  const [birthday, setBirthday] = useState("")
  const [phone, setPhone] = useState("")
  const [error, setError] = useState("")
  const [pending, setPending] = useState(false)
  const [sentTo, setSentTo] = useState("")

  const isRegister = mode === "register"

  async function handleSubmit(e: FormEvent) {
    e.preventDefault()
    setError("")
    setPending(true)
    try {
      if (isRegister) {
        const result = await register({
          email,
          password,
          username,
          first_name: firstName,
          last_name: lastName,
          birthday: birthday || undefined,
          phone: phone || undefined,
        })
        if (result.status === "verify_email") {
          setSentTo(email)
          return
        }
      } else {
        await login(email, password)
      }
      navigate("/")
    } catch (err) {
      let msg = "Something went wrong. Please try again."
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
    <div className="flex min-h-screen items-center justify-center bg-background px-4 py-10">
      <div className={isRegister ? "w-full max-w-md" : "w-full max-w-sm"}>
        <h1 className="text-center text-2xl font-semibold tracking-tight">
          {SITE_NAME}
        </h1>
        <p className="mt-1 text-center text-sm text-muted-foreground">
          {isRegister ? "Create your account" : "Welcome back"}
        </p>

        {sentTo ? (
          <div className="mt-8 rounded-xl border border-border bg-surface p-6 text-center">
            <h2 className="text-base font-semibold">Check your email</h2>
            <p className="mt-2 text-sm text-muted-foreground">
              We sent a verification link to{" "}
              <span className="font-medium text-foreground">{sentTo}</span>. Click
              it to activate your account, then log in.
            </p>
            <Link
              to="/login"
              className="mt-4 inline-block text-sm font-medium text-accent hover:underline"
            >
              Back to log in
            </Link>
          </div>
        ) : (
          <form
            onSubmit={handleSubmit}
            className="mt-8 flex flex-col gap-3 rounded-xl border border-border bg-surface p-6"
          >
            <Input
              type="email"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              placeholder="Email"
              aria-label="Email"
              autoComplete="email"
              required
            />

            {isRegister && (
              <>
                <Input
                  value={username}
                  onChange={(e) => setUsername(e.target.value)}
                  placeholder="Username"
                  aria-label="Username"
                  autoComplete="username"
                  required
                />
                <div className="flex gap-3">
                  <Input
                    value={firstName}
                    onChange={(e) => setFirstName(e.target.value)}
                    placeholder="First name"
                    aria-label="First name"
                    autoComplete="given-name"
                    required
                  />
                  <Input
                    value={lastName}
                    onChange={(e) => setLastName(e.target.value)}
                    placeholder="Surname"
                    aria-label="Surname"
                    autoComplete="family-name"
                    required
                  />
                </div>
                <label className="text-xs text-muted-foreground">
                  Birthday
                  <Input
                    type="date"
                    value={birthday}
                    onChange={(e) => setBirthday(e.target.value)}
                    aria-label="Birthday"
                    className="mt-1"
                    required
                  />
                </label>
                <Input
                  type="tel"
                  value={phone}
                  onChange={(e) => setPhone(e.target.value)}
                  placeholder="Phone (optional)"
                  aria-label="Phone"
                  autoComplete="tel"
                />
              </>
            )}

            <Input
              type="password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              placeholder="Password"
              aria-label="Password"
              autoComplete={isRegister ? "new-password" : "current-password"}
              required
            />
            {error && <p className="text-sm text-[hsl(var(--danger))]">{error}</p>}
            <Button type="submit" disabled={pending} className="mt-1">
              {pending
                ? "Please wait…"
                : isRegister
                  ? "Create account"
                  : "Log in"}
            </Button>
          </form>
        )}

        <p className="mt-4 text-center text-sm text-muted-foreground">
          {isRegister ? (
            <>
              Already have an account?{" "}
              <Link to="/login" className="font-medium text-accent hover:underline">
                Log in
              </Link>
            </>
          ) : (
            <>
              New here?{" "}
              <Link to="/register" className="font-medium text-accent hover:underline">
                Create an account
              </Link>
            </>
          )}
        </p>
      </div>
    </div>
  )
}
