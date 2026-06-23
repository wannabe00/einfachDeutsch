import { useState } from "react"

import { useAuth } from "@/contexts/AuthContext"
import { updateProfile } from "@/api/account"
import { ThemeToggle } from "@/components/layout/ThemeToggle"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { cn } from "@/lib/utils"
import { Field, Msg, Section, Toggle } from "./primitives"

const WEEKDAYS = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]

/** Learning goal, notification toggles, and localization — all saved together
    via the single "Save preferences" button (one `preferences` JSON blob). */
export function PreferencesSection() {
  const { user, refreshUser } = useAuth()
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
  const [msg, setMsg] = useState("")

  function toggleWeekday(i: number) {
    setWeekdays((w) => (w.includes(i) ? w.filter((d) => d !== i) : [...w, i]))
  }

  async function savePrefs() {
    setMsg("")
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
      setMsg("Preferences saved.")
    } catch {
      setMsg("Could not save — try again.")
    }
  }

  return (
    <>
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

      <Section title="Notifications">
        <Toggle label="Email me when my streak is about to break" checked={notifyStreak} onChange={setNotifyStreak} />
        <Toggle label="Email me when a new lesson unlocks" checked={notifyUnlock} onChange={setNotifyUnlock} />
        <p className="mt-1 text-xs text-muted-foreground">
          Preferences are saved now; email delivery turns on once mail is configured.
        </p>
      </Section>

      <Section title="Appearance & localization">
        <div className="mb-3">
          <p className="mb-1 text-xs text-muted-foreground">Theme</p>
          <div className="rounded-md border border-border">
            <ThemeToggle />
          </div>
        </div>
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

      {msg && <Msg tone="success">{msg}</Msg>}
      <Button className="self-start" onClick={savePrefs}>
        Save preferences
      </Button>
    </>
  )
}
