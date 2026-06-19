/**
 * Freemium access policy (decided 2026-06-19).
 *
 * Guests may use the "free to the owner" features (read-only or cheap, and
 * rate-limited on the backend). Account-only features either cost the owner
 * money/quota (AI, Recite) or are reserved by product decision (Drills), plus
 * anything that writes per-user progress or edits content.
 *
 * The backend is the real enforcement boundary (DRF throttling + per-view
 * auth); these flags drive the UI (route guards, lock badges, sign-up wall).
 */

/** Routes a guest cannot open — they get bounced to /login. */
export const ACCOUNT_ONLY_PATHS = ["/drills", "/ai", "/speak"] as const

export function isAccountOnlyPath(path: string): boolean {
  return ACCOUNT_ONLY_PATHS.some((p) => path === p || path.startsWith(`${p}/`))
}

/**
 * Max "actions" (a graded exercise, a reviewed card, etc.) a signed-out guest
 * may perform per calendar day before the sign-up wall appears. Signed-in users
 * are unlimited. This is UX only — the backend throttles independently.
 */
export const GUEST_DAILY_ACTION_LIMIT = 20
