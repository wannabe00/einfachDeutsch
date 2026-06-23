import { useState } from "react"
import { useNavigate } from "react-router-dom"

import { TOKEN_KEY } from "@/api/client"
import { changePassword, logoutAllDevices } from "@/api/account"
import { errorText } from "@/lib/apiError"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { Field, Msg, Section } from "./primitives"

/** Change password (revealed by a button, confirm field required) + log out
    of all devices. */
export function SecuritySection() {
  const navigate = useNavigate()
  const [editing, setEditing] = useState(false)
  const [oldPw, setOldPw] = useState("")
  const [newPw, setNewPw] = useState("")
  const [confirmPw, setConfirmPw] = useState("")
  const [msg, setMsg] = useState("")
  const [error, setError] = useState("")

  function closeForm() {
    setEditing(false)
    setOldPw("")
    setNewPw("")
    setConfirmPw("")
    setError("")
  }

  async function savePassword() {
    setMsg("")
    setError("")
    if (newPw.length < 8) {
      setError("New password must be at least 8 characters.")
      return
    }
    if (newPw !== confirmPw) {
      setError("The two new passwords don't match.")
      return
    }
    try {
      await changePassword(oldPw, newPw)
      closeForm()
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
      {editing ? (
        <>
          <div className="grid gap-3 sm:grid-cols-3">
            <Field label="Current password">
              <Input type="password" value={oldPw} onChange={(e) => setOldPw(e.target.value)} autoComplete="current-password" />
            </Field>
            <Field label="New password">
              <Input type="password" value={newPw} onChange={(e) => setNewPw(e.target.value)} autoComplete="new-password" />
            </Field>
            <Field label="Confirm new password">
              <Input type="password" value={confirmPw} onChange={(e) => setConfirmPw(e.target.value)} autoComplete="new-password" />
            </Field>
          </div>
          {error && <Msg tone="danger">{error}</Msg>}
          <div className="mt-3 flex flex-wrap gap-2">
            <Button onClick={savePassword}>Save new password</Button>
            <Button variant="outline" onClick={closeForm}>
              Cancel
            </Button>
          </div>
        </>
      ) : (
        <>
          {msg && <Msg tone="success">{msg}</Msg>}
          <div className="flex flex-wrap gap-2">
            <Button variant="outline" onClick={() => setEditing(true)}>
              Change password
            </Button>
            <Button variant="outline" onClick={handleLogoutAll}>
              Log out of all devices
            </Button>
          </div>
        </>
      )}
    </Section>
  )
}
