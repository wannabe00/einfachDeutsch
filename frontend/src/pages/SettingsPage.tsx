import { useState, type ComponentType } from "react"
import { useSearchParams } from "react-router-dom"
import { User, Shield, SlidersHorizontal, UserCog, type LucideIcon } from "lucide-react"

import { cn } from "@/lib/utils"
import { ProfileHeader } from "@/components/profile/ProfileHeader"
import { ProfileSection } from "@/components/settings/ProfileSection"
import { SecuritySection } from "@/components/settings/SecuritySection"
import { PreferencesSection } from "@/components/settings/PreferencesSection"
import { AccountSection } from "@/components/settings/AccountSection"

/*
 * Settings: a tab list (vertical on desktop, a scrolling strip on mobile) and
 * the active section next to it. Each section manages its own state and saving,
 * so only the active one is mounted.
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
  { id: "account", label: "Account", icon: UserCog, Component: AccountSection },
]

export default function SettingsPage() {
  // ?tab=account opens a tab directly (Stripe sends users back there).
  const [params] = useSearchParams()
  const [active, setActive] = useState(
    TABS.find((t) => t.id === params.get("tab"))?.id ?? TABS[0].id,
  )
  const current = TABS.find((t) => t.id === active) ?? TABS[0]
  const Panel = current.Component

  return (
    <div className="flex flex-col gap-6">
      <ProfileHeader />

      <div className="grid gap-6 md:grid-cols-[210px_1fr]">
        {/* Scrolls sideways on mobile, sticks to the side on desktop. */}
        <nav
          aria-label="Settings sections"
          className="-mx-1 flex gap-1 overflow-x-auto px-1 pb-1 md:mx-0 md:flex-col md:overflow-visible md:px-0 md:pb-0 md:self-start md:sticky md:top-20"
        >
          {TABS.map((tab) => {
            const isActive = tab.id === active
            return (
              <button
                key={tab.id}
                onClick={() => setActive(tab.id)}
                aria-current={isActive ? "page" : undefined}
                className={cn(
                  "flex min-h-[44px] shrink-0 items-center gap-2.5 whitespace-nowrap rounded-xl px-3.5 py-2.5 text-[15px] font-medium transition-colors md:w-full",
                  isActive
                    ? "bg-surface text-foreground shadow-card"
                    : "text-muted-foreground hover:bg-surface hover:text-foreground",
                )}
              >
                <tab.icon className="size-4 shrink-0" aria-hidden="true" />
                {tab.label}
              </button>
            )
          })}
        </nav>

        {/* Active section panel */}
        <div className="flex min-w-0 flex-col gap-5">
          <Panel />
        </div>
      </div>
    </div>
  )
}
