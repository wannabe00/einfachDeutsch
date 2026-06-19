import { Moon, Sun } from "lucide-react"

import { useTheme } from "@/contexts/ThemeContext"
import { cn } from "@/lib/utils"

interface ThemeToggleProps {
  collapsed?: boolean
}

export function ThemeToggle({ collapsed }: ThemeToggleProps) {
  const { theme, toggleTheme } = useTheme()
  const isDark = theme === "dark"
  const label = isDark ? "Light mode" : "Dark mode"

  return (
    <button
      onClick={toggleTheme}
      aria-label={isDark ? "Switch to light mode" : "Switch to dark mode"}
      title={collapsed ? label : undefined}
      className={cn(
        "flex w-full items-center gap-3 rounded-md py-2 text-sm font-medium text-muted-foreground transition-colors hover:bg-background hover:text-foreground",
        collapsed ? "justify-center px-2" : "px-3",
      )}
    >
      {isDark ? (
        <Sun className="size-5 shrink-0" aria-hidden="true" />
      ) : (
        <Moon className="size-5 shrink-0" aria-hidden="true" />
      )}
      {!collapsed && label}
    </button>
  )
}
