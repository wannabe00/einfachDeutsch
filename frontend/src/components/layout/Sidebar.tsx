import { useState } from "react"
import { NavLink } from "react-router-dom"
import {
  LayoutDashboard,
  GraduationCap,
  BookMarked,
  BookOpen,
  NotebookPen,
  Library,
  Sparkles,
  Swords,
  Mic,
  Tv,
  Landmark,
  Menu,
} from "lucide-react"

import { cn } from "@/lib/utils"
import { ThemeToggle } from "./ThemeToggle"

const navItems = [
  { to: "/", label: "Dashboard", icon: LayoutDashboard, end: true },
  { to: "/review", label: "Review", icon: GraduationCap, end: false },
  { to: "/words", label: "Word Bank", icon: BookMarked, end: false },
  { to: "/grammar", label: "Grammar", icon: BookOpen, end: false },
  { to: "/exercises", label: "Exercises", icon: NotebookPen, end: false },
  { to: "/drills", label: "Drills", icon: Swords, end: false },
  { to: "/speak", label: "Recite", icon: Mic, end: false },
  { to: "/videos", label: "Videos", icon: Tv, end: false },
  { to: "/history", label: "History", icon: Landmark, end: false },
  { to: "/books", label: "Books", icon: Library, end: false },
  { to: "/ai", label: "AI Assistant", icon: Sparkles, end: false },
]

export function Sidebar() {
  // Desktop: expands on hover. Mobile: a button opens it as a drawer.
  const [hover, setHover] = useState(false)
  const [mobileOpen, setMobileOpen] = useState(false)
  const expanded = hover || mobileOpen
  const close = () => setMobileOpen(false)

  return (
    // The outer element reserves the slim rail's width (64px); the inner panel
    // expands over the content on hover (no layout shift).
    <aside className="relative w-16 shrink-0">
      {mobileOpen && (
        <div
          className="fixed inset-x-0 bottom-0 top-14 z-40 bg-black/50 md:hidden"
          onClick={close}
          aria-hidden="true"
        />
      )}

      <div
        onMouseEnter={() => setHover(true)}
        onMouseLeave={() => setHover(false)}
        className={cn(
          "sticky top-14 z-50 flex h-[calc(100dvh-3.5rem)] flex-col overflow-hidden border-r border-border bg-surface transition-[width] duration-200",
          expanded ? "w-60" : "w-16",
          mobileOpen &&
            "max-md:fixed max-md:left-0 max-md:top-14 max-md:bottom-0 max-md:h-auto max-md:shadow-2xl",
        )}
      >
        {/* Open/close — mobile only (desktop uses hover) */}
        <div className="flex items-center px-3 py-2 md:hidden">
          <button
            onClick={() => setMobileOpen((v) => !v)}
            aria-label={mobileOpen ? "Close menu" : "Open menu"}
            className="rounded-md p-1.5 text-muted-foreground transition-colors hover:bg-background hover:text-foreground"
          >
            <Menu className="size-5" />
          </button>
        </div>

        <nav className="flex flex-col gap-1 px-3 pt-1">
          {navItems.map(({ to, label, icon: Icon, end }) => (
            <NavLink
              key={to}
              to={to}
              end={end}
              onClick={close}
              title={label}
              className={({ isActive }) =>
                cn(
                  "flex items-center gap-3 rounded-md px-3 py-2 text-sm font-medium transition-colors",
                  isActive
                    ? "bg-primary text-primary-foreground"
                    : "text-muted-foreground hover:bg-background hover:text-foreground",
                )
              }
            >
              <Icon className="size-5 shrink-0" aria-hidden="true" />
              <span
                className={cn(
                  "whitespace-nowrap transition-opacity",
                  expanded ? "opacity-100" : "opacity-0",
                )}
              >
                {label}
              </span>
            </NavLink>
          ))}
        </nav>

        <div className="mt-auto px-3 pb-4">
          <ThemeToggle collapsed={!expanded} />
        </div>
      </div>
    </aside>
  )
}
