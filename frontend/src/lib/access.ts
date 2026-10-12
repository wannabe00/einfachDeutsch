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

/**
 * How many "actions" (a graded exercise, a reviewed card, ...) a signed-out
 * guest gets per day before the sign-up prompt appears. Signed-in users have no
 * limit. This is only a UI nudge; the backend has its own throttling.
 */
export const GUEST_DAILY_ACTION_LIMIT = 20
