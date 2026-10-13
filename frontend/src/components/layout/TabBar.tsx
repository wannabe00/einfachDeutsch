import { useState } from "react"
import { NavLink, useLocation } from "react-router-dom"
import { BookMarked, GraduationCap, Home, MoreHorizontal, Route as RouteIcon } from "lucide-react"

import { cn } from "@/lib/utils"
import { MoreSheet } from "./MoreSheet"

const TABS = [
  { to: "/", label: "Home", icon: Home, end: true },
  { to: "/path", label: "Path", icon: RouteIcon },
  { to: "/review", label: "Review", icon: GraduationCap },
  { to: "/words", label: "Words", icon: BookMarked },
]

/*
 * iOS-style bottom tab bar on phones (hidden from lg up, where the top bar has
 * the full nav). "More" opens a sheet with every other page.
 */
export function TabBar() {
  const [moreOpen, setMoreOpen] = useState(false)
  const { pathname } = useLocation()
  const inTabs = TABS.some((t) => (t.end ? pathname === t.to : pathname.startsWith(t.to)))

  // Close the sheet whenever the route changes (adjust-state-on-change idiom).
  const [seenPath, setSeenPath] = useState(pathname)
  if (seenPath !== pathname) {
    setSeenPath(pathname)
    if (moreOpen) setMoreOpen(false)
  }

  const tabCls = (active: boolean) =>
    cn(
      "flex min-h-[48px] min-w-[60px] flex-1 flex-col items-center justify-center gap-0.5 text-[11px] font-medium transition-colors",
      active ? "text-primary" : "text-muted-foreground",
    )

  return (
    <>
      <nav
        aria-label="Main"
        className="glass fixed inset-x-0 bottom-0 z-30 flex border-t border-border/60 px-2 pt-1.5 pb-[max(env(safe-area-inset-bottom),10px)] lg:hidden"
      >
        {TABS.map(({ to, label, icon: Icon, end }) => (
          <NavLink key={to} to={to} end={end} className={({ isActive }) => tabCls(isActive)}>
            <Icon className="size-6" aria-hidden="true" />
            {label}
          </NavLink>
        ))}
        <button
          onClick={() => setMoreOpen(true)}
          aria-haspopup="dialog"
          aria-expanded={moreOpen}
          className={tabCls(moreOpen || !inTabs)}
        >
          <MoreHorizontal className="size-6" aria-hidden="true" />
          More
        </button>
      </nav>
      <MoreSheet open={moreOpen} onClose={() => setMoreOpen(false)} />
    </>
  )
}
