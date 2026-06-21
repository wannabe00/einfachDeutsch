import { useEffect, useRef, useState } from "react"
import { Link } from "react-router-dom"
import {
  BookMarked,
  BrainCircuit,
  CalendarCheck,
  ChevronDown,
  Clapperboard,
  GraduationCap,
  Landmark,
  Mic,
  Sparkles,
  Swords,
} from "lucide-react"

import { SITE_NAME } from "@/lib/site"
import { Button } from "@/components/ui/button"
import { cn } from "@/lib/utils"

// Swap these for your own photos anytime (e.g. files in /public). A gradient
// shows underneath if the image fails to load.
const HERO_IMG =
  "https://images.unsplash.com/photo-1595867818082-083862f3d630?auto=format&fit=crop&w=2400&q=80"

export default function LandingPage() {
  const imgRef = useRef<HTMLImageElement>(null)
  const [imgOk, setImgOk] = useState(true)

  // Parallax: drift the photo slower than the page as you scroll (no re-render).
  useEffect(() => {
    function onScroll() {
      if (imgRef.current) {
        imgRef.current.style.transform = `translateY(${window.scrollY * 0.4}px)`
      }
    }
    window.addEventListener("scroll", onScroll, { passive: true })
    return () => window.removeEventListener("scroll", onScroll)
  }, [])

  return (
    <div className="bg-background text-foreground">
      <Hero imgRef={imgRef} imgOk={imgOk} onImgError={() => setImgOk(false)} />
      <ValueProps />
      <HowItWorks />
      <Teaser />
      <FeatureShowcase />
      <CefrPath />
      <CultureHook />
      <Stats />
      <FaqAndCta />
    </div>
  )
}

function TopBar() {
  return (
    <header className="absolute inset-x-0 top-0 z-20 flex items-center justify-between px-6 py-5">
      <span className="text-lg font-semibold tracking-tight text-white drop-shadow">
        {SITE_NAME}
      </span>
      <div className="flex items-center gap-2">
        <Button asChild variant="ghost" className="text-white hover:bg-white/15">
          <Link to="/login">Log in</Link>
        </Button>
        <Button asChild>
          <Link to="/register">Sign up</Link>
        </Button>
      </div>
    </header>
  )
}

function Hero({
  imgRef,
  imgOk,
  onImgError,
}: {
  imgRef: React.RefObject<HTMLImageElement | null>
  imgOk: boolean
  onImgError: () => void
}) {
  return (
    <section className="relative flex h-screen min-h-[560px] items-center justify-center overflow-hidden">
      {/* Gradient fallback (always present, behind the photo) */}
      <div className="absolute inset-0 bg-gradient-to-br from-[#1b2a4a] via-[#24304d] to-[#3a2a4d]" />
      {imgOk && (
        <img
          ref={imgRef}
          src={HERO_IMG}
          alt="Munich — Marienplatz"
          onError={onImgError}
          className="absolute inset-0 h-[130%] w-full object-cover"
        />
      )}
      <div className="absolute inset-0 bg-black/55" />

      <TopBar />

      <div className="relative z-10 mx-auto max-w-3xl px-6 text-center text-white">
        <h1 className="text-4xl font-bold leading-tight tracking-tight sm:text-6xl">
          Learn German that actually sticks.
        </h1>
        <p className="mx-auto mt-5 max-w-xl text-lg text-white/85">
          Spaced-repetition flashcards, real grammar and exercises, drills, an AI
          tutor, speaking practice, and German culture — all in one place, paced
          to your level.
        </p>
        <div className="mt-8 flex flex-col items-center justify-center gap-3 sm:flex-row">
          <Button asChild size="lg" className="w-full sm:w-auto">
            <Link to="/register">Start free</Link>
          </Button>
          <Button
            asChild
            size="lg"
            variant="outline"
            className="w-full border-white/40 bg-white/10 text-white hover:bg-white/20 sm:w-auto"
          >
            <Link to="/register">Take the 2-minute level test</Link>
          </Button>
        </div>
      </div>

      <ChevronDown className="absolute bottom-6 left-1/2 z-10 size-7 -translate-x-1/2 animate-bounce text-white/80" />
    </section>
  )
}

