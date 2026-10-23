import { useEffect, useRef, useState, type ReactNode } from "react"
import { Link } from "react-router-dom"
import { useQuery } from "@tanstack/react-query"

import { fetchPublicStats } from "@/api/stats"
import { LEGAL_PAGES, SITE_NAME } from "@/lib/site"
import { MUNICH_PHOTO } from "@/lib/photos"
import { cn } from "@/lib/utils"
import { BookMarked, GraduationCap, Landmark, Route as RouteIcon, Sparkles, Swords, type LucideIcon } from "lucide-react"

import { Reveal } from "@/components/landing/Reveal"
import { Logo } from "@/components/layout/TopBar"

/*
 * The page guests see at `/` (signed-in users get the dashboard). It's a run of
 * run of sections, several over Berlin and Munich photos. Photo sections stay
 * dark with white text in both themes; the others follow light/dark. Photos are
 * free Unsplash images; if one fails to load, the section falls back to plain dark.
 */
const PHOTO_ISAR =
  "https://images.unsplash.com/photo-1770983437965-a88b456f2305?auto=format&fit=crop&w=2000&q=80"
const PHOTO_BERLIN =
  "https://images.unsplash.com/photo-1745878136928-d1b3c10afc35?auto=format&fit=crop&w=2000&q=80"
const PHOTO_MARIEN =
  "https://images.unsplash.com/photo-1780545311196-f8b507b08b94?auto=format&fit=crop&w=1400&q=80"

const PRIMARY_LINK =
  "inline-flex min-h-[52px] items-center justify-center rounded-full bg-primary px-8 text-base font-semibold text-primary-foreground transition hover:brightness-110 active:scale-[0.97]"

export default function LandingPage() {
  return (
    <div className="min-h-screen bg-background text-foreground">
      <Nav />
      <Hero />
      <Teaser />
      <Features />
      <Stats />
      <CultureMoment />
      <FaqCta />
    </div>
  )
}

/* Transparent over the hero, solid once you scroll. */
function Nav() {
  const [solid, setSolid] = useState(false)
  useEffect(() => {
    const onScroll = () => setSolid(window.scrollY > 40)
    window.addEventListener("scroll", onScroll, { passive: true })
    return () => window.removeEventListener("scroll", onScroll)
  }, [])
  return (
    <header
      className={cn(
        "fixed inset-x-0 top-0 z-30 flex h-16 items-center justify-between px-5 transition-colors duration-300 sm:px-8",
        solid ? "glass text-foreground" : "bg-transparent text-white",
      )}
    >
      <Logo className="text-inherit" />
      <div className="flex items-center gap-1 text-[15px] font-semibold">
        <Link
          to="/login"
          className={cn("hidden rounded-full px-4 py-2 transition-opacity sm:inline-block", solid ? "opacity-70 hover:opacity-100" : "text-white/85 hover:text-white")}
        >
          Log in
        </Link>
        <Link
          to="/login"
          className="rounded-full bg-primary px-5 py-2 text-primary-foreground transition hover:brightness-110"
        >
          Get started
        </Link>
      </div>
    </header>
  )
}

function Hero() {
  const imgRef = useRef<HTMLImageElement>(null)
  const [ok, setOk] = useState(true)
  useEffect(() => {
    const onScroll = () => {
      if (imgRef.current) imgRef.current.style.transform = `translateY(${window.scrollY * 0.35}px)`
    }
    window.addEventListener("scroll", onScroll, { passive: true })
    return () => window.removeEventListener("scroll", onScroll)
  }, [])
  return (
    <section className="relative flex h-[100svh] min-h-[620px] items-center justify-center overflow-hidden bg-[#111] text-white">
      {ok && (
        <img
          ref={imgRef}
          src={MUNICH_PHOTO}
          alt="Munich's old town at sunset"
          onError={() => setOk(false)}
          className="absolute inset-0 h-[135%] w-full object-cover"
        />
      )}
      <div className="absolute inset-0 bg-gradient-to-b from-black/55 via-black/35 to-black/75" />
      <div className="absolute inset-x-0 bottom-0 h-32 bg-gradient-to-t from-background to-transparent" />
      <div className="relative z-10 mx-auto max-w-4xl px-6 text-center">
        <Reveal>
          <p className="mb-5 text-[13px] font-semibold uppercase tracking-[0.2em] text-white/75">
            Deutsch lernen · A1–B1
          </p>
          <h1 className="text-[44px] font-extrabold leading-[1.02] tracking-[-0.035em] sm:text-7xl lg:text-[84px]">
            Learn German,
            <br />
            one short lesson a day.
          </h1>
          <p className="mx-auto mt-6 max-w-xl text-lg text-white/85 sm:text-xl">
            A guided A1–B1 German course: flashcards that come back just before you
            forget them, quick drills, Goethe-style exam practice for Lesen, Schreiben,
            Hören and Sprechen, and short reads on German history.
          </p>
          <div className="mt-9 flex flex-col items-center justify-center gap-3 sm:flex-row">
            <Link to="/login" className={cn(PRIMARY_LINK, "w-full sm:w-auto")}>
              Start free
            </Link>
            <Link
              to="/login"
              className="inline-flex min-h-[52px] w-full items-center justify-center rounded-full bg-white/15 px-8 text-base font-semibold text-white backdrop-blur-md transition-colors hover:bg-white/25 sm:w-auto"
            >
              I already know some German
            </Link>
          </div>
        </Reveal>
      </div>
    </section>
  )
}

