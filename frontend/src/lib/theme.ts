/*
 * Light / dark choice. "system" follows the device; "light" and "dark" pin it.
 * Stored per device (it's a display preference) and applied as `data-theme`
 * on <html>, which index.css reads.
 */
export type ThemePref = "system" | "light" | "dark"

const KEY = "theme"

export function getThemePref(): ThemePref {
  try {
    const v = localStorage.getItem(KEY)
    if (v === "light" || v === "dark") return v
  } catch {
    // Storage can be blocked (private mode); fall back to the device setting.
  }
  return "system"
}

export function applyTheme(pref: ThemePref) {
  const root = document.documentElement
  if (pref === "system") root.removeAttribute("data-theme")
  else root.setAttribute("data-theme", pref)
}

export function setThemePref(pref: ThemePref) {
  try {
    if (pref === "system") localStorage.removeItem(KEY)
    else localStorage.setItem(KEY, pref)
  } catch {
    // Not saved, but still applied for this visit.
  }
  applyTheme(pref)
}