const VALUES = [
  {
    icon: GraduationCap,
    title: "Words that come back",
    body: "An SM-2 spaced-repetition engine schedules each word so you review it right before you'd forget it.",
  },
  {
    icon: Clapperboard,
    title: "Learn from real German",
    body: "Curated shows, channels, and podcasts matched to your level — unlocked as you progress.",
  },
  {
    icon: Sparkles,
    title: "An AI tutor on tap",
    body: "Explanations, generated exercises, and instant feedback on your answers, whenever you're stuck.",
  },
  {
    icon: CalendarCheck,
    title: "Practice that fits your week",
    body: "New lessons Mon/Wed/Fri, reviews any day, and streaks with freeze tokens to keep momentum.",
  },
]

function ValueProps() {
  return (
    <Section>
      <SectionHeading
        eyebrow="Why it works"
        title="Built for people who actually want to remember"
      />
      <div className="grid gap-5 sm:grid-cols-2 lg:grid-cols-4">
        {VALUES.map((v) => (
          <div
            key={v.title}
            className="rounded-xl border border-border bg-surface p-5"
          >
            <div className="flex size-10 items-center justify-center rounded-lg bg-accent/10 text-accent">
              <v.icon className="size-5" />
            </div>
            <h3 className="mt-3 font-semibold">{v.title}</h3>
            <p className="mt-1 text-sm text-muted-foreground">{v.body}</p>
          </div>
        ))}
      </div>
    </Section>
  )
}

const STEPS = [
  {
    n: "1",
    title: "Find your level",
    body: "Take a short placement test (or pick A1–C2). We tune everything to you.",
  },
  {
    n: "2",
    title: "Learn on a rhythm",
    body: "Fresh lessons Mon/Wed/Fri, reviews and drills any day. Small, steady, sustainable.",
  },
  {
    n: "3",
    title: "Keep your streak",
    body: "Build a habit with streaks and freeze tokens — and watch new content unlock as you climb.",
  },
]

function HowItWorks() {
  return (
    <Section muted>
      <SectionHeading eyebrow="How it works" title="Three steps to fluency" />
      <div className="grid gap-5 sm:grid-cols-3">
        {STEPS.map((s) => (
          <div key={s.n} className="rounded-xl border border-border bg-background p-6">
            <div className="flex size-9 items-center justify-center rounded-full bg-accent text-base font-bold text-accent-foreground">
              {s.n}
            </div>
            <h3 className="mt-3 font-semibold">{s.title}</h3>
            <p className="mt-1 text-sm text-muted-foreground">{s.body}</p>
          </div>
        ))}
      </div>
    </Section>
  )
}

const TEASER = [
  { noun: "Hund", en: "dog", article: "der" },
  { noun: "Katze", en: "cat", article: "die" },
  { noun: "Haus", en: "house", article: "das" },
] as const
const ARTICLE_VAR: Record<string, string> = {
  der: "--article-der",
  die: "--article-die",
  das: "--article-das",
}

function Teaser() {
  const [i, setI] = useState(0)
  const [picked, setPicked] = useState<string | null>(null)
  const [score, setScore] = useState(0)
  const done = i >= TEASER.length
  const current = TEASER[i] ?? TEASER[0]

  function choose(a: string) {
    if (picked) return
    setPicked(a)
    if (a === current.article) setScore((s) => s + 1)
    window.setTimeout(() => {
      setPicked(null)
      setI((n) => n + 1)
    }, 750)
  }

  return (
    <Section>
      <SectionHeading
        eyebrow="Try it now"
        title="der, die, or das? Give it a go"
      />
      <div className="mx-auto max-w-md rounded-2xl border border-border bg-surface p-8 text-center">
        {done ? (
          <>
            <p className="text-lg font-semibold">You got {score}/{TEASER.length}.</p>
            <p className="mt-1 text-sm text-muted-foreground">
              Gender is hard — that's exactly what the drills train. Make a free
              account to keep going.
            </p>
            <Button asChild className="mt-5">
              <Link to="/register">Create a free account</Link>
            </Button>
          </>
        ) : (
          <>
            <p className="text-sm text-muted-foreground">
              Which article? ({current.en})
            </p>
            <p className="mt-2 text-3xl font-bold">{current.noun}</p>
            <div className="mt-6 grid grid-cols-3 gap-3">
              {(["der", "die", "das"] as const).map((a) => {
                const isCorrect = picked && a === current.article
                const isWrong = picked === a && a !== current.article
                return (
                  <button
                    key={a}
                    onClick={() => choose(a)}
                    disabled={!!picked}
                    className={cn(
                      "rounded-xl border-2 py-4 text-lg font-bold transition-colors",
                      isCorrect
                        ? "border-[hsl(var(--success))] bg-[hsl(var(--success-bg))] text-[hsl(var(--success))]"
                        : isWrong
                          ? "border-[hsl(var(--danger))] bg-[hsl(var(--danger-bg))] text-[hsl(var(--danger))]"
                          : "border-border hover:border-accent",
                    )}
                    style={
                      !picked
                        ? { color: `hsl(var(${ARTICLE_VAR[a]}))` }
                        : undefined
                    }
                  >
                    {a}
                  </button>
                )
              })}
            </div>
          </>
        )}
      </div>
    </Section>
  )
}

