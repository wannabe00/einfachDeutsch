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

/* Navigation items, shared by the desktop top bar and the mobile drawer so
   both always list the same pages. */

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
/** The learning path is the core of the app, so it gets a top-level link. */
export const pathItem: NavLeaf = { to: "/path", label: "Path", icon: RouteIcon }
export const aiItem: NavLeaf = { to: "/ai", label: "AI Assistant", icon: Sparkles }

/** The grouped menus between Dashboard and AI Assistant. */
export const navGroups: NavGroup[] = [
  {
    label: "Practice",
    items: [
      { to: "/review", label: "Review", icon: GraduationCap },
      { to: "/exercises", label: "Practice", icon: NotebookPen },
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
