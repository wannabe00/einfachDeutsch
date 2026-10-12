/**
 * Counts a signed-out guest's "actions" per day in localStorage (a graded
 * exercise, a reviewed card, a drill answer). At the daily limit the UI shows
 * the sign-up prompt. The backend never trusts this counter; it throttles on
 * its own.
 */
import { GUEST_DAILY_ACTION_LIMIT } from "./access"

const STORAGE_KEY = "guest_actions"

function today(): string {
  return new Date().toISOString().slice(0, 10) // YYYY-MM-DD (local-ish)
}

interface GuestActionState {
  date: string
  count: number
}

function read(): GuestActionState {
  try {
    const raw = localStorage.getItem(STORAGE_KEY)
    if (raw) {
      const parsed = JSON.parse(raw) as GuestActionState
      if (parsed.date === today()) return parsed
    }
  } catch {
    // ignore malformed storage
  }
  return { date: today(), count: 0 }
}

function guestActionCount(): number {
  return read().count
}

export function guestLimitReached(): boolean {
  return guestActionCount() >= GUEST_DAILY_ACTION_LIMIT
}

/** Record one guest action. Returns the new count. */
export function recordGuestAction(): number {
  const state = read()
  const next = { date: today(), count: state.count + 1 }
  try {
    localStorage.setItem(STORAGE_KEY, JSON.stringify(next))
  } catch {
    // ignore storage write failures (private mode, etc.)
  }
  return next.count
}
