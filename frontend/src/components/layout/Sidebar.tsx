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
  PanelLeftClose,
  PanelLeft,
} from "lucide-react"

import { cn } from "@/lib/utils"
import { SITE_NAME } from "@/lib/site"
import { ThemeToggle } from "./ThemeToggle"

const navItems = [
  { to: "/", label: "Dashboard", icon: LayoutDashboard, end: true },
  { to: "/review", label: "Review", icon: GraduationCap, end: false },
  { to: "/words", label: "Word Bank", icon: BookMarked, end: false },
  { to: "/grammar", label: "Grammar", icon: BookOpen, end: false },
  { to: "/exercises", label: "Exercises", icon: NotebookPen, end: false },
  { to: "/drills", label: "Drills", icon: Swords, end: false },
  { to: "/speak", label: "Recite", icon: Mic, end: false },
  { to: "/books", label: "Books", icon: Library, end: false },
  { to: "/ai", label: "AI Assistant", icon: Sparkles, end: false },
]

const STORAGE_KEY = "sidebar-collapsed"

export function Sidebar() {
  const [collapsed, setCollapsed] = useState(
    () => localStorage.getItem(STORAGE_KEY) === "true",
  )

  useEffect(() => {
    localStorage.setItem(STORAGE_KEY, String(collapsed))
  }, [collapsed])

  return (
    <aside
      className={cn(
        "sticky top-0 flex h-screen shrink-0 flex-col border-r border-border bg-surface transition-[width] duration-200",
        collapsed ? "w-16" : "w-60",
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
            {!collapsed && label}
          </NavLink>
        ))}
      </nav>

      <div className={cn("mt-auto pb-4", collapsed ? "px-2" : "px-3")}>
        <ThemeToggle collapsed={collapsed} />
      </div>
    </aside>
  )
}