/* A three-noun der/die/das quiz guests can play right on the page. */
const TEASER = [
  { noun: "Hund", en: "dog", article: "der" },
  { noun: "Katze", en: "cat", article: "die" },
  { noun: "Haus", en: "house", article: "das" },
] as const

const ARTICLE_TEXT: Record<string, string> = {
  der: "text-article-der",
  die: "text-article-die",
  das: "text-article-das",
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
    <Section bg={<PhotoBg src={PHOTO_MARIEN} />} dark>
      <Reveal>
        <SectionHeader label="Try it" title="der, die or das?" />
        <div className="mx-auto mt-10 max-w-md rounded-[28px] bg-surface p-8 text-center text-foreground shadow-lift">
          {done ? (
            <>
              <p className="text-lg font-semibold">
                You got {score} of {TEASER.length}.
              </p>
              <p className="mt-1 text-sm text-muted-foreground">
                Noun genders are hard. The drills give you plenty of practice with them.
              </p>
              <Link to="/login" className={cn(PRIMARY_LINK, "mt-6")}>
                Create a free account
              </Link>
            </>
          ) : (
            <>
              <p className="text-sm text-muted-foreground">Which article? ({current.en})</p>
              <p className="mt-2 font-grotesk text-5xl font-extrabold tracking-tight">{current.noun}</p>
              <div className="mt-7 grid grid-cols-3 gap-3">
                {(["der", "die", "das"] as const).map((a) => {
                  const isCorrect = picked && a === current.article
                  const isWrong = picked === a && a !== current.article
                  return (
                    <button
                      key={a}
                      onClick={() => choose(a)}
                      disabled={!!picked}
                      className={cn(
                        "min-h-[60px] rounded-2xl border-2 text-lg font-bold transition-colors",
                        isCorrect
                          ? "border-success bg-success/15 text-success"
                          : isWrong
                            ? "border-danger bg-danger/15 text-danger"
                            : "border-transparent bg-surface-2 hover:bg-border",
                        !picked && ARTICLE_TEXT[a],
                      )}
                    >
                      {a}
                    </button>
                  )
                })}
              </div>
            </>
          )}
        </div>
      </Reveal>
    </Section>
  )
}

const FEATURES: { title: string; body: string; icon: LucideIcon }[] = [
  {
    icon: RouteIcon,
    title: "The path",
    body: "A1, A2 and B1, split into units of two or three lessons: new words, grammar, then conversation and review.",
  },
  {
    icon: GraduationCap,
    title: "Spaced review",
    body: "Flashcards scheduled with SM-2, so each word returns just before you'd forget it.",
  },
  {
    icon: BookMarked,
    title: "Word Bank",
    body: "Every word you've reached, grouped by level and part of speech.",
  },
  { icon: Swords, title: "Drills", body: "Quick games for articles, spelling and word order." },
  {
    icon: Landmark,
    title: "History",
    body: "Short reads on German history, first in English and then in German.",
  },
  {
    icon: Sparkles,
    title: "AI tutor and Talk to AI",
    body: "Premium: ask a tutor anything, or have a spoken conversation in German and get a report on it.",
  },
]

