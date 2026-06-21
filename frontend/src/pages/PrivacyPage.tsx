import { Link } from "react-router-dom"

import { SITE_NAME } from "@/lib/site"

export default function PrivacyPage() {
  return (
    <div className="min-h-screen bg-background px-6 py-10 text-foreground">
      <div className="mx-auto max-w-2xl">
        <Link to="/" className="text-sm font-medium text-accent hover:underline">
          ← {SITE_NAME}
        </Link>
        <h1 className="mt-6 text-2xl font-semibold tracking-tight">Privacy</h1>
        <p className="mt-1 text-sm text-muted-foreground">
          A short, plain-language summary of how {SITE_NAME} handles your data.
        </p>

        <div className="mt-6 flex flex-col gap-5 text-sm leading-relaxed">
        <section>
          <h2 className="font-semibold">What we store</h2>
          <p className="mt-1 text-muted-foreground">
            Your email, a securely hashed password (never the plain text), your
            CEFR level, and your learning progress (reviews, exercise attempts,
            streaks, completed lessons). That's it.
          </p>
        </section>

        <section>
          <h2 className="font-semibold">Speaking practice</h2>
          <p className="mt-1 text-muted-foreground">
            Recordings you make in Recite are transcribed and then{" "}
            <strong>discarded</strong> — the audio is never stored. Only the
            transcript and your score are kept.
          </p>
        </section>

        <section>
          <h2 className="font-semibold">AI features</h2>
          <p className="mt-1 text-muted-foreground">
            Text you send to the AI tutor and recitation grading is processed by
            a third-party AI provider to generate responses. Don't share
            sensitive personal information in those fields.
          </p>
        </section>

        <section>
          <h2 className="font-semibold">Your control</h2>
          <p className="mt-1 text-muted-foreground">
            You can stop using your account at any time. To request deletion of
            your account and data, contact the site owner.
          </p>
        </section>

          <p className="text-xs text-muted-foreground">
            This is a summary for a personal-scale project, not a formal legal
            policy. It will be expanded before any wider public launch.
          </p>
        </div>
      </div>
    </div>
  )
}
