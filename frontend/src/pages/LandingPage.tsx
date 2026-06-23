import { useEffect, useRef, useState } from "react"
import { Link } from "react-router-dom"
import {
  BookMarked,
  BrainCircuit,
  ChevronDown,
  GraduationCap,
  Landmark,
  Mic,
  Swords,
} from "lucide-react"

import { SITE_NAME } from "@/lib/site"
import { Button } from "@/components/ui/button"
import { cn } from "@/lib/utils"

// Swap these for your own photos anytime; a gradient shows if an image fails.
const HERO_IMG =
  "https://images.unsplash.com/photo-1595867818082-083862f3d630?auto=format&fit=crop&w=2400&q=80"

const CITY_PHOTOS = [
  {
    src: "https://images.unsplash.com/photo-1770983437965-a88b456f2305?auto=format&fit=crop&w=1100&q=80",
    caption: "Die Isar",
    city: "München",
  },
  {
    src: "https://images.unsplash.com/photo-1745878136928-d1b3c10afc35?auto=format&fit=crop&w=1100&q=80",
    caption: "Brandenburger Tor",
    city: "Berlin",
  },
  {
    src: "https://images.unsplash.com/photo-1780545311196-f8b507b08b94?auto=format&fit=crop&w=1100&q=80",
    caption: "Marienplatz bei Nacht",
    city: "München",
  },
]