const FEATURES = [
  { icon: GraduationCap, title: "Review", body: "Flashcards that ask you to produce the German — with the right article." },
  { icon: BookMarked, title: "Word Bank", body: "Build vocabulary chapter by chapter; import your own lists." },
  { icon: Swords, title: "Drills", body: "Fast, focused games: gender triage, unscramble, recall, and more." },
  { icon: Mic, title: "Recite", body: "Read a text, retell it aloud, get scored on coverage and grammar." },
  { icon: BrainCircuit, title: "Exercises", body: "Interactive practice with instant, server-checked answers." },
  { icon: Landmark, title: "History", body: "Bite-size German history — in English then German as you level up." },
]

function FeatureShowcase() {
  return (
    <Section muted>
      <SectionHeading
        eyebrow="What's inside"
        title="Everything you need, in one app"
      />
      <div className="grid gap-5 sm:grid-cols-2 lg:grid-cols-3">
        {FEATURES.map((f) => (
          <div key={f.title} className="rounded-xl border border-border bg-background p-5">
            <div className="flex items-center gap-3">
              <div className="flex size-9 items-center justify-center rounded-lg bg-accent/10 text-accent">
                <f.icon className="size-5" />
              </div>
              <h3 className="font-semibold">{f.title}</h3>
            </div>
            <p className="mt-2 text-sm text-muted-foreground">{f.body}</p>
          </div>
        ))}
      </div>
    </Section>
  )
}

const LEVELS = [
  { l: "A1", t: "Basics & greetings" },
  { l: "A2", t: "Everyday situations" },
  { l: "B1", t: "Videos & shows unlock" },
  { l: "B2", t: "Fluent, spontaneous" },
  { l: "C1", t: "Advanced & idiomatic" },
  { l: "C2", t: "Mastery" },
]

function CefrPath() {
  return (
    <Section>
      <SectionHeading
        eyebrow="Your path"
        title="Climb from A1 to C2"
        subtitle="Content unlocks as you progress — so you're always learning at the right level."
      />
      <div className="flex flex-wrap items-stretch justify-center gap-3">
        {LEVELS.map((lvl) => (
          <div
            key={lvl.l}
            className="flex w-[140px] flex-col rounded-xl border border-border bg-surface p-4"
          >
            <span className="text-2xl font-bold text-accent">{lvl.l}</span>
            <span className="mt-1 text-xs text-muted-foreground">{lvl.t}</span>
          </div>
        ))}
      </div>
    </Section>
  )
}

function CultureHook() {
  return (
    <Section muted>
      <div className="grid items-center gap-8 lg:grid-cols-2">
        <div>
          <p className="text-xs font-semibold uppercase tracking-wide text-accent">
            More than vocabulary
          </p>
          <h2 className="mt-2 text-2xl font-semibold tracking-tight sm:text-3xl">
            Learn the language and the country
          </h2>
          <p className="mt-3 text-muted-foreground">
            Short German-history lessons (shown in English, then German as you
            level up) and curated shows give you real context — so the language
            connects to a culture, not just a wordlist.
          </p>
          <Button asChild className="mt-5">
            <Link to="/register">Explore the history track</Link>
          </Button>
        </div>
        <div className="grid grid-cols-2 gap-3">
          {["Holy Roman Empire", "The Reformation", "Unification 1871", "Reunification 1990"].map(
            (t) => (
              <div
                key={t}
                className="flex items-center gap-2 rounded-xl border border-border bg-background p-4 text-sm font-medium"
              >
                <Landmark className="size-4 shrink-0 text-accent" />
                {t}
              </div>
            ),
          )}
        </div>
      </div>
    </Section>
  )
}

