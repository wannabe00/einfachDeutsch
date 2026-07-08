import { useState } from "react"
import { useNavigate } from "react-router-dom"
import { useQueryClient } from "@tanstack/react-query"

import { useAuth } from "@/contexts/AuthContext"
import { TOKEN_KEY } from "@/api/client"
import { deactivateAccount, deleteAccount, resetProgress } from "@/api/account"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { errorText } from "@/lib/apiError"
import { Msg, Section } from "./primitives"

type Action = "reset" | "deactivate" | "delete"

const CONFIRM: Record<Action, string> = {
  reset: "Reset ALL your learning progress (reviews, streaks, completed lessons)? This cannot be undone.",
  deactivate: "Deactivate your account? You won't be able to log in until an admin re-enables it.",
  delete: "Permanently delete your account and all data? This cannot be undone.",
}

/** Reset progress, deactivate, or permanently delete the account. Each action
    requires the account password (server-enforced, AUDIT S2) and surfaces real
    errors instead of silently reporting success (B2). */
export function DangerZoneSection() {
  const { logout } = useAuth()
  const navigate = useNavigate()
  const qc = useQueryClient()
  const [password, setPassword] = useState("")
  const [pending, setPending] = useState<Action | null>(null)
  const [msg, setMsg] = useState("")
  const [error, setError] = useState("")

  async function run(action: Action) {
    setMsg("")
    setError("")
    if (!password) {
      setError("Enter your password to confirm.")
      return
    }
    if (!window.confirm(CONFIRM[action])) return
    setPending(action)
    try {
      if (action === "reset") {
        await resetProgress(password)
        qc.invalidateQueries()
        setPassword("")
        setMsg("Progress reset.")
      } else if (action === "deactivate") {
        await deactivateAccount(password)
        await logout()
        navigate("/")
      } else {
        await deleteAccount(password)
        localStorage.removeItem(TOKEN_KEY)
        navigate("/")
      }
    } catch (e) {
      setError(errorText(e))
    } finally {
      setPending(null)
    }
  }

  return (
    <Section title="Danger zone" danger>
      <p className="mb-3 text-xs text-muted-foreground">
        These actions require your password.
      </p>
      <Input
        type="password"
        value={password}
        onChange={(e) => setPassword(e.target.value)}
        placeholder="Your password"
        autoComplete="current-password"
        className="mb-3 max-w-xs"
      />
      <div className="flex flex-col divide-y divide-border">
        <Row
          label="Reset all learning progress"
          button="Reset progress"
          onClick={() => run("reset")}
          busy={pending === "reset"}
          disabled={pending !== null}
        />
        <Row
          label="Deactivate account (reversible by an admin)"
          button="Deactivate"
          onClick={() => run("deactivate")}
          busy={pending === "deactivate"}
          disabled={pending !== null}
        />
        <Row
          label="Delete account permanently"
          button="Delete account"
          onClick={() => run("delete")}
          busy={pending === "delete"}
          disabled={pending !== null}
        />
      </div>
      {error && <Msg tone="danger">{error}</Msg>}
      {msg && <Msg tone="success">{msg}</Msg>}
    </Section>
  )
}

function Row({
  label,
  button,
  onClick,
  busy,
  disabled,
}: {
  label: string
  button: string
  onClick: () => void
  busy: boolean
  disabled: boolean
}) {
  return (
    <div className="flex flex-wrap items-center justify-between gap-3 py-3 first:pt-0 last:pb-0">
      <span className="text-sm">{label}</span>
      <Button variant="destructive" onClick={onClick} disabled={disabled}>
        {busy ? "Working…" : button}
      </Button>
    </div>
  )
}
