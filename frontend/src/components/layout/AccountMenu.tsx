import { useEffect, useRef, useState } from "react"
import { Link, useNavigate } from "react-router-dom"
import { LogOut, Settings, Shield } from "lucide-react"
import type { LucideIcon } from "lucide-react"

import { useAuth } from "@/contexts/AuthContext"

export function AccountMenu() {
  const { user, logout } = useAuth()
  const navigate = useNavigate()
  const [open, setOpen] = useState(false)
  const ref = useRef<HTMLDivElement>(null)

  // Close on outside click (the listener's setState is async — fine).
  useEffect(() => {
    function onDoc(e: MouseEvent) {
      if (ref.current && !ref.current.contains(e.target as Node)) setOpen(false)
    }
    document.addEventListener("mousedown", onDoc)
    return () => document.removeEventListener("mousedown", onDoc)
  }, [])

  if (!user) return null
  const initial = (user.email || "?").charAt(0).toUpperCase()

  async function handleLogout() {
    setOpen(false)
    await logout()
    navigate("/")
  }

  return (
    <div ref={ref} className="relative">
      <button
        onClick={() => setOpen((v) => !v)}
        aria-haspopup="menu"
        aria-expanded={open}
        aria-label="Account menu"
        className="flex size-9 items-center justify-center rounded-full bg-accent/15 text-sm font-bold text-accent transition-colors hover:bg-accent/25"
      >
        {initial}
      </button>

      {open && (
        <div className="absolute right-0 top-full z-50 mt-2 w-56 rounded-xl border border-border bg-surface p-1.5 shadow-xl">
          <div className="px-3 py-2">
            <p className="truncate text-sm font-medium" title={user.email}>
              {user.email}
            </p>
            <p className="text-xs text-muted-foreground">Level {user.cefr_level}</p>
          </div>
          <div className="my-1 h-px bg-border" />
          <MenuLink to="/settings" icon={Settings} label="Settings" onClick={() => setOpen(false)} />
          <MenuLink to="/privacy" icon={Shield} label="Privacy" onClick={() => setOpen(false)} />
          <button
            onClick={handleLogout}
            className="flex w-full items-center gap-2 rounded-md px-3 py-2 text-sm text-muted-foreground transition-colors hover:bg-background hover:text-foreground"
          >
            <LogOut className="size-4" /> Log out
          </button>
        </div>
      )}
    </div>
  )
}

function MenuLink({
  to,
  icon: Icon,
  label,
  onClick,
}: {
  to: string
  icon: LucideIcon
  label: string
  onClick: () => void
}) {
  return (
    <Link
      to={to}
      onClick={onClick}
      className="flex items-center gap-2 rounded-md px-3 py-2 text-sm text-muted-foreground transition-colors hover:bg-background hover:text-foreground"
    >
      <Icon className="size-4" /> {label}
    </Link>
  )
}
