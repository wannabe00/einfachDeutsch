import { useEffect, type ReactNode } from "react"

/*
 * The app is dark-only (Design v2 — Cinematic). There is no light theme and no
 * toggle: this provider simply pins the `dark` class on <html> so the design
 * tokens in index.css resolve to the cinematic palette. Kept as a provider (not
 * inlined) so the single place that owns "the app is dark" is obvious, and so a
 * future theme system has a home to slot back into.
 */
export function ThemeProvider({ children }: { children: ReactNode }) {
  useEffect(() => {
    const root = document.documentElement
    root.classList.add("dark")
    // Clear any theme preference persisted by the old light/dark toggle.
    localStorage.removeItem("theme")
  }, [])

  return <>{children}</>
}
