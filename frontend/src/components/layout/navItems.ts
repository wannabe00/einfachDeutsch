import {
  LayoutDashboard,
  Route as RouteIcon,
  GraduationCap,
  NotebookPen,
  Swords,
  Mic,
  BookMarked,
  BookOpen,
  Library,
  Tv,
  Landmark,
  Sparkles,
} from "lucide-react"
import type { LucideIcon } from "lucide-react"

/* Shared navigation model — consumed by both the desktop top bar (grouped
   dropdowns) and the mobile drawer, so the two never drift apart. Same items as
   before; only the presentation changed. */

export interface NavLeaf {
  to: string
  label: string
  icon: LucideIcon
  /** exact-match highlighting (only Dashboard, at "/") */
  end?: boolean
}

export interface NavGroup {
  label: string
  items: NavLeaf[]
}

/** Standalone links that sit on their own in the bar (not under a menu). */
export const dashboardItem: NavLeaf = {
  to: "/",
  label: "Dashboard",
  icon: LayoutDashboard,
  end: true,
}
/** The learning path — the spine of the app (Phase 23), so it sits top-level. */
export const pathItem: NavLeaf = { to: "/path", label: "Path", icon: RouteIcon }
export const aiItem: NavLeaf = { to: "/ai", label: "AI Assistant", icon: Sparkles }

/** The grouped menus between Dashboard and AI Assistant. */
export const navGroups: NavGroup[] = [
  {
    label: "Practice",
    items: [
      { to: "/review", label: "Review", icon: GraduationCap },
      { to: "/exercises", label: "Exercises", icon: NotebookPen },
      { to: "/drills", label: "Drills", icon: Swords },
      { to: "/speak", label: "Recite", icon: Mic },
    ],
  },
  {
    label: "Library",
    items: [
      { to: "/words", label: "Word Bank", icon: BookMarked },
      { to: "/grammar", label: "Grammar", icon: BookOpen },
      { to: "/books", label: "Books", icon: Library },
    ],
  },
  {
    label: "Explore",
    items: [
      { to: "/videos", label: "Videos", icon: Tv },
      { to: "/history", label: "History", icon: Landmark },
    ],
  },
]
