import type { ReactNode } from "react"
import { Database, Mic, ShieldCheck, Sparkles, type LucideIcon } from "lucide-react"

import { SITE_NAME } from "@/lib/site"
import { BackLink } from "@/components/ui/BackLink"
import { Logo } from "@/components/layout/TopBar"

/* A plain-language privacy summary. Lives outside the app shell (it's linked
   from the landing footer), so it brings its own logo and back link. */
export default function PrivacyPage() {
  return (
    <div className="min-h-screen bg-background px-4 py-6 text-foreground sm:px-6 sm:py-10">
      <div className="mx-auto max-w-2xl">
        <div className="flex items-center justify-between">
          <BackLink to="/" label={SITE_NAME} />
          <Logo className="hidden sm:flex" />
        </div>
        <h1 className="mt-6 text-4xl font-extrabold">Privacy</h1>
        <p className="mt-2 text-lg text-muted-foreground">
          A short, plain-language summary of how {SITE_NAME} handles your data.
        </p>

        <div className="mt-8 flex flex-col gap-4">
          <Item icon={Database} color="hsl(var(--section-1))" title="What we store">
            Your email, a securely hashed password (never the plain text), your CEFR level, and
            your learning progress (reviews, exercise attempts, streaks, completed lessons).
            That's it.
          </Item>
          <Item icon={Mic} color="hsl(var(--section-6))" title="Speaking practice">
            In Talk to AI your voice is streamed live to Google Gemini to hold the conversation.
            We <strong>never store the audio</strong>; only the text transcript and your report are
            kept, so you can read them again.
          </Item>
          <Item icon={Sparkles} color="hsl(var(--section-3))" title="AI features">
            Text you send to the AI tutor, Talk to AI and AI grading is processed by a third-party AI
            provider to generate responses. Don't share sensitive personal information in those
            fields.
          </Item>
          <Item icon={ShieldCheck} color="hsl(var(--section-4))" title="Your control">
            You can stop using your account at any time. To request deletion of your account and
            data, contact the site owner.
          </Item>
        </div>

        <p className="mt-8 text-sm text-muted-foreground">
          This is a summary for a personal-scale project, not a formal legal policy. It will be
          expanded before any wider public launch.
        </p>
      </div>
    </div>
  )
}

function Item({
  icon: Icon,
  color,
  title,
  children,
}: {
  icon: LucideIcon
  color: string
  title: string
  children: ReactNode
}) {
  return (
    <section className="flex gap-4 rounded-[24px] bg-surface p-5 shadow-card sm:p-6">
      <span
        className="flex size-11 shrink-0 items-center justify-center rounded-2xl text-white"
        style={{ background: color }}
      >
        <Icon className="size-5" aria-hidden="true" />
      </span>
      <div>
        <h2 className="text-lg font-bold">{title}</h2>
        <p className="mt-1 leading-relaxed text-muted-foreground">{children}</p>
      </div>
    </section>
  )
}
