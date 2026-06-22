import { useRef, useState, type ReactNode } from "react"
import { Link, useNavigate } from "react-router-dom"
import { useQueryClient } from "@tanstack/react-query"
import { isAxiosError } from "axios"

import { useAuth } from "@/contexts/AuthContext"
import { TOKEN_KEY } from "@/api/client"
import {
  changePassword,
  deactivateAccount,
  deleteAccount,
  exportMyData,
  logoutAllDevices,
  resetProgress,
  updateProfile,
  uploadAvatar,
} from "@/api/account"
import { ThemeToggle } from "@/components/layout/ThemeToggle"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { cn } from "@/lib/utils"

const WEEKDAYS = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]

function err(e: unknown): string {
  if (isAxiosError(e) && e.response?.data) {
    const d = e.response.data as Record<string, unknown>
    const first = Object.values(d)[0]
    if (Array.isArray(first)) return String(first[0])
    if (typeof first === "string") return first
  }
  return "Something went wrong."
}

export default function SettingsPage() {
  const { user, refreshUser, logout } = useAuth()
  const navigate = useNavigate()
  const qc = useQueryClient()

  // Profile
  const [firstName, setFirstName] = useState(user?.first_name ?? "")
  const [lastName, setLastName] = useState(user?.last_name ?? "")
  const [usernameField, setUsernameField] = useState(user?.username ?? "")
  const [birthday, setBirthday] = useState(user?.birthday ?? "")
  const [phone, setPhone] = useState(user?.phone ?? "")
  const [profileMsg, setProfileMsg] = useState("")
  const [profileErr, setProfileErr] = useState("")
  const avatarInput = useRef<HTMLInputElement>(null)

  // Security
  const [oldPw, setOldPw] = useState("")
  const [newPw, setNewPw] = useState("")
  const [pwMsg, setPwMsg] = useState("")
  const [pwErr, setPwErr] = useState("")

  // Account
  const [deletePw, setDeletePw] = useState("")

  // Preferences
  const prefs = (user?.preferences ?? {}) as Record<string, unknown>
  const [dailyGoal, setDailyGoal] = useState(String(prefs.daily_goal ?? 20))
  const [reminder, setReminder] = useState(String(prefs.reminder_time ?? ""))
  const [weekdays, setWeekdays] = useState<number[]>(
    Array.isArray(prefs.weekdays) ? (prefs.weekdays as number[]) : [0, 2, 4],
  )
  const [notifyStreak, setNotifyStreak] = useState(Boolean(prefs.notify_streak))
  const [notifyUnlock, setNotifyUnlock] = useState(Boolean(prefs.notify_unlock))
  const [language, setLanguage] = useState(String(prefs.language ?? "en"))
  const [timezone, setTimezone] = useState(
    String(prefs.timezone ?? Intl.DateTimeFormat().resolvedOptions().timeZone),
  )
  const [prefMsg, setPrefMsg] = useState("")

  async function saveProfile() {
    setProfileMsg("")
    setProfileErr("")
    try {
      await updateProfile({
        first_name: firstName,
        last_name: lastName,
        username: usernameField,
        birthday: birthday || null,
        phone,
      })
      await refreshUser()
      setProfileMsg("Saved.")
    } catch (e) {
      setProfileErr(err(e))
    }
  }

  async function onAvatarPick(file: File) {
    setProfileErr("")
    try {
      await uploadAvatar(file)
      await refreshUser()
      setProfileMsg("Picture updated.")
    } catch (e) {
      setProfileErr(err(e))
    }
  }

  async function savePassword() {
    setPwMsg("")
    setPwErr("")
    if (newPw.length < 8) {
      setPwErr("New password must be at least 8 characters.")
      return
    }
    try {
      await changePassword(oldPw, newPw)
      setOldPw("")
      setNewPw("")
      setPwMsg("Password changed.")
    } catch (e) {
      setPwErr(err(e))
    }
  }

  async function savePrefs() {
    setPrefMsg("")
    try {
      await updateProfile({
        preferences: {
          daily_goal: Number(dailyGoal) || 0,
          reminder_time: reminder,
          weekdays,
          notify_streak: notifyStreak,
          notify_unlock: notifyUnlock,
          language,
          timezone,
        },
      })
      await refreshUser()
      setPrefMsg("Preferences saved.")
    } catch {
      setPrefMsg("Could not save — try again.")
    }
  }

  async function handleLogoutAll() {
    await logoutAllDevices().catch(() => {})
    localStorage.removeItem(TOKEN_KEY)
    navigate("/login")
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
      setProfileErr(err(e))
    }
  }

  async function handleReset() {
    if (!window.confirm("Reset ALL your learning progress (reviews, streaks, completed lessons)? This cannot be undone.")) return
    await resetProgress().catch(() => {})
    qc.invalidateQueries()
    setPrefMsg("Progress reset.")
  }

  async function handleExport() {
    const data = await exportMyData()
    const blob = new Blob([JSON.stringify(data, null, 2)], {
      type: "application/json",
    })
    const url = URL.createObjectURL(blob)
    const a = document.createElement("a")
    a.href = url
    a.download = "my-data.json"
    a.click()
    URL.revokeObjectURL(url)
  }

  function toggleWeekday(i: number) {
    setWeekdays((w) => (w.includes(i) ? w.filter((d) => d !== i) : [...w, i]))
  }

  return (
    <div className="flex flex-col gap-6">
      <div>
        <h1 className="text-2xl font-semibold tracking-tight">Settings</h1>
        <p className="mt-1 text-sm text-muted-foreground">
          Manage your profile, security, and preferences.
        </p>
      </div>

      {/* Profile */}
      <Section title="Profile">
        <div className="flex items-center gap-4">
          <div className="flex size-16 items-center justify-center overflow-hidden rounded-full bg-accent/15 text-xl font-bold text-accent">
            {user?.avatar_url ? (
              <img src={user.avatar_url} alt="" className="size-full object-cover" />
            ) : (
              (user?.username ?? "?").charAt(0).toUpperCase()
            )}
          </div>
          <div>
            <input
              ref={avatarInput}
              type="file"
              accept="image/*"
              className="hidden"
              onChange={(e) => {
                const f = e.target.files?.[0]
                if (f) onAvatarPick(f)
              }}
            />
            <Button variant="outline" size="sm" onClick={() => avatarInput.current?.click()}>
              Change picture
            </Button>
          </div>
        </div>

        <div className="mt-4 grid gap-3 sm:grid-cols-2">
          <Field label="First name">
            <Input value={firstName} onChange={(e) => setFirstName(e.target.value)} />
          </Field>
          <Field label="Surname">
            <Input value={lastName} onChange={(e) => setLastName(e.target.value)} />
          </Field>
          <Field label="Username (changeable every 30 days)">
            <Input value={usernameField} onChange={(e) => setUsernameField(e.target.value)} />
          </Field>
          <Field label="Birthday">
            <Input type="date" value={birthday ?? ""} onChange={(e) => setBirthday(e.target.value)} />
          </Field>
          <Field label="Phone">
            <Input type="tel" value={phone} onChange={(e) => setPhone(e.target.value)} />
          </Field>
          <Field label="Email (not editable)">
            <Input value={user?.email ?? ""} disabled />
          </Field>
        </div>
        {profileErr && <Msg tone="danger">{profileErr}</Msg>}
        {profileMsg && <Msg tone="success">{profileMsg}</Msg>}
        <Button className="mt-3 self-start" onClick={saveProfile}>
          Save profile
        </Button>
      </Section>

      {/* Security */}
      <Section title="Security">
        <div className="grid gap-3 sm:grid-cols-2">
          <Field label="Current password">
            <Input type="password" value={oldPw} onChange={(e) => setOldPw(e.target.value)} autoComplete="current-password" />
          </Field>
          <Field label="New password">
            <Input type="password" value={newPw} onChange={(e) => setNewPw(e.target.value)} autoComplete="new-password" />
          </Field>
        </div>
        {pwErr && <Msg tone="danger">{pwErr}</Msg>}
        {pwMsg && <Msg tone="success">{pwMsg}</Msg>}
        <div className="mt-3 flex flex-wrap gap-2">
          <Button onClick={savePassword}>Change password</Button>
          <Button variant="outline" onClick={handleLogoutAll}>
            Log out of all devices
          </Button>
        </div>
      </Section>

      {/* Appearance */}
      <Section title="Appearance">
        <ThemeToggle />
      </Section>

      {/* Learning */}
      <Section title="Learning">
        <div className="grid gap-3 sm:grid-cols-2">
          <Field label="Daily goal (reviews)">
            <Input type="number" min={0} value={dailyGoal} onChange={(e) => setDailyGoal(e.target.value)} />
          </Field>
          <Field label="Reminder time">
            <Input type="time" value={reminder} onChange={(e) => setReminder(e.target.value)} />
          </Field>
        </div>
        <p className="mt-3 mb-1 text-xs text-muted-foreground">Days that count toward your schedule</p>
        <div className="flex flex-wrap gap-2">
          {WEEKDAYS.map((d, i) => (
            <button
              key={d}
              onClick={() => toggleWeekday(i)}
              className={cn(
                "rounded-lg border px-3 py-1.5 text-sm transition-colors",
                weekdays.includes(i)
                  ? "border-accent bg-accent text-accent-foreground"
                  : "border-border bg-background hover:border-accent",
              )}
            >
              {d}
            </button>
          ))}
        </div>
      </Section>

      {/* Notifications */}
      <Section title="Notifications">
        <Toggle label="Email me when my streak is about to break" checked={notifyStreak} onChange={setNotifyStreak} />
        <Toggle label="Email me when a new lesson unlocks" checked={notifyUnlock} onChange={setNotifyUnlock} />
        <p className="mt-1 text-xs text-muted-foreground">
          Preferences are saved now; email delivery turns on once mail is configured.
        </p>
      </Section>

      {/* Localization */}
      <Section title="Localization">
        <div className="grid gap-3 sm:grid-cols-2">
          <Field label="Interface language">
            <select
              value={language}
              onChange={(e) => setLanguage(e.target.value)}
              className="h-10 w-full rounded-md border border-input bg-background px-3 text-sm"
            >
              <option value="en">English</option>
              <option value="de">Deutsch</option>
            </select>
          </Field>
          <Field label="Timezone">
            <Input value={timezone} onChange={(e) => setTimezone(e.target.value)} />
          </Field>
        </div>
        <p className="mt-1 text-xs text-muted-foreground">
          Timezone affects when your streak day rolls over.
        </p>
      </Section>

      {prefMsg && <Msg tone="success">{prefMsg}</Msg>}
      <Button className="self-start" onClick={savePrefs}>
        Save preferences
      </Button>

      {/* Account / data */}
      <Section title="Your data">
        <div className="flex flex-wrap gap-2">
          <Button variant="outline" onClick={handleExport}>
            Export my data
          </Button>
          <Button variant="outline" asChild>
            <Link to="/privacy">Privacy policy</Link>
          </Button>
        </div>
      </Section>

      {/* Danger zone */}
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
      </Section>
    </div>
  )
}

