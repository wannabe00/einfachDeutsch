import { useState } from "react"
import { useNavigate } from "react-router-dom"
import { useQueryClient } from "@tanstack/react-query"

import { useAuth } from "@/contexts/AuthContext"
import { TOKEN_KEY } from "@/api/client"
import { deactivateAccount, deleteAccount, resetProgress } from "@/api/account"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { errorText } from "@/lib/apiError"
import { Field, Msg, Section } from "./primitives"

/** Reset progress, deactivate, or permanently delete the account. */
export function DangerZoneSection() {
  const { logout } = useAuth()
  const navigate = useNavigate()
  const qc = useQueryClient()
  const [deletePw, setDeletePw] = useState("")
  const [msg, setMsg] = useState("")
  const [error, setError] = useState("")

  async function handleReset() {
    if (!window.confirm("Reset ALL your learning progress (reviews, streaks, completed lessons)? This cannot be undone.")) return
    await resetProgress().catch(() => {})
    qc.invalidateQueries()
    setMsg("Progress reset.")
  }

  async function handleDeactivate() {
    if (!window.confirm("Deactivate your account? You won't be able to log in until an admin re-enables it.")) return
    await deactivateAccount().catch(() => {})
    await logout()
    navigate("/")
  }

  async function handleDelete() {
    if (!window.confirm("Permanently delete your account and all data? This cannot be undone.")) return
    try {
      await deleteAccount(deletePw || undefined)
      localStorage.removeItem(TOKEN_KEY)
      navigate("/")
    } catch (e) {
      setError(errorText(e))
    }
  }

  return (
    <Section title="Danger zone" danger>
      <div className="flex flex-col gap-4">
        <div className="flex flex-wrap items-center justify-between gap-2">
          <span className="text-sm">Reset all learning progress</span>
          <Button variant="destructive" onClick={handleReset}>
            Reset progress
          </Button>
        </div>
        <div className="flex flex-wrap items-center justify-between gap-2">
          <span className="text-sm">Deactivate account (reversible by an admin)</span>
          <Button variant="destructive" onClick={handleDeactivate}>
            Deactivate
          </Button>
        </div>
        <div className="flex flex-wrap items-end justify-between gap-2">
          <Field label="Delete account permanently — confirm with your password">
            <Input
              type="password"
              value={deletePw}
              onChange={(e) => setDeletePw(e.target.value)}
              placeholder="Password"
              className="max-w-xs"
            />
          </Field>
          <Button variant="destructive" onClick={handleDelete}>
            Delete account
          </Button>
        </div>
      </div>
      {error && <Msg tone="danger">{error}</Msg>}
      {msg && <Msg tone="success">{msg}</Msg>}
    </Section>
  )
}
