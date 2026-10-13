import { useState } from "react"
import { Check, Monitor, Moon, Sun, type LucideIcon } from "lucide-react"

import { cn } from "@/lib/utils"
import { getThemePref, setThemePref, type ThemePref } from "@/lib/theme"
import { Section } from "./primitives"

const OPTIONS: { id: ThemePref; label: string; hint: string; icon: LucideIcon }[] = [
  { id: "system", label: "System", hint: "Match this device", icon: Monitor },
  { id: "light", label: "Light", hint: "Always light", icon: Sun },
  { id: "dark", label: "Dark", hint: "Always dark", icon: Moon },
]

/** Light / dark / follow the device. Applies at once and is remembered on this device. */
export function AppearanceSection() {
  const [pref, setPref] = useState<ThemePref>(getThemePref)

  function choose(next: ThemePref) {
    setPref(next)
    setThemePref(next)
  }

  return (
    <Section title="Appearance">
      <div className="grid gap-3 sm:grid-cols-3" role="radiogroup" aria-label="Theme">
        {OPTIONS.map(({ id, label, hint, icon: Icon }) => {
          const on = pref === id
          return (
            <button
              key={id}
              role="radio"
              aria-checked={on}
              onClick={() => choose(id)}
              className={cn(
                "relative flex min-h-[64px] items-center gap-3 rounded-xl bg-surface-2 px-4 py-3 text-left transition-colors",
                on ? "ring-2 ring-primary" : "hover:bg-border",
              )}
            >
              <Icon className="size-5 shrink-0 text-muted-foreground" aria-hidden="true" />
              <span className="min-w-0">
                <span className="block font-semibold">{label}</span>
                <span className="block text-sm text-muted-foreground">{hint}</span>
              </span>
              {on && <Check className="ml-auto size-5 text-primary" aria-hidden="true" />}
            </button>
          )
        })}
      </div>
      <p className="mt-3 text-sm text-muted-foreground">Saved on this device.</p>
    </Section>
  )
}
