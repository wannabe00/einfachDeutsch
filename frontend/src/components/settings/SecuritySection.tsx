import { useState } from "react"
import { useNavigate } from "react-router-dom"

import { TOKEN_KEY } from "@/api/client"
import { changePassword, logoutAllDevices } from "@/api/account"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { errorText } from "@/lib/apiError"
import { Field, Msg, Section } from "./primitives"

/** Change password + log out of all devices. */
export function SecuritySection() {
  const navigate = useNavigate()
  const [oldPw, setOldPw] = useState("")
  const [newPw, setNewPw] = useState("")
  const [msg, setMsg] = useState("")
  const [error, setError] = useState("")

  async function savePassword() {
    setMsg("")
    setError("")
    if (newPw.length < 8) {
      setError("New password must be at least 8 characters.")
      return
    }
    try {
      await changePassword(oldPw, newPw)
      setOldPw("")
      setNewPw("")
      setMsg("Password changed.")
    } catch (e) {
      setError(errorText(e))
    }
  }

  async function handleLogoutAll() {
    await logoutAllDevices().catch(() => {})
    localStorage.removeItem(TOKEN_KEY)
    navigate("/login")
  }

  return (
    <Section title="Security">
      <div className="grid gap-3 sm:grid-cols-2">
        <Field label="Current password">
          <Input type="password" value={oldPw} onChange={(e) => setOldPw(e.target.value)} autoComplete="current-password" />
        </Field>
        <Field label="New password">
          <Input type="password" value={newPw} onChange={(e) => setNewPw(e.target.value)} autoComplete="new-password" />
        </Field>
      </div>
      {error && <Msg tone="danger">{error}</Msg>}
      {msg && <Msg tone="success">{msg}</Msg>}
      <div className="mt-3 flex flex-wrap gap-2">
        <Button onClick={savePassword}>Change password</Button>
        <Button variant="outline" onClick={handleLogoutAll}>
          Log out of all devices
        </Button>
      </div>
    </Section>
  )
}
