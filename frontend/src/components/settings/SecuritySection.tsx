import { useState } from "react"
import { useNavigate } from "react-router-dom"
import QRCode from "qrcode"
import { Check, Copy, ShieldCheck } from "lucide-react"

import { useAuth } from "@/contexts/AuthContext"
import { TOKEN_KEY } from "@/api/client"
import {
  changePassword,
  logoutAllDevices,
  newBackupCodes,
  twoFactorDisable,
  twoFactorEnable,
  twoFactorSetup,
} from "@/api/account"
import { errorText } from "@/lib/apiError"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { Field, Msg, Section } from "./primitives"
import { PasswordDialog } from "./PasswordDialog"

/** Password, two-factor login and signed-in devices. */
export function SecuritySection() {
  return (
    <>
      <PasswordCard />
      <TwoFactorCard />
      <DevicesCard />
    </>
  )
}

/** Change password (revealed by a button, confirm field required). */
function PasswordCard() {
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

  return (
    <Section title="Password">
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
          <p className="mb-3 text-sm text-muted-foreground">Used when you log in with your username instead of Google or GitHub.</p>
          {msg && <Msg tone="success">{msg}</Msg>}
          <Button variant="outline" className="self-start" onClick={() => setEditing(true)}>
            Change password
          </Button>
        </>
      )}
    </Section>
  )
}

type Dialog = null | "enable" | "disable" | "codes"

/** Authenticator-app codes on username + password logins, with backup codes. */
function TwoFactorCard() {
  const { user, refreshUser } = useAuth()
  const on = !!user?.two_factor
  const [setup, setSetup] = useState<{ secret: string; qr: string } | null>(null)
  const [code, setCode] = useState("")
  const [dialog, setDialog] = useState<Dialog>(null)
  const [codes, setCodes] = useState<string[] | null>(null)
  const [error, setError] = useState("")

  async function start() {
    setError("")
    try {
      const { secret, uri } = await twoFactorSetup()
      setSetup({ secret, qr: await QRCode.toDataURL(uri, { margin: 1, width: 200 }) })
    } catch (e) {
      setError(errorText(e))
    }
  }

  async function confirm(password: string) {
    if (dialog === "enable") {
      setCodes(await twoFactorEnable(code.trim(), password))
      setSetup(null)
      setCode("")
    } else if (dialog === "codes") {
      setCodes(await newBackupCodes(password))
    } else {
      await twoFactorDisable(password)
      setCodes(null)
    }
    setDialog(null)
    await refreshUser()
  }

  return (
    <Section title="Two-factor login">
      <div className="flex items-start gap-3">
        <span className="flex size-10 shrink-0 items-center justify-center rounded-xl bg-surface-2 text-muted-foreground">
          <ShieldCheck className="size-5" aria-hidden="true" />
        </span>
        <p className="text-sm text-muted-foreground">
          {on
            ? "On. Username logins also ask for a code from your authenticator app."
            : "Ask for a code from an authenticator app (Google Authenticator, 1Password, Authy…) when you log in with your username. Google and GitHub logins use their own 2FA."}
        </p>
      </div>

      {codes && <BackupCodes codes={codes} onDone={() => setCodes(null)} />}

      {!on && !setup && (
        <Button className="mt-4 self-start" onClick={start}>
          Set up two-factor login
        </Button>
      )}

      {!on && setup && (
        <div className="mt-4 flex flex-col gap-4 rounded-2xl bg-surface-2 p-4 sm:flex-row sm:items-start">
          <img src={setup.qr} alt="QR code for your authenticator app" className="size-[200px] shrink-0 rounded-xl bg-white" />
          <div className="flex min-w-0 flex-col gap-3">
            <p className="text-sm">
              1. Scan the code with your authenticator app, or enter this key:
              <code className="mt-1 block break-all rounded-lg bg-surface px-2 py-1 font-mono text-[13px]">{setup.secret}</code>
            </p>
            <Field label="2. Enter the 6-digit code it shows">
              <Input value={code} onChange={(e) => setCode(e.target.value)} inputMode="numeric" autoComplete="one-time-code" placeholder="123 456" />
            </Field>
            <div className="flex flex-wrap gap-2">
              <Button disabled={code.replace(/\s/g, "").length !== 6} onClick={() => setDialog("enable")}>
                Turn on
              </Button>
              <Button variant="outline" onClick={() => setSetup(null)}>
                Cancel
              </Button>
            </div>
          </div>
        </div>
      )}

      {on && !codes && (
        <div className="mt-4 flex flex-wrap gap-2">
          <Button variant="outline" onClick={() => setDialog("codes")}>
            New backup codes
          </Button>
          <Button variant="outline" onClick={() => setDialog("disable")}>
            Turn off
          </Button>
        </div>
      )}
      {error && <Msg tone="danger">{error}</Msg>}

      {dialog && (
        <PasswordDialog
          title={{ enable: "Turn on two-factor login", disable: "Turn off two-factor login", codes: "New backup codes" }[dialog]}
          description={
            dialog === "codes"
              ? "Your old backup codes stop working."
              : dialog === "disable"
                ? "Username logins will only need your password again."
                : "Confirm it's you."
          }
          confirmLabel={{ enable: "Turn on", disable: "Turn off", codes: "Make new codes" }[dialog]}
          danger={dialog === "disable"}
          onConfirm={confirm}
          onClose={() => setDialog(null)}
        />
      )}
    </Section>
  )
}

/** Shown once: each code logs you in one time if you lose your phone. */
function BackupCodes({ codes, onDone }: { codes: string[]; onDone: () => void }) {
  const [copied, setCopied] = useState(false)
  async function copy() {
    await navigator.clipboard.writeText(codes.join("\n")).catch(() => {})
    setCopied(true)
  }
  return (
    <div className="mt-4 rounded-2xl bg-surface-2 p-4">
      <p className="font-semibold">Save your backup codes</p>
      <p className="mt-1 text-sm text-muted-foreground">
        Each one logs you in once if you lose your phone. They won't be shown again.
      </p>
      <ul className="mt-3 grid grid-cols-2 gap-2 font-mono text-[15px] sm:grid-cols-4">
        {codes.map((c) => (
          <li key={c} className="rounded-lg bg-surface px-2 py-1.5 text-center">{c}</li>
        ))}
      </ul>
      <div className="mt-3 flex flex-wrap gap-2">
        <Button variant="outline" onClick={copy}>
          {copied ? <Check className="size-4" /> : <Copy className="size-4" />} {copied ? "Copied" : "Copy"}
        </Button>
        <Button onClick={onDone}>I saved them</Button>
      </div>
    </div>
  )
}

function DevicesCard() {
  const navigate = useNavigate()
  async function handleLogoutAll() {
    await logoutAllDevices().catch(() => {})
    localStorage.removeItem(TOKEN_KEY)
    navigate("/login")
  }
  return (
    <Section title="Signed-in devices">
      <p className="mb-3 text-sm text-muted-foreground">
        Lost a phone or used a shared computer? Sign out everywhere, including here.
      </p>
      <Button variant="outline" className="self-start" onClick={handleLogoutAll}>
        Log out of all devices
      </Button>
    </Section>
  )
}