const STAT_ITEMS = [
  { n: "560+", l: "vocabulary words" },
  { n: "18", l: "grammar topics" },
  { n: "6", l: "drills & games" },
  { n: "6", l: "history lessons" },
]

function Stats() {
  return (
    <Section>
      <div className="grid grid-cols-2 gap-6 rounded-2xl border border-border bg-surface p-8 sm:grid-cols-4">
        {STAT_ITEMS.map((s) => (
          <div key={s.l} className="text-center">
            <div className="text-3xl font-bold text-accent">{s.n}</div>
            <div className="mt-1 text-sm text-muted-foreground">{s.l}</div>
          </div>
        ))}
      </div>
    </Section>
  )
}

const FAQS = [
  { q: "Is it free?", a: "Yes — you can use the core features for free. Some features (AI, speaking practice, drills) need a free account." },
  { q: "Do I need an account?", a: "You can try grammar, exercises, and a taste of the drills as a guest. Sign up to save progress and unlock everything." },
  { q: "What level is it for?", a: "A1 to C2. A short placement test (or a quick pick) sets your starting point, and content adapts as you grow." },
  { q: "Do I need to know any German?", a: "No — start from absolute zero at A1. Lessons and history are shown in English early on." },
]

function FaqAndCta() {
  return (
    <Section muted>
      <SectionHeading eyebrow="Questions" title="Good to know" />
      <div className="mx-auto max-w-2xl divide-y divide-border">
        {FAQS.map((f) => (
          <div key={f.q} className="py-4">
            <p className="font-medium">{f.q}</p>
            <p className="mt-1 text-sm text-muted-foreground">{f.a}</p>
          </div>
        ))}
      </div>

      <div className="mt-12 rounded-2xl border border-border bg-background p-10 text-center">
        <h2 className="text-2xl font-semibold tracking-tight sm:text-3xl">
          Ready to start learning German?
        </h2>
        <p className="mx-auto mt-2 max-w-md text-muted-foreground">
          Create a free account and find your level in two minutes.
        </p>
        <Button asChild size="lg" className="mt-6">
          <Link to="/register">Start free</Link>
        </Button>
      </div>

      <footer className="mt-12 flex flex-col items-center justify-between gap-3 border-t border-border pt-6 text-sm text-muted-foreground sm:flex-row">
        <span>© {new Date().getFullYear()} {SITE_NAME}</span>
        <div className="flex gap-4">
          <Link to="/privacy" className="hover:text-foreground">Privacy</Link>
          <Link to="/login" className="hover:text-foreground">Log in</Link>
          <Link to="/register" className="hover:text-foreground">Sign up</Link>
        </div>
      </footer>
    </Section>
  )
}

/* ---- small layout helpers ---- */
function Section({
  children,
  muted,
}: {
  children: React.ReactNode
  muted?: boolean
}) {
  return (
    <section className={cn("px-6 py-16 sm:py-20", muted && "bg-surface/40")}>
      <div className="mx-auto max-w-5xl">{children}</div>
    </section>
  )
}

function SectionHeading({
  eyebrow,
  title,
  subtitle,
}: {
  eyebrow: string
  title: string
  subtitle?: string
}) {
  return (
    <div className="mb-10 text-center">
      <p className="text-xs font-semibold uppercase tracking-wide text-accent">
        {eyebrow}
      </p>
      <h2 className="mt-2 text-2xl font-semibold tracking-tight sm:text-3xl">
        {title}
      </h2>
      {subtitle && (
        <p className="mx-auto mt-3 max-w-xl text-muted-foreground">{subtitle}</p>
      )}
    </div>
  )
}
