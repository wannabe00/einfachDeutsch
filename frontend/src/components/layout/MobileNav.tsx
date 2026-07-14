import { useEffect } from "react"
import { NavLink } from "react-router-dom"

import { cn } from "@/lib/utils"
import { dashboardItem, aiItem, navGroups, type NavLeaf } from "./navItems"

/*
 * Mobile navigation drawer — slides in from the left under the top bar. On phones
 * a drawer beats the desktop top bar (all items reachable with one thumb), so the
 * full nav lives here, grouped with section labels. Controlled by the top bar's
 * hamburger; closes on backdrop tap, Escape, or any link tap. While open it locks
 * body scroll so the page behind doesn't move.
 */
export function MobileNav({ open, onClose }: { open: boolean; onClose: () => void }) {
  useEffect(() => {
    if (!open) return
    const prevOverflow = document.body.style.overflow
    document.body.style.overflow = "hidden"
    const onKey = (e: KeyboardEvent) => {
      if (e.key === "Escape") onClose()
    }
    document.addEventListener("keydown", onKey)
    return () => {
      document.body.style.overflow = prevOverflow
      document.removeEventListener("keydown", onKey)
    }
  }, [open, onClose])

  return (
    <div className="md:hidden" aria-hidden={!open}>
      {/* Backdrop */}
      <div
        onClick={onClose}
        className={cn(
          "fixed inset-x-0 bottom-0 top-16 z-40 bg-black/60 transition-opacity duration-200",
          open ? "opacity-100" : "pointer-events-none opacity-0",
        )}
      />

      {/* Drawer panel */}
      <nav
        className={cn(
          "fixed bottom-0 left-0 top-16 z-50 w-[min(18rem,82vw)] overflow-y-auto border-r border-border bg-surface p-3 transition-transform duration-200 ease-out",
          open ? "translate-x-0" : "-translate-x-full",
        )}
      >
        <DrawerLink item={dashboardItem} onClose={onClose} />

        {navGroups.map((group) => (
          <div key={group.label} className="mt-4">
            <p className="px-3 pb-1 text-xs font-semibold uppercase tracking-wider text-muted-foreground">
              {group.label}
            </p>
            {group.items.map((item) => (
              <DrawerLink key={item.to} item={item} onClose={onClose} />
            ))}
          </div>
        ))}

        <div className="mt-4 border-t border-border pt-3">
          <DrawerLink item={aiItem} onClose={onClose} />
        </div>
      </nav>
    </div>
  )
}

function DrawerLink({ item, onClose }: { item: NavLeaf; onClose: () => void }) {
  const { to, label, icon: Icon, end } = item
  return (
    <NavLink
      to={to}
      end={end}
      onClick={onClose}
      className={({ isActive }) =>
        cn(
          "flex min-h-[44px] items-center gap-3 rounded-md px-3 py-3 text-sm font-medium transition-colors",
          isActive
            ? "bg-primary/15 text-foreground"
            : "text-muted-foreground hover:bg-background hover:text-foreground",
        )
      }
    >
      <Icon className="size-5 shrink-0" aria-hidden="true" />
      {label}
    </NavLink>
  )
}
