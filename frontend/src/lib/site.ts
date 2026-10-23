/** The product name. Import this instead of hardcoding it in components. */
export const SITE_NAME = "einfachDeutsch"

/** Who runs the site, for the legal pages. */
export const OPERATOR_NAME = "Levan Kobakhidze"
export const OPERATOR_COUNTRY = "Georgia"
export const CONTACT_EMAIL = "00wannabe11@gmail.com"
/** The youngest age allowed to make an account. */
export const MIN_AGE = 16
/** When the Terms, Privacy, Refund and Cookie pages last changed. */
export const LEGAL_UPDATED = "20 October 2026"

/** The legal pages, linked from the landing footer, sign-in and Settings. */
export const LEGAL_PAGES = [
  { to: "/terms", label: "Terms" },
  { to: "/privacy", label: "Privacy" },
  { to: "/refunds", label: "Refunds" },
  { to: "/cookies", label: "Cookies" },
]

/** Premium prices as Stripe charges them (the price IDs live in the backend env). */
export const PRICES = { monthly: "$2.99", annual: "$29.99" }

/** The course's levels: it ends at B1 (the backend's COURSE_LEVELS). */
export const COURSE_LEVELS = ["A1", "A2", "B1"] as const