function Features() {
  return (
    <Section>
      <Reveal>
        <SectionHeader label="What's in it" title="How the app works" />
      </Reveal>
      <div className="mt-12 grid gap-4 sm:grid-cols-2 lg:grid-cols-3">
        {FEATURES.map((f, i) => (
          <Reveal key={f.title} delay={i * 60}>
            <div className="lift h-full rounded-[24px] bg-surface p-6 shadow-card">
              <span
                className="flex size-11 items-center justify-center rounded-2xl text-white"
                style={{ background: `hsl(var(--section-${(i % 6) + 1}))` }}
              >
                <f.icon className="size-[22px]" aria-hidden="true" />
              </span>
              <h3 className="mt-4 text-lg font-bold">{f.title}</h3>
              <p className="mt-1 text-muted-foreground">{f.body}</p>
            </div>
          </Reveal>
        ))}
      </div>
    </Section>
  )
}

/* Live counts from the API. Hidden if the API is unreachable, rather than
   showing a row of zeros. */
function Stats() {
  const { data } = useQuery({ queryKey: ["public-stats"], queryFn: fetchPublicStats })
  if (!data) return null

  const items = [
    { value: data.words, label: "words" },
    { value: data.grammar_topics, label: "grammar topics" },
    { value: data.exercises, label: "exercises" },
    { value: data.history_reads, label: "history reads" },
  ].filter((s) => s.value > 0)

  if (items.length === 0) return null

  return (
    <Section>
      <Reveal>
        <SectionHeader label="Right now" title="What's in the app" />
        <p className="mx-auto mt-3 max-w-md text-center text-muted-foreground">
          These are counted live from the database.
        </p>
        <div className="mt-10 grid grid-cols-2 gap-6 sm:grid-cols-4">
          {items.map((s) => (
            <div key={s.label} className="text-center">
              <p className="font-grotesk text-5xl font-extrabold tracking-tight text-primary sm:text-6xl">
                {s.value.toLocaleString()}
              </p>
              <p className="mt-1 text-muted-foreground">{s.label}</p>
            </div>
          ))}
        </div>
      </Reveal>
    </Section>
  )
}

const SIGHTS = [
  { src: PHOTO_BERLIN, name: "Brandenburger Tor", city: "Berlin" },
  { src: PHOTO_ISAR, name: "Die Isar", city: "München" },
  { src: PHOTO_MARIEN, name: "Marienplatz", city: "München" },
]

/* Rotating city photos; clicking a name jumps to it. */
function CultureMoment() {
  const [active, setActive] = useState(0)

  // No automatic rotation for people who prefer reduced motion.
  useEffect(() => {
    if (window.matchMedia("(prefers-reduced-motion: reduce)").matches) return
    const id = window.setInterval(() => setActive((n) => (n + 1) % SIGHTS.length), 5000)
    return () => window.clearInterval(id)
  }, [])

  const current = SIGHTS[active]

  return (
    <section className="relative flex min-h-screen items-center overflow-hidden bg-[#111] text-white">
      {SIGHTS.map((s, i) => (
        <img
          key={s.name}
          src={s.src}
          alt={`${s.name}, ${s.city}`}
          className={cn(
            "absolute inset-0 size-full object-cover transition-opacity duration-1000 motion-reduce:transition-none",
            i === active ? "opacity-100" : "opacity-0",
          )}
        />
      ))}
      {/* Darken the left for the text, and fade top and bottom into the page. */}
      <div className="absolute inset-0 bg-gradient-to-r from-black/80 via-black/45 to-black/10" />
      <div className="absolute inset-x-0 top-0 h-40 bg-gradient-to-b from-background to-transparent" />
      <div className="absolute inset-x-0 bottom-0 h-40 bg-gradient-to-t from-background to-transparent" />

      <div className="relative z-10 mx-auto w-full max-w-5xl px-6">
        <Reveal className="max-w-xl">
          <SectionLabel>Mehr als Vokabeln</SectionLabel>
          <h2 className="mt-3 text-4xl font-extrabold leading-tight sm:text-6xl">
            Learn the language and the country
          </h2>
          <p className="mt-4 text-lg text-white/85">
            The history track covers the places and events behind the words you're
            learning.
          </p>
          <div className="mt-8 flex flex-wrap gap-2">
            {SIGHTS.map((s, i) => (
              <button
                key={s.name}
                onClick={() => setActive(i)}
                className={cn(
                  "min-h-[44px] rounded-full px-4 text-sm font-semibold transition-colors",
                  i === active
                    ? "bg-primary text-primary-foreground"
                    : "bg-white/15 text-white backdrop-blur-md hover:bg-white/25",
                )}
              >
                {s.name}
              </button>
            ))}
          </div>
          <p className="mt-3 text-sm text-white/75">{current.city}</p>
        </Reveal>
      </div>
    </section>
  )
}

