import { useEffect } from "react"
import { NavLink } from "react-router-dom"
import { Settings } from "lucide-react"

import { useAuth } from "@/contexts/AuthContext"
import { cn } from "@/lib/utils"
import { aiItem, navGroups, type NavLeaf } from "./navItems"

/*
 * Bottom sheet behind the tab bar's "More" button: every page that isn't a
 * tab, grouped like the desktop menus. Closes on a backdrop tap, Escape or any
 * link, and locks page scrolling while open.
 */
export function MoreSheet({ open, onClose }: { open: boolean; onClose: () => void }) {
  const { user } = useAuth()

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

  // Review and Word Bank are tabs already.
  const groups = navGroups.map((g) => ({
    ...g,
    items: g.items.filter((it) => it.to !== "/review" && it.to !== "/words"),
  }))
  const extra: NavLeaf[] = [aiItem]
  if (user) extra.push({ to: "/settings", label: "Settings", icon: Settings })

  return (
    <div className="lg:hidden" aria-hidden={!open}>
      <div
        onClick={onClose}
        className={cn(
          "fixed inset-0 z-40 bg-black/40 transition-opacity duration-200",
          open ? "opacity-100" : "pointer-events-none opacity-0",
        )}
      />
      <div
        role="dialog"
        aria-modal="true"
        aria-label="More pages"
        className={cn(
          "fixed inset-x-0 bottom-0 z-50 max-h-[85vh] overflow-y-auto rounded-t-[28px] bg-surface px-4 pb-[max(env(safe-area-inset-bottom),16px)] pt-2 shadow-lift transition-transform duration-300 ease-out",
          open ? "translate-y-0" : "pointer-events-none translate-y-full",
        )}
      >
        <div className="mx-auto mb-3 h-1.5 w-10 rounded-full bg-surface-2" aria-hidden="true" />
        {groups.map((group) => (
          <div key={group.label} className="mb-4">
            <p className="px-2 pb-1.5 text-[13px] font-semibold uppercase tracking-[0.04em] text-muted-foreground">
              {group.label}
            </p>
            <div className="overflow-hidden rounded-2xl bg-surface-2/60">
              {group.items.map((item) => (
                <SheetLink key={item.to} item={item} onClose={onClose} />
              ))}
            </div>
          </div>
        ))}
        <div className="overflow-hidden rounded-2xl bg-surface-2/60">
          {extra.map((item) => (
            <SheetLink key={item.to} item={item} onClose={onClose} />
          ))}
        </div>
      </div>
    </div>
  )
}

function SheetLink({ item, onClose }: { item: NavLeaf; onClose: () => void }) {
  const { to, label, icon: Icon } = item
  return (
    <NavLink
      to={to}
      onClick={onClose}
      className={({ isActive }) =>
        cn(
          "flex min-h-[52px] items-center gap-3 px-4 text-[16px] transition-colors [&:not(:last-child)]:border-b [&:not(:last-child)]:border-border/70",
          isActive ? "font-semibold text-primary" : "text-foreground active:bg-surface-2",
        )
      }
    >
      <Icon className="size-5 shrink-0 text-muted-foreground" aria-hidden="true" />
      {label}
    </NavLink>
  )
}
