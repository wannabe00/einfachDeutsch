import { useEffect, useState } from "react"
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
  PanelLeftClose,
  PanelLeft,
  LogIn,
} from "lucide-react"

import { cn } from "@/lib/utils"
import { SITE_NAME } from "@/lib/site"
import { useAuth } from "@/contexts/AuthContext"
import { ThemeToggle } from "./ThemeToggle"
import { AccountMenu } from "./AccountMenu"

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

const STORAGE_KEY = "sidebar-collapsed"

export function Sidebar() {
  const { user } = useAuth()
  const [collapsed, setCollapsed] = useState(() => {
    // Respect a saved preference; otherwise default to collapsed on small
    // (phone-width) screens so the icon rail leaves room for content.
    const stored = localStorage.getItem(STORAGE_KEY)
    if (stored !== null) return stored === "true"
    return typeof window !== "undefined" && window.innerWidth < 768
  })

  useEffect(() => {
    localStorage.setItem(STORAGE_KEY, String(collapsed))
  }, [collapsed])

  return (
    <>
      {/* On phones, an expanded sidebar overlays the content (drawer) instead
          of pushing it off-screen. Tapping the backdrop closes it. */}
      {!collapsed && (
        <div
          className="fixed inset-0 z-40 bg-black/50 md:hidden"
          onClick={() => setCollapsed(true)}
          aria-hidden="true"
        />
      )}
      <aside
        className={cn(
          "sticky top-0 flex h-screen shrink-0 flex-col border-r border-border bg-surface transition-[width] duration-200",
          collapsed ? "w-16" : "w-60",
          // expanded on mobile → fixed overlay so main content keeps full width
          !collapsed && "max-md:fixed max-md:inset-y-0 max-md:left-0 max-md:z-50 max-md:shadow-2xl",
        )}
      >
      <div
        className={cn(
          "flex items-center py-5",
          collapsed ? "justify-center px-2" : "justify-between px-4",
        )}
      >
        {!collapsed && (
          <span className="text-base font-semibold tracking-tight">
            {SITE_NAME}
          </span>
        )}
        <button
          onClick={() => setCollapsed((v) => !v)}
          aria-label={collapsed ? "Expand sidebar" : "Collapse sidebar"}
          className="rounded-md p-1.5 text-muted-foreground transition-colors hover:bg-background hover:text-foreground"
        >
          {collapsed ? (
            <PanelLeft className="size-5" />
          ) : (
            <PanelLeftClose className="size-5" />
          )}
        </button>
      </div>

      <nav className="flex flex-col gap-1 px-3">
        {navItems.map(({ to, label, icon: Icon, end }) => (
          <NavLink
            key={to}
            to={to}
            end={end}
            title={collapsed ? label : undefined}
            className={({ isActive }) =>
              cn(
                "flex items-center gap-3 rounded-md py-2 text-sm font-medium transition-colors",
                collapsed ? "justify-center px-2" : "px-3",
                isActive
                  ? "bg-primary text-primary-foreground"
                  : "text-muted-foreground hover:bg-background hover:text-foreground",
              )
            }
          >
            <Icon className="size-5 shrink-0" aria-hidden="true" />
            {!collapsed && <span className="flex-1">{label}</span>}
          </NavLink>
        ))}
      </nav>

      <div
        className={cn(
          "mt-auto flex flex-col gap-1 pb-4",
          collapsed ? "px-2" : "px-3",
        )}
      >
        <ThemeToggle collapsed={collapsed} />

        {user ? (
          <AccountMenu collapsed={collapsed} />
        ) : (
          <NavLink
            to="/login"
            aria-label="Log in"
            title={collapsed ? "Log in" : undefined}
            className={cn(
              "flex w-full items-center gap-3 rounded-md py-2 text-sm font-medium text-primary transition-colors hover:bg-background",
              collapsed ? "justify-center px-2" : "px-3",
            )}
          >
            <LogIn className="size-5 shrink-0" aria-hidden="true" />
            {!collapsed && "Log in / Sign up"}
          </NavLink>
        )}
      </div>
      </aside>
    </>
  )
}