const FAQS = [
  {
    q: "Is it free?",
    a: "Yes. The whole A1–B1 path (limited by energy), review, Word Bank, grammar, drills, videos and history are free. Premium adds unlimited energy, Lesen, Hören and Schreiben practice, the AI tutor and Talk to AI.",
  },
  {
    q: "Do I need an account?",
    a: "You can try the grammar pages and one drill as a guest. Sign in with Google or GitHub to save progress and follow the path.",
  },
  {
    q: "What level is it for?",
    a: "Beginners up to intermediate: the course covers A1, A2 and B1 in full and stops at B1. B2 and higher aren't on the site yet. If you already know some German, the placement test picks your starting level.",
  },
]

function FaqCta() {
  return (
    <Section>
      <Reveal>
        <SectionHeader label="Questions" title="Good to know" />
      </Reveal>
      <div className="mx-auto mt-10 max-w-2xl divide-y divide-border rounded-[24px] bg-surface px-6 shadow-card">
        {FAQS.map((f) => (
          <Reveal key={f.q}>
            <div className="py-5">
              <p className="text-lg font-semibold">{f.q}</p>
              <p className="mt-1 text-muted-foreground">{f.a}</p>
            </div>
          </Reveal>
        ))}
      </div>

      <Reveal>
        <div className="mx-auto mt-14 max-w-2xl rounded-[28px] bg-surface p-10 text-center shadow-card">
          <h2 className="text-3xl font-extrabold sm:text-5xl">Ready to start?</h2>
          <p className="mx-auto mt-3 max-w-md text-muted-foreground">
            Sign in with Google or GitHub. It takes about a minute.
          </p>
          <Link to="/login" className={cn(PRIMARY_LINK, "mt-7")}>
            Start free
          </Link>
        </div>
      </Reveal>

      <footer className="mx-auto mt-14 flex w-full max-w-2xl flex-col items-center justify-between gap-3 border-t border-border pt-6 text-sm text-muted-foreground sm:flex-row">
        <span>
          © {new Date().getFullYear()} {SITE_NAME}
        </span>
        <div className="flex flex-wrap justify-center gap-x-4 gap-y-2">
          {LEGAL_PAGES.map((p) => (
            <Link key={p.to} to={p.to} className="hover:text-foreground">
              {p.label}
            </Link>
          ))}
          <Link to="/login" className="hover:text-foreground">
            Log in
          </Link>
        </div>
      </footer>
    </Section>
  )
}

/** A full-height section, optionally over a background (e.g. a photo). */
function Section({ children, bg, dark }: { children: ReactNode; bg?: ReactNode; dark?: boolean }) {
  return (
    <section
      className={cn(
        "relative flex flex-col justify-center overflow-hidden px-5 py-24 sm:px-8 sm:py-32",
        dark && "min-h-screen bg-[#111] text-white",
      )}
    >
      {bg}
      <div className="relative z-10 mx-auto w-full max-w-5xl">{children}</div>
    </section>
  )
}

/** A photo darkened for legibility, fading into the page at top and bottom. */
function PhotoBg({ src }: { src: string }) {
  const [ok, setOk] = useState(true)
  return (
    <>
      {ok && (
        <img
          src={src}
          alt=""
          onError={() => setOk(false)}
          className="absolute inset-0 size-full object-cover"
        />
      )}
      <div className="absolute inset-0 bg-black/55" />
      <div className="absolute inset-x-0 top-0 h-40 bg-gradient-to-b from-background to-transparent" />
      <div className="absolute inset-x-0 bottom-0 h-40 bg-gradient-to-t from-background to-transparent" />
    </>
  )
}

function SectionHeader({ label, title }: { label: string; title: string }) {
  return (
    <div className="mx-auto max-w-2xl text-center">
      <SectionLabel>{label}</SectionLabel>
      <h2 className="mt-3 text-4xl font-extrabold sm:text-5xl">{title}</h2>
    </div>
  )
}

function SectionLabel({ children }: { children: ReactNode }) {
  return (
    <p className="text-[13px] font-semibold uppercase tracking-[0.2em] opacity-70">{children}</p>
  )
}
