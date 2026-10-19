/*
 * Error tracking (sentry.io), only when VITE_SENTRY_DSN is set. Loaded as its
 * own chunk after start-up so the app's first load stays small. No personal
 * data: no user details, no session replay, no performance tracing.
 */
export function startMonitoring() {
  const dsn = import.meta.env.VITE_SENTRY_DSN as string | undefined
  if (!dsn) return
  void import("@sentry/react").then((Sentry) =>
    Sentry.init({ dsn, environment: import.meta.env.MODE }),
  )
}