function Section({
  title,
  children,
  danger,
}: {
  title: string
  children: ReactNode
  danger?: boolean
}) {
  return (
    <section
      className={cn(
        "flex flex-col rounded-xl border bg-surface p-5",
        danger ? "border-[hsl(var(--danger))]/40" : "border-border",
      )}
    >
      <h2 className={cn("text-sm font-semibold", danger && "text-[hsl(var(--danger))]")}>
        {title}
      </h2>
      <div className="mt-3">{children}</div>
    </section>
  )
}

function Field({ label, children }: { label: string; children: ReactNode }) {
  return (
    <label className="flex flex-col gap-1 text-xs text-muted-foreground">
      {label}
      {children}
    </label>
  )
}

function Toggle({
  label,
  checked,
  onChange,
}: {
  label: string
  checked: boolean
  onChange: (v: boolean) => void
}) {
  return (
    <label className="flex items-center gap-2 py-1 text-sm">
      <input type="checkbox" checked={checked} onChange={(e) => onChange(e.target.checked)} />
      {label}
    </label>
  )
}

function Msg({ tone, children }: { tone: "success" | "danger"; children: ReactNode }) {
  return (
    <p
      className={cn(
        "mt-2 text-sm",
        tone === "success" ? "text-[hsl(var(--success))]" : "text-[hsl(var(--danger))]",
      )}
    >
      {children}
    </p>
  )
}