export default function LandingPage() {
  const imgRef = useRef<HTMLImageElement>(null)
  const [imgOk, setImgOk] = useState(true)

  // Parallax: drift the hero photo slower than the page (no re-render).
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
      <Teaser />
      <Features />
      <CultureBand />
      <CefrPath />
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
          <Link to="/login">Get started</Link>
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
      <div className="absolute inset-0 bg-gradient-to-br from-[#1b2a4a] via-[#24304d] to-[#3a2a4d]" />
      {imgOk && (
        <img
          ref={imgRef}
          src={HERO_IMG}
          alt="München — Marienplatz"
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
          Spaced-repetition flashcards, drills, an AI tutor, speaking practice,
          and German culture — paced to your level, from Berlin to München.
        </p>
        <div className="mt-8 flex flex-col items-center justify-center gap-3 sm:flex-row">
          <Button asChild size="lg" className="w-full sm:w-auto">
            <Link to="/login">Start free</Link>
          </Button>
          <Button
            asChild
            size="lg"
            variant="outline"
            className="w-full border-white/40 bg-white/10 text-white hover:bg-white/20 sm:w-auto"
          >
            <Link to="/login">Take the level test</Link>
          </Button>
        </div>
      </div>

      <ChevronDown className="absolute bottom-6 left-1/2 z-10 size-7 -translate-x-1/2 animate-bounce text-white/80" />
    </section>
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
      <SectionHeading eyebrow="Try it now" title="der, die, or das?" />
      <div className="mx-auto max-w-md rounded-2xl border border-border bg-surface p-8 text-center">
        {done ? (
          <>
            <p className="text-lg font-semibold">
              You got {score}/{TEASER.length}.
            </p>
            <p className="mt-1 text-sm text-muted-foreground">
              Gender is hard — that's exactly what the drills train.
            </p>
            <Button asChild className="mt-5">
              <Link to="/login">Create a free account</Link>
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
                    style={!picked ? { color: `hsl(var(${ARTICLE_VAR[a]}))` } : undefined}
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
  { icon: GraduationCap, title: "Spaced review", body: "SM-2 flashcards timed to just before you'd forget." },
  { icon: BookMarked, title: "Word Bank", body: "Vocabulary by chapter; import your own lists." },
  { icon: Swords, title: "Drills", body: "Fast games: gender, unscramble, recall." },
  { icon: Mic, title: "Recite", body: "Retell a text aloud, scored on coverage & grammar." },
  { icon: BrainCircuit, title: "AI tutor", body: "Explanations, exercises, and instant feedback." },
  { icon: Landmark, title: "History", body: "German history — English first, then German." },
]

function Features() {
  return (
    <Section muted>
      <SectionHeading eyebrow="What's inside" title="Everything in one place" />
      <div className="grid gap-4 sm:grid-cols-2 lg:grid-cols-3">
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

function CultureBand() {
  return (
    <Section>
      <SectionHeading
        eyebrow="More than vocabulary"
        title="Learn the language and the country"
        subtitle="From Marienplatz to the Brandenburg Gate — culture and context, not just a wordlist."
      />
      <div className="grid gap-4 sm:grid-cols-3">
        {CITY_PHOTOS.map((p) => (
          <PhotoTile key={p.caption} {...p} />
        ))}
      </div>
    </Section>
  )
}

function PhotoTile({ src, caption, city }: { src: string; caption: string; city: string }) {
  const [ok, setOk] = useState(true)
  return (
    <div className="relative aspect-[4/3] overflow-hidden rounded-xl border border-border">
      <div className="absolute inset-0 bg-gradient-to-br from-[#24304d] to-[#3a2a4d]" />
      {ok && (
        <img
          src={src}
          alt={`${caption}, ${city}`}
          loading="lazy"
          onError={() => setOk(false)}
          className="absolute inset-0 size-full object-cover transition-transform duration-500 hover:scale-105"
        />
      )}
      <div className="absolute inset-x-0 bottom-0 bg-gradient-to-t from-black/70 to-transparent p-3 text-white">
        <p className="text-sm font-semibold">{caption}</p>
        <p className="text-xs text-white/75">{city}</p>
      </div>
    </div>
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
    <Section muted>
      <SectionHeading eyebrow="Your path" title="A1 to C2" />
      <div className="flex flex-wrap items-stretch justify-center gap-3">
        {LEVELS.map((lvl) => (
          <div
            key={lvl.l}
            className="flex w-[140px] flex-col rounded-xl border border-border bg-background p-4"
          >
            <span className="text-2xl font-bold text-accent">{lvl.l}</span>
            <span className="mt-1 text-xs text-muted-foreground">{lvl.t}</span>
          </div>
        ))}
      </div>
    </Section>
  )
}

const FAQS = [
  { q: "Is it free?", a: "Yes — the core features are free. Some (AI, speaking, drills) need a free account." },
  { q: "Do I need an account?", a: "Try grammar, exercises, and a taste of the drills as a guest. Sign in to save progress and unlock everything." },
  { q: "What level is it for?", a: "A1 to C2 — start at A1 or take a placement test, and content adapts as you grow." },
]

function FaqAndCta() {
  return (
    <Section>
      <SectionHeading eyebrow="Questions" title="Good to know" />
      <div className="mx-auto max-w-2xl divide-y divide-border">
        {FAQS.map((f) => (
          <div key={f.q} className="py-4">
            <p className="font-medium">{f.q}</p>
            <p className="mt-1 text-sm text-muted-foreground">{f.a}</p>
          </div>
        ))}
      </div>

      <div className="mt-12 rounded-2xl border border-border bg-surface p-10 text-center">
        <h2 className="text-2xl font-semibold tracking-tight sm:text-3xl">
          Ready to start learning German?
        </h2>
        <p className="mx-auto mt-2 max-w-md text-muted-foreground">
          Sign in with Google or GitHub and find your level in minutes.
        </p>
        <Button asChild size="lg" className="mt-6">
          <Link to="/login">Start free</Link>
        </Button>
      </div>

      <footer className="mt-12 flex flex-col items-center justify-between gap-3 border-t border-border pt-6 text-sm text-muted-foreground sm:flex-row">
        <span>
          © {new Date().getFullYear()} {SITE_NAME}
        </span>
        <div className="flex gap-4">
          <Link to="/privacy" className="hover:text-foreground">Privacy</Link>
          <Link to="/login" className="hover:text-foreground">Log in</Link>
        </div>
      </footer>
    </Section>
  )
}

/* ---- small layout helpers ---- */
function Section({ children, muted }: { children: React.ReactNode; muted?: boolean }) {
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
      <p className="text-xs font-semibold uppercase tracking-wide text-accent">{eyebrow}</p>
      <h2 className="mt-2 text-2xl font-semibold tracking-tight sm:text-3xl">{title}</h2>
      {subtitle && <p className="mx-auto mt-3 max-w-xl text-muted-foreground">{subtitle}</p>}
    </div>
  )
}
