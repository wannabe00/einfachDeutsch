import { useState, type FormEvent } from "react"
import { useNavigate } from "react-router-dom"
import { isAxiosError } from "axios"

import { useAuth } from "@/contexts/AuthContext"
import { SITE_NAME } from "@/lib/site"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"

/** First-run profile setup shown after a social sign-in (profile_complete=false).
    Sets username + password (so username login works) + name; birthday/phone
    optional. Afterwards the level onboarding takes over. */
export default function WelcomePage() {
  const { user, completeProfile } = useAuth()
  const navigate = useNavigate()
  const [username, setUsername] = useState(user?.username ?? "")
  const [password, setPassword] = useState("")
  const [firstName, setFirstName] = useState(user?.first_name ?? "")
  const [lastName, setLastName] = useState(user?.last_name ?? "")
  const [birthday, setBirthday] = useState("")
  const [phone, setPhone] = useState("")
  const [error, setError] = useState("")
  const [pending, setPending] = useState(false)

  async function handleSubmit(e: FormEvent) {
    e.preventDefault()
    setError("")
    if (password.length < 8) {
      setError("Password must be at least 8 characters.")
      return
    }
    setPending(true)
    try {
      await completeProfile({
        username: username.trim(),
        password,
        first_name: firstName.trim(),
        last_name: lastName.trim(),
        birthday: birthday || undefined,
        phone: phone || undefined,
      })
      // Level onboarding (and the rest of the app) is gated downstream.
      navigate("/", { replace: true })
    } catch (err) {
      let msg = "Could not save your profile. Please try again."
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
      <div className="w-full max-w-md">
        <h1 className="text-center text-2xl font-semibold tracking-tight">
          Welcome to {SITE_NAME}
        </h1>
        <p className="mt-1 text-center text-sm text-muted-foreground">
          Set up your profile. Your password lets you log in without Google or
          GitHub too.
        </p>

        <form
          onSubmit={handleSubmit}
          className="mt-8 flex flex-col gap-3 rounded-xl border border-border bg-surface p-6"
        >
          <Input
            value={username}
            onChange={(e) => setUsername(e.target.value)}
            placeholder="Username (nickname)"
            aria-label="Username"
            autoComplete="username"
            required
          />
          <Input
            type="password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            placeholder="Password (min 8 characters)"
            aria-label="Password"
            autoComplete="new-password"
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
            Birthday (optional)
            <Input
              type="date"
              value={birthday}
              onChange={(e) => setBirthday(e.target.value)}
              aria-label="Birthday"
              className="mt-1"
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
          {error && <p className="text-sm text-[hsl(var(--danger))]">{error}</p>}
          <Button type="submit" disabled={pending} className="mt-1">
            {pending ? "Saving…" : "Continue"}
          </Button>
        </form>
      </div>
    </div>
  )
}
