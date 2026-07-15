import { useEffect, useRef, useState } from "react"
import { Link, NavLink, useLocation } from "react-router-dom"
import { ChevronDown, Menu, X } from "lucide-react"

import { useAuth } from "@/contexts/AuthContext"
import { SITE_NAME } from "@/lib/site"
import { cn } from "@/lib/utils"
import { Button } from "@/components/ui/button"
import { useEnergy } from "@/hooks/useEnergy"
import { EnergyMeter } from "@/components/path/EnergyMeter"
import { AccountMenu } from "./AccountMenu"
import { MobileNav } from "./MobileNav"
import { dashboardItem, pathItem, aiItem, navGroups, type NavGroup, type NavLeaf } from "./navItems"

/*
 * Primary app navigation (Design v2 — Cinematic). Desktop = a spaceship-style
 * top bar: logo, a couple of standalone links, and grouped dropdown menus
 * (Practice / Library / Explore). Mobile = a hamburger that opens `MobileNav`.
 * The left rail is retired. Nav only renders for signed-in users; guests see
 * the login/sign-up buttons.
 */
export function TopBar() {
  const { user } = useAuth()
  const [drawerOpen, setDrawerOpen] = useState(false)
  const { pathname } = useLocation()

  // Close the mobile drawer whenever the route changes (React's adjust-state-on-
  // change idiom: compare against a previous-value state, during render).
  const [seenPath, setSeenPath] = useState(pathname)
  if (seenPath !== pathname) {
    setSeenPath(pathname)
    if (drawerOpen) setDrawerOpen(false)
  }

  const brand = SITE_NAME === "German Learning Platform" ? "einfachDeutsch" : SITE_NAME

  return (
    <>
      <header className="sticky top-0 z-30 flex h-16 shrink-0 items-center gap-3 border-b border-border bg-surface/80 px-4 backdrop-blur">
        <button
          onClick={() => setDrawerOpen((v) => !v)}
          aria-label={drawerOpen ? "Close menu" : "Open menu"}
          aria-expanded={drawerOpen}
          className="rounded-md p-2 text-muted-foreground transition-colors hover:bg-background hover:text-foreground md:hidden"
        >
          {drawerOpen ? <X className="size-5" /> : <Menu className="size-5" />}
        </button>

        <Link
          to="/"
          className="flex shrink-0 items-center gap-2 text-base font-bold tracking-tight text-foreground"
        >
          <span className="inline-flex gap-1" aria-hidden="true">
            <span className="size-2.5 rounded-full" style={{ background: "hsl(var(--article-der))" }} />
            <span
              className="size-2.5"
              style={{ background: "hsl(var(--article-die))", clipPath: "polygon(50% 0, 100% 100%, 0 100%)" }}
            />
            <span className="size-2.5" style={{ background: "hsl(var(--article-das))" }} />
          </span>
          {brand}
        </Link>

        <nav className="ml-4 hidden items-center gap-1 md:flex">
          <BarLink item={dashboardItem} />
          <BarLink item={pathItem} />
          {navGroups.map((group) => (
            <NavDropdown key={group.label} group={group} />
          ))}
          <BarLink item={aiItem} />
        </nav>

        <div className="ml-auto flex shrink-0 items-center gap-3">
          {user ? (
            <>
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
      </header>

      <MobileNav open={drawerOpen} onClose={() => setDrawerOpen(false)} />
    </>
  )
}

/** The always-visible energy meter, ticking down to the next refill. */
function GlobalEnergy() {
  const { energy, secondsUntilNext } = useEnergy()
  if (!energy) return null
  return (
    <EnergyMeter
      energy={energy.current}
      max={energy.max}
      premium={energy.premium}
      secondsUntilNext={secondsUntilNext}
      className="max-sm:hidden"
    />
  )
}

/** A standalone top-bar link (Dashboard, AI Assistant). */
function BarLink({ item }: { item: NavLeaf }) {
  return (
    <NavLink
      to={item.to}
      end={item.end}
      className={({ isActive }) =>
        cn(
          "rounded-md px-3 py-2 text-sm font-medium transition-colors",
          isActive ? "bg-primary/15 text-foreground" : "text-muted-foreground hover:text-foreground",
        )
      }
    >
      {item.label}
    </NavLink>
  )
}

/** A top-bar dropdown menu. Opens on hover (desktop pointer) and on click;
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
        className={cn(
          "flex items-center gap-1 rounded-md px-3 py-2 text-sm font-medium transition-colors",
          active || open ? "text-foreground" : "text-muted-foreground hover:text-foreground",
        )}
      >
        {group.label}
        <ChevronDown className={cn("size-4 transition-transform", open && "rotate-180")} />
      </button>

      {open && (
        <div className="absolute left-0 top-full z-50 w-56 pt-1">
          <div className="rounded-xl border border-border bg-surface p-1.5 shadow-xl">
            {group.items.map((item) => (
              <NavLink
                key={item.to}
                to={item.to}
                className={({ isActive }) =>
                  cn(
                    "flex items-center gap-2.5 rounded-md px-3 py-2 text-sm transition-colors",
                    isActive
                      ? "bg-primary/15 text-foreground"
                      : "text-muted-foreground hover:bg-background hover:text-foreground",
                  )
                }
              >
                <item.icon className="size-4 shrink-0" aria-hidden="true" />
                {item.label}
              </NavLink>
            ))}
          </div>
        </div>
      )}
    </div>
  )
}
