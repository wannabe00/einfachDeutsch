import { useState, type ComponentType } from "react"
import {
  User,
  Shield,
  SlidersHorizontal,
  Download,
  TriangleAlert,
  type LucideIcon,
} from "lucide-react"

import { cn } from "@/lib/utils"
import { ProfileSection } from "@/components/settings/ProfileSection"
import { SecuritySection } from "@/components/settings/SecuritySection"
import { PreferencesSection } from "@/components/settings/PreferencesSection"
import { DataSection } from "@/components/settings/DataSection"
import { DangerZoneSection } from "@/components/settings/DangerZoneSection"

/*
 * Settings v2 (Design v2 — Cinematic). Spaceship-style layout: a vertical tab
 * rail on the left (desktop) / a horizontal scrolling tab strip (mobile), with a
 * single panel showing the active section. Each tab is one of the existing
 * self-contained section components — they own their own state + save logic, so
 * only the active one is mounted at a time.
 */
interface Tab {
  id: string
  label: string
  icon: LucideIcon
  Component: ComponentType
}

const TABS: Tab[] = [
  { id: "profile", label: "Profile", icon: User, Component: ProfileSection },
  { id: "security", label: "Security", icon: Shield, Component: SecuritySection },
  { id: "preferences", label: "Preferences", icon: SlidersHorizontal, Component: PreferencesSection },
  { id: "data", label: "Data", icon: Download, Component: DataSection },
  { id: "danger", label: "Danger zone", icon: TriangleAlert, Component: DangerZoneSection },
]

export default function SettingsPage() {
  const [active, setActive] = useState(TABS[0].id)
  const current = TABS.find((t) => t.id === active) ?? TABS[0]
  const Panel = current.Component

  return (
    <div className="flex flex-col gap-6">
      <header>
        <h1 className="text-2xl font-bold tracking-tight">Settings</h1>
        <p className="mt-1 text-sm text-muted-foreground">
          Manage your profile, security, and preferences.
        </p>
      </header>

      <div className="grid gap-6 md:grid-cols-[210px_1fr]">
        {/* Tab rail — horizontal scroll on mobile, sticky vertical on desktop */}
        <nav
          aria-label="Settings sections"
          className="-mx-1 flex gap-1 overflow-x-auto px-1 pb-1 md:mx-0 md:flex-col md:overflow-visible md:px-0 md:pb-0 md:self-start md:sticky md:top-20"
        >
          {TABS.map((tab) => {
            const isActive = tab.id === active
            const danger = tab.id === "danger"
            return (
              <button
                key={tab.id}
                onClick={() => setActive(tab.id)}
                aria-current={isActive ? "page" : undefined}
                className={cn(
                  "flex shrink-0 items-center gap-2.5 whitespace-nowrap rounded-lg px-3 py-2.5 text-sm font-medium transition-colors md:w-full",
                  isActive
                    ? danger
                      ? "bg-[hsl(var(--danger))]/15 text-[hsl(var(--danger))]"
                      : "bg-primary/15 text-foreground"
                    : cn(
                        "text-muted-foreground hover:bg-surface hover:text-foreground",
                        danger && "hover:text-[hsl(var(--danger))]",
                      ),
                )}
              >
                <tab.icon className="size-4 shrink-0" aria-hidden="true" />
                {tab.label}
              </button>
            )
          })}
        </nav>

        {/* Active section panel */}
        <div className="min-w-0">
          <Panel />
        </div>
      </div>
    </div>
  )
}
