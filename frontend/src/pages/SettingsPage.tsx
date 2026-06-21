import { useMutation } from "@tanstack/react-query"

import { useAuth } from "@/contexts/AuthContext"
import { setLevel } from "@/api/leveling"
import type { CEFRLevel } from "@/types"
import { ThemeToggle } from "@/components/layout/ThemeToggle"
import { cn } from "@/lib/utils"

const LEVELS: CEFRLevel[] = ["A1", "A2", "B1", "B2", "C1", "C2"]

export default function SettingsPage() {
  const { user, refreshUser } = useAuth()

  const change = useMutation({
    mutationFn: (level: CEFRLevel) => setLevel(level),
    onSuccess: () => refreshUser(),
  })

  return (
    <div>
      <h1 className="text-2xl font-semibold tracking-tight">Settings</h1>
      <p className="mt-1 text-sm text-muted-foreground">
        Manage your account and preferences.
      </p>

      {/* Account */}
      <div className="mt-6 rounded-xl border border-border bg-surface p-5">
        <h2 className="text-sm font-semibold">Account</h2>
        <dl className="mt-3 space-y-2 text-sm">
          <div className="flex justify-between gap-4">
            <dt className="text-muted-foreground">Email</dt>
            <dd className="truncate font-medium">{user?.email}</dd>
          </div>
          <div className="flex justify-between gap-4">
            <dt className="text-muted-foreground">Current level</dt>
            <dd className="font-medium">{user?.cefr_level}</dd>
          </div>
        </dl>
      </div>

      {/* Level */}
      <div className="mt-4 rounded-xl border border-border bg-surface p-5">
        <h2 className="text-sm font-semibold">Your level</h2>
        <p className="mt-1 text-sm text-muted-foreground">
          Change the level your content is tuned to.
        </p>
        <div className="mt-3 grid grid-cols-3 gap-2 sm:grid-cols-6">
          {LEVELS.map((lvl) => (
            <button
              key={lvl}
              disabled={change.isPending}
              onClick={() => change.mutate(lvl)}
              className={cn(
                "rounded-lg border py-2 text-sm font-semibold transition-colors disabled:opacity-50",
                user?.cefr_level === lvl
                  ? "border-accent bg-accent text-accent-foreground"
                  : "border-border bg-background hover:border-accent",
              )}
            >
              {lvl}
            </button>
          ))}
        </div>
        {change.isSuccess && (
          <p className="mt-2 text-xs text-[hsl(var(--success))]">Level updated.</p>
        )}
      </div>

      {/* Appearance */}
      <div className="mt-4 rounded-xl border border-border bg-surface p-5">
        <h2 className="text-sm font-semibold">Appearance</h2>
        <div className="mt-2">
          <ThemeToggle />
        </div>
      </div>

      <p className="mt-6 text-sm text-muted-foreground">
        More settings (change email, password, notifications) are coming soon.
      </p>
    </div>
  )
}
