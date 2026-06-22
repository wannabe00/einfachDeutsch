import { ThemeToggle } from "@/components/layout/ThemeToggle"
import { Section } from "@/components/settings/primitives"
import { ProfileSection } from "@/components/settings/ProfileSection"
import { SecuritySection } from "@/components/settings/SecuritySection"
import { PreferencesSection } from "@/components/settings/PreferencesSection"
import { DataSection } from "@/components/settings/DataSection"
import { DangerZoneSection } from "@/components/settings/DangerZoneSection"

/** Settings shell — each section is a self-contained component under
    `components/settings/` that owns its own state + save logic. */
export default function SettingsPage() {
  return (
    <div className="flex flex-col gap-6">
      <div>
        <h1 className="text-2xl font-semibold tracking-tight">Settings</h1>
        <p className="mt-1 text-sm text-muted-foreground">
          Manage your profile, security, and preferences.
        </p>
      </div>

      <ProfileSection />
      <SecuritySection />
      <Section title="Appearance">
        <ThemeToggle />
      </Section>
      <PreferencesSection />
      <DataSection />
      <DangerZoneSection />
    </div>
  )
}
