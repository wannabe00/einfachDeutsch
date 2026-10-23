import { SITE_NAME } from "@/lib/site"
import { Clause, ContactLink, LegalLayout } from "./LegalLayout"

export default function CookiesPage() {
  return (
    <LegalLayout
      title="Cookie Policy"
      intro={`${SITE_NAME} uses no advertising or tracking cookies, so there's no cookie banner.`}
    >
      <Clause title="What your browser stores">
        <ul>
          <li>
            <strong>Your sign-in</strong>, so you stay logged in (local storage). Strictly necessary.
          </li>
          <li>
            <strong>For visitors without an account,</strong> how many free lessons were tried
            (local storage).
          </li>
          <li>
            <strong>Small preferences</strong> such as light or dark mode and settings you open often
            (local storage).
          </li>
          <li>
            <strong>A short-lived security value</strong> while you sign in with Google or GitHub
            (session storage), deleted right after.
          </li>
        </ul>
        <p>
          These are only used by {SITE_NAME} itself, never for advertising or to follow you across
          sites. Clearing your browser's site data removes them (and signs you out).
        </p>
      </Clause>
      <Clause title="Other services">
        <p>
          Error reports are sent to Sentry without cookies. Google or GitHub may set their own cookies
          on their sign-in pages, under their policies. We don't use analytics or tracking tools; if
          that ever changes, this page and, where needed, a consent choice come first.
        </p>
      </Clause>
      <Clause title="Questions">
        <p>
          <ContactLink />
        </p>
      </Clause>
    </LegalLayout>
  )
}
