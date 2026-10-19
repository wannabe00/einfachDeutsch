import { useState } from "react"
import { Link } from "react-router-dom"

import { useAuth } from "@/contexts/AuthContext"
import { updateProfile } from "@/api/account"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { AITutorForm } from "@/components/ai/AISettingsDialog"
import { AppearanceSection } from "./AppearanceSection"
import { Field, Msg, Section } from "./primitives"

/** Learning (the daily goal), the AI tutor (premium) and the theme. */
export function PreferencesSection() {
  const { user } = useAuth()
  return (
    <>
      <LearningCard />
      <Section title="AI tutor">
        {user?.has_premium ? (
          <>
            <p className="-mt-2 mb-4 text-sm text-muted-foreground">
              How the AI Assistant talks to you. Your level and learned words are always included.
            </p>
            <AITutorForm />
          </>
        ) : (
          <p className="text-sm text-muted-foreground">
            Reply language, tone, corrections and your interests for the AI tutor are part of Premium.{" "}
            <Link to="/ai" className="font-semibold text-primary hover:underline">
              See Premium
            </Link>
          </p>
        )}
      </Section>
      <AppearanceSection />
    </>
  )
}

/** Reviews per day, shown as a ring on the dashboard. */
function LearningCard() {
  const { user, refreshUser } = useAuth()
  const prefs = (user?.preferences ?? {}) as Record<string, unknown>
  const [dailyGoal, setDailyGoal] = useState(String(prefs.daily_goal ?? 20))
  const [msg, setMsg] = useState("")

  async function save() {
    setMsg("")
    try {
      await updateProfile({ preferences: { daily_goal: Number(dailyGoal) || 20 } })
      await refreshUser()
      setMsg("Saved.")
    } catch {
      setMsg("Could not save. Try again.")
    }
  }

  return (
    <Section title="Learning">
      <div className="flex flex-wrap items-end gap-3">
        <Field label="Daily goal (reviews)">
          <Input type="number" min={1} value={dailyGoal} onChange={(e) => setDailyGoal(e.target.value)} className="w-32" />
        </Field>
        <Button onClick={save}>Save</Button>
      </div>
      <p className="mt-2 text-xs text-muted-foreground">
        Your streak counts every day you practise; a missed day uses a freeze.
      </p>
      {msg && <Msg tone="success">{msg}</Msg>}
    </Section>
  )
}
