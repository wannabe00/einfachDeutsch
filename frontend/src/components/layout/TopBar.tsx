import { useEffect, useRef, useState } from "react"
import { Link, NavLink, useLocation } from "react-router-dom"
import { useQuery } from "@tanstack/react-query"
import { ChevronDown } from "lucide-react"

import { useAuth } from "@/contexts/AuthContext"
import { fetchStreak } from "@/api/leveling"
import { SITE_NAME } from "@/lib/site"
import { cn } from "@/lib/utils"
import { Button } from "@/components/ui/button"
import { useEnergy } from "@/hooks/useEnergy"
import { EnergyMeter } from "@/components/path/EnergyMeter"
import { StreakFlame } from "@/components/lektion/StreakFlame"
import { AccountMenu } from "./AccountMenu"
import { BrandMark } from "./BrandMark"
import { dashboardItem, pathItem, aiItem, navGroups, type NavGroup, type NavLeaf } from "./navItems"

/** The streak shows in the bar once the flame is earned (see DESIGN.md). */
const STREAK_CHIP_FROM = 3

/*
 * Frosted top bar. Large screens: logo, the nav in a pill track (with
 * Practice / Library / Explore dropdowns), then streak, energy and account.
 * Phones and tablets only show the logo, energy and account here; their
 * navigation is the bottom `TabBar`. Guests see login buttons.
 */
export function TopBar() {
  const { user, loading } = useAuth()

  return (
    <header className="glass sticky top-0 z-30 shrink-0">
      {/* Full width: logo at the left edge, account at the right, and on large
          screens the links exactly centred (equal side columns). */}
      <div className="grid h-14 w-full grid-cols-[1fr_auto] items-center gap-3 px-4 sm:px-6 lg:h-16 lg:grid-cols-[1fr_auto_1fr] lg:px-8">
        <Logo className="justify-self-start" />

        <nav
          className="hidden items-center gap-0.5 rounded-full bg-surface-2/80 p-1 lg:flex"
          aria-label="Main"
        >
          <BarLink item={dashboardItem} />
          <BarLink item={pathItem} />
          {navGroups.map((group) => (
            <NavDropdown key={group.label} group={group} />
          ))}
          <BarLink item={aiItem} />
        </nav>

        <div className="flex shrink-0 items-center justify-self-end gap-2">
          {/* Nothing until we know who's signed in, so members don't see a
              flash of the guest buttons on every page load. */}
          {loading ? null : user ? (
            <>
              <StreakChip />
              <GlobalEnergy />
              <AccountMenu />
            </>
          ) : (
            <>
              {/* Hide the ghost "Log in" on the smallest screens so the guest bar
                  never overflows; "Sign up" lands on the same page anyway. */}
              <Button asChild variant="ghost" size="sm" className="hidden sm:inline-flex">
                <Link to="/login">Log in</Link>
              </Button>
              <Button asChild size="sm">
                <Link to="/login">Sign up</Link>
              </Button>
            </>
          )}
        </div>
      </div>
    </header>
  )
}

/** The mark plus the site name, its last capitalised word in red ("einfach" + "Deutsch"). */
export function Logo({ className }: { className?: string }) {
  const m = SITE_NAME.match(/^(.*?)([A-Z][a-z]+)$/)
  return (
    <Link
      to="/"
      className={cn(
        "flex shrink-0 items-center gap-2 text-[19px] font-extrabold tracking-[-0.03em] text-foreground",
        className,
      )}
    >
      <BrandMark />
      <span>
        {m ? (
          <>
            {m[1]}
            <span className="text-primary">{m[2]}</span>
          </>
        ) : (
          SITE_NAME
        )}
      </span>
    </Link>
  )
}

/** Streak count with the flame, only once it's earned. */
function StreakChip() {
  const { user } = useAuth()
  const { data } = useQuery({ queryKey: ["streak"], queryFn: fetchStreak, enabled: !!user })
  const days = data?.current_streak ?? 0
  if (days < STREAK_CHIP_FROM) return null
  return (
    <Link
      to="/"
      className="hidden h-9 items-center gap-1 rounded-full bg-surface-2 pl-2 pr-3 text-sm font-bold tabular-nums sm:inline-flex"
      title={`${days}-day streak`}
      aria-label={`${days}-day streak`}
    >
      <StreakFlame size={20} />
      {days}
    </Link>
  )
}

/** The always-visible energy chip, ticking down to the next refill. */
function GlobalEnergy() {
  const { energy, secondsUntilNext } = useEnergy()
  if (!energy) return null
  return (
    <EnergyMeter
      energy={energy.current}
      max={energy.max}
      premium={energy.premium}
      secondsUntilNext={secondsUntilNext}
    />
  )
}

const linkCls = (active: boolean) =>
  cn(
    "flex h-9 items-center rounded-full px-3.5 text-[15px] font-medium transition-colors",
    active
      ? "bg-surface text-foreground shadow-card"
      : "text-muted-foreground hover:text-foreground",
  )

/** A standalone link in the track (Home, Path, AI Assistant). */
function BarLink({ item }: { item: NavLeaf }) {
  return (
    <NavLink to={item.to} end={item.end} className={({ isActive }) => linkCls(isActive)}>
      {item.label}
    </NavLink>
  )
}

/** A dropdown in the track. Opens on hover (desktop pointer) and on click;
    closes on outside click or route change. Highlights when a child is active. */
function NavDropdown({ group }: { group: NavGroup }) {
  const [open, setOpen] = useState(false)
  const ref = useRef<HTMLDivElement>(null)
  const { pathname } = useLocation()
  const active = group.items.some((it) => pathname === it.to || pathname.startsWith(it.to + "/"))

  // Close the menu on route change (adjust-state-on-change during render).
  const [seenPath, setSeenPath] = useState(pathname)
  if (seenPath !== pathname) {
    setSeenPath(pathname)
    if (open) setOpen(false)
  }

  useEffect(() => {
    function onDoc(e: MouseEvent) {
      if (ref.current && !ref.current.contains(e.target as Node)) setOpen(false)
    }
    document.addEventListener("mousedown", onDoc)
    return () => document.removeEventListener("mousedown", onDoc)
  }, [])

  return (
    <div
      ref={ref}
      className="relative"
      onMouseEnter={() => setOpen(true)}
      onMouseLeave={() => setOpen(false)}
    >
      <button
        onClick={() => setOpen((v) => !v)}
        aria-haspopup="menu"
        aria-expanded={open}
        className={cn(linkCls(active), "gap-1", open && !active && "text-foreground")}
      >
        {group.label}
        <ChevronDown className={cn("size-4 transition-transform", open && "rotate-180")} />
      </button>

      {open && (
        <div className="absolute left-1/2 top-full z-50 w-64 -translate-x-1/2 pt-2">
          <div className="rounded-2xl bg-popover p-1.5 shadow-lift animate-in fade-in-0 zoom-in-95 duration-150">
            {group.items.map((item) => (
              <NavLink
                key={item.to}
                to={item.to}
                className={({ isActive }) =>
                  cn(
                    "flex min-h-[44px] items-center gap-3 rounded-xl px-3 py-2 text-[15px] transition-colors",
                    isActive
                      ? "bg-surface-2 font-semibold text-foreground"
                      : "text-muted-foreground hover:bg-surface-2 hover:text-foreground",
                  )
                }
              >
                <item.icon className="size-[18px] shrink-0" aria-hidden="true" />
                {item.label}
              </NavLink>
            ))}
          </div>
        </div>
      )}
    </div>
  )
}
