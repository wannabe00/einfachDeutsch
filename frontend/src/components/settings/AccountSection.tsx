import { useState } from "react"
import { Link, useNavigate } from "react-router-dom"
import { useQueryClient } from "@tanstack/react-query"

import { useAuth } from "@/contexts/AuthContext"
import { TOKEN_KEY } from "@/api/client"
import { deactivateAccount, deleteAccount, exportMyData, resetProgress } from "@/api/account"
import { Button } from "@/components/ui/button"
import { Msg, Section } from "./primitives"
import { PasswordDialog } from "./PasswordDialog"

type Action = "reset" | "deactivate" | "delete"

const ACTIONS: Record<Action, { label: string; hint: string; button: string; confirm: string }> = {
  reset: {
    label: "Reset learning progress",
    hint: "Reviews, streaks, finished lessons and scores. Your account stays.",
    button: "Reset progress",
    confirm: "This resets ALL your learning progress and can't be undone.",
  },
  deactivate: {
    label: "Deactivate account",
    hint: "You can't log in until an admin turns it back on.",
    button: "Deactivate",
    confirm: "You'll be logged out and can't log in again until an admin re-enables your account.",
  },
  delete: {
    label: "Delete account",
    hint: "Your account and all your data, permanently.",
    button: "Delete account",
    confirm: "This permanently deletes your account and all your data. It can't be undone.",
  },
}

/** Your data (export, privacy policy), then the actions that can't be undone.
    Each red button asks for the password in a dialog (checked by the server). */
export function AccountSection() {
  const { logout } = useAuth()
  const navigate = useNavigate()
  const qc = useQueryClient()
  const [open, setOpen] = useState<Action | null>(null)
  const [msg, setMsg] = useState("")

  async function handleExport() {
    const data = await exportMyData()
    const blob = new Blob([JSON.stringify(data, null, 2)], { type: "application/json" })
    const url = URL.createObjectURL(blob)
    const a = document.createElement("a")
    a.href = url
    a.download = "my-data.json"
    a.click()
    URL.revokeObjectURL(url)
  }

  async function run(action: Action, password: string) {
    if (action === "reset") {
      await resetProgress(password)
      qc.invalidateQueries()
      setOpen(null)
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
  }

  return (
    <>
      <Section title="Your data">
        <p className="mb-3 text-sm text-muted-foreground">
          Download everything we store about you as a JSON file.
        </p>
        <div className="flex flex-wrap gap-2">
          <Button variant="outline" onClick={handleExport}>
            Export my data
          </Button>
          <Button variant="outline" asChild>
            <Link to="/privacy">Privacy policy</Link>
          </Button>
          <Button variant="outline" asChild>
            <Link to="/terms">Terms</Link>
          </Button>
        </div>
      </Section>

      <Section title="Can't be undone" danger>
        <div className="flex flex-col divide-y divide-border">
          {(Object.keys(ACTIONS) as Action[]).map((action) => (
            <div key={action} className="flex flex-wrap items-center justify-between gap-3 py-3 first:pt-0 last:pb-0">
              <span className="min-w-0">
                <span className="block text-[15px] font-semibold">{ACTIONS[action].label}</span>
                <span className="block text-sm text-muted-foreground">{ACTIONS[action].hint}</span>
              </span>
              <Button variant="destructive" onClick={() => setOpen(action)}>
                {ACTIONS[action].button}
              </Button>
            </div>
          ))}
        </div>
        {msg && <Msg tone="success">{msg}</Msg>}
      </Section>

      {open && (
        <PasswordDialog
          title={ACTIONS[open].label}
          description={ACTIONS[open].confirm}
          confirmLabel={ACTIONS[open].button}
          danger
          onConfirm={(password) => run(open, password)}
          onClose={() => setOpen(null)}
        />
      )}
    </>
  )
}
