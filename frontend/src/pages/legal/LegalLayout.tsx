import type { ReactNode } from "react"
import { Link } from "react-router-dom"

import { CONTACT_EMAIL, LEGAL_PAGES, LEGAL_UPDATED, SITE_NAME } from "@/lib/site"
import { usePageTitle } from "@/lib/usePageTitle"
import { BackLink } from "@/components/ui/BackLink"
import { Logo } from "@/components/layout/TopBar"

/* The frame of the legal pages: outside the app shell (they're linked from
   the landing page and sign-in), with their own logo, back link and the
   links between them. */
export function LegalLayout({ title, intro, children }: { title: string; intro: string; children: ReactNode }) {
  usePageTitle(title)
  return (
    <div className="min-h-screen bg-background px-4 py-6 text-foreground sm:px-6 sm:py-10">
      <div className="mx-auto max-w-2xl">
        <div className="flex items-center justify-between">
          <BackLink to="/" label={SITE_NAME} />
          <Logo className="hidden sm:flex" />
        </div>
        <h1 className="mt-6 text-4xl font-extrabold">{title}</h1>
        <p className="mt-2 text-sm text-muted-foreground">Last updated {LEGAL_UPDATED}</p>
        <p className="mt-4 text-lg text-muted-foreground">{intro}</p>
        <div className="mt-8 flex flex-col gap-4">{children}</div>
        <nav aria-label="Legal" className="mt-10 flex flex-wrap gap-x-5 gap-y-2 border-t border-border pt-6 text-sm">
          {LEGAL_PAGES.map((p) => (
            <Link key={p.to} to={p.to} className="text-muted-foreground hover:text-foreground">
              {p.label}
            </Link>
          ))}
        </nav>
      </div>
    </div>
  )
}

/** One numbered or titled section of a legal page. */
export function Clause({ title, children }: { title: string; children: ReactNode }) {
  return (
    <section className="rounded-[24px] bg-surface p-5 shadow-card sm:p-6">
      <h2 className="text-lg font-bold">{title}</h2>
      <div className="mt-2 flex flex-col gap-2 leading-relaxed text-muted-foreground [&_a]:font-semibold [&_a]:text-primary [&_li]:ml-5 [&_li]:list-disc [&_strong]:text-foreground">
        {children}
      </div>
    </section>
  )
}

/** The contact address as a mail link. */
export function ContactLink() {
  return <a href={`mailto:${CONTACT_EMAIL}`}>{CONTACT_EMAIL}</a>
}
