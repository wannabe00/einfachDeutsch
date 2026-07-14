import { useEffect, useRef, useState, type ReactNode } from "react"
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
import { cn } from "@/lib/utils"
import { Reveal } from "@/components/landing/Reveal"

/*
 * Cinematic landing (Design v2). Always-dark marketing page built as a sequence
 * of full-viewport "moments" — you focus on one at a time. Sections blend into
 * each other (photo backdrops fade to the page canvas top & bottom, so there's
 * no hard seam), and each has depth (a full-bleed Berlin/Munich photo or a soft
 * brand glow), never a plain block on flat black. Big Space Grotesk type, one
 * swappable brand accent (`--brand`, German-flag red now), pill CTAs,
 * scroll-reveal. This is the guest `/`; signed-in users get the dashboard.
 * Verified free Unsplash URLs; a gradient shows if an image fails.
 */
const HERO_IMG =
  "https://images.unsplash.com/photo-1595867818082-083862f3d630?auto=format&fit=crop&w=2400&q=80"
const PHOTO_ISAR =
  "https://images.unsplash.com/photo-1770983437965-a88b456f2305?auto=format&fit=crop&w=2000&q=80"
const PHOTO_BERLIN =
  "https://images.unsplash.com/photo-1745878136928-d1b3c10afc35?auto=format&fit=crop&w=2000&q=80"
const PHOTO_MARIEN =
  "https://images.unsplash.com/photo-1780545311196-f8b507b08b94?auto=format&fit=crop&w=1400&q=80"

const brand = "hsl(var(--brand))"

export default function LandingPage() {
  return (
    <div className="min-h-screen bg-[#0a0a0b] font-grotesk text-white">
      <Nav />
      <Hero />
      <Teaser />
      <Features />
      <CultureMoment />
      <FaqCta />
    </div>
  )
}

/* ---- Nav: transparent over the hero, solid after scroll ---- */
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
        "fixed inset-x-0 top-0 z-30 flex items-center justify-between px-6 py-4 transition-colors duration-300",
        solid ? "border-b border-white/10 bg-[#0a0a0b]/90 backdrop-blur" : "bg-transparent",
      )}
    >
      <span className="flex items-center gap-2 text-lg font-bold tracking-tight">
        <span className="inline-flex gap-1" aria-hidden="true">
          <span className="size-2.5 rounded-full" style={{ background: "hsl(var(--article-der))" }} />
          <span className="size-2.5" style={{ background: "hsl(var(--article-die))", clipPath: "polygon(50% 0, 100% 100%, 0 100%)" }} />
          <span className="size-2.5" style={{ background: "hsl(var(--article-das))" }} />
        </span>
        {SITE_NAME === "German Learning Platform" ? "einfachDeutsch" : SITE_NAME}
      </span>
      <div className="flex items-center gap-2 text-sm font-semibold">
        <Link to="/login" className="rounded-full px-4 py-2 text-white/80 transition-colors hover:text-white">
          Log in
        </Link>
        <Link
          to="/login"
          className="rounded-full px-5 py-2 text-white transition-transform hover:scale-105"
          style={{ background: brand }}
        >
          Get started
        </Link>
      </div>
    </header>
  )
}

/* ---- Hero: full-bleed photo + parallax + big headline ---- */
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
    <section className="relative flex h-screen min-h-[620px] items-center justify-center overflow-hidden">
      <div className="absolute inset-0 bg-gradient-to-br from-[#12131a] to-[#0a0a0b]" />
      {ok && (
        <img
          ref={imgRef}
          src={HERO_IMG}
          alt="München"
          onError={() => setOk(false)}
          className="absolute inset-0 h-[135%] w-full object-cover"
        />
      )}
      <div className="absolute inset-0 bg-gradient-to-t from-[#0a0a0b] via-[#0a0a0b]/40 to-[#0a0a0b]/70" />
      <div className="relative z-10 mx-auto max-w-4xl px-6 text-center">
        <Reveal>
          <p className="mb-4 text-xs font-semibold uppercase tracking-[0.25em] text-white/60">
            Deutsch lernen · A1 → C1
          </p>
          <h1 className="text-5xl font-bold leading-[1.05] tracking-tight sm:text-7xl">
            Learn German
            <br />
            that <span style={{ color: brand }}>actually sticks.</span>
          </h1>
          <p className="mx-auto mt-6 max-w-xl text-lg text-white/75">
            Spaced-repetition flashcards, drills, an AI tutor, and speaking
            practice — paced to your level, from Berlin to München.
          </p>
          <div className="mt-9 flex flex-col items-center justify-center gap-3 sm:flex-row">
            <Link
              to="/login"
              className="w-full rounded-full px-8 py-3.5 text-base font-semibold text-white transition-transform hover:scale-105 sm:w-auto"
              style={{ background: brand }}
            >
              Start free
            </Link>
            <Link
              to="/login"
              className="w-full rounded-full border border-white/30 bg-white/5 px-8 py-3.5 text-base font-semibold text-white backdrop-blur transition-colors hover:bg-white/10 sm:w-auto"
            >
              Take the level test
            </Link>
          </div>
        </Reveal>
      </div>
      <ChevronDown className="absolute bottom-6 left-1/2 z-10 size-7 -translate-x-1/2 animate-bounce text-white/60" />
    </section>
  )
}

/* ---- der/die/das interactive tester (kept — owner likes it) ---- */
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
    <Moment bg={<PhotoBg src={PHOTO_MARIEN} />}>
      <Reveal>
        <MomentHeader label="Try it now" title="der, die, or das?" />
        <div className="mx-auto mt-10 max-w-md rounded-2xl border border-white/10 bg-[#0a0a0b]/55 p-8 text-center backdrop-blur-md">
          {done ? (
            <>
              <p className="text-lg font-semibold">
                You got {score}/{TEASER.length}.
              </p>
              <p className="mt-1 text-sm text-white/70">
                Gender is hard — that's exactly what the drills train.
              </p>
              <Link
                to="/login"
                className="mt-6 inline-block rounded-full px-6 py-2.5 text-sm font-semibold text-white"
                style={{ background: brand }}
              >
                Create a free account
              </Link>
            </>
          ) : (
            <>
              <p className="text-sm text-white/70">Which article? ({current.en})</p>
              <p className="mt-2 text-4xl font-bold">{current.noun}</p>
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
                        "rounded-xl border-2 py-4 text-lg font-bold transition-colors",
                        isCorrect
                          ? "border-[hsl(var(--success))] bg-[hsl(var(--success)/0.15)] text-[hsl(var(--success))]"
                          : isWrong
                            ? "border-[hsl(var(--danger))] bg-[hsl(var(--danger)/0.15)] text-[hsl(var(--danger))]"
                            : "border-white/15 hover:border-white/40",
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
      </Reveal>
    </Moment>
  )
}

/* ---- Feature strip ---- */
const FEATURES = [
  { icon: GraduationCap, title: "Spaced review", body: "SM-2 flashcards timed to just before you'd forget." },
  { icon: BookMarked, title: "Word Bank", body: "Vocabulary by chapter; import your own lists." },
  { icon: Swords, title: "Drills", body: "Fast games: gender, unscramble, recall." },
  { icon: Mic, title: "Recite", body: "Retell a text aloud, scored on coverage & grammar." },
  { icon: BrainCircuit, title: "AI tutor", body: "Explanations, exercises, instant feedback." },
  { icon: Landmark, title: "History", body: "German history — English first, then German." },
]

function Features() {
  return (
    <Moment>
      <Reveal>
        <MomentHeader label="What's inside" title="Everything in one place" />
      </Reveal>
      <div className="mt-12 grid gap-4 sm:grid-cols-2 lg:grid-cols-3">
        {FEATURES.map((f, i) => (
          <Reveal key={f.title} delay={i * 60}>
            <div className="h-full rounded-xl border border-white/10 bg-white/[0.03] p-6 transition-colors hover:border-white/25">
              <div
                className="flex size-10 items-center justify-center rounded-lg"
                style={{ background: "hsl(var(--brand)/0.15)", color: brand }}
              >
                <f.icon className="size-5" />
              </div>
              <h3 className="mt-4 font-bold">{f.title}</h3>
              <p className="mt-1 text-sm text-white/60">{f.body}</p>
            </div>
          </Reveal>
        ))}
      </div>
    </Moment>
  )
}

/* ---- Culture moment: interactive sightseeing backdrop ---- */
const SIGHTS = [
  { src: PHOTO_BERLIN, name: "Brandenburger Tor", city: "Berlin" },
  { src: PHOTO_ISAR, name: "Die Isar", city: "München" },
  { src: PHOTO_MARIEN, name: "Marienplatz", city: "München" },
]

function CultureMoment() {
  const [active, setActive] = useState(0)

  // Auto-rotate the backdrop; clicking a sight jumps to it. Reduced-motion
  // users stay on whatever they pick (no automatic movement).
  useEffect(() => {
    if (window.matchMedia("(prefers-reduced-motion: reduce)").matches) return
    const id = window.setInterval(() => setActive((n) => (n + 1) % SIGHTS.length), 5000)
    return () => window.clearInterval(id)
  }, [])

  const current = SIGHTS[active]

  return (
    <section className="relative flex min-h-screen items-center overflow-hidden">
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
      {/* Readability wash on the left + top/bottom fades so the section blends
          seamlessly into the ones above and below. */}
      <div className="absolute inset-0 bg-gradient-to-r from-[#0a0a0b] via-[#0a0a0b]/55 to-[#0a0a0b]/10" />
      <div className="absolute inset-x-0 top-0 h-40 bg-gradient-to-b from-[#0a0a0b] to-transparent" />
      <div className="absolute inset-x-0 bottom-0 h-40 bg-gradient-to-t from-[#0a0a0b] to-transparent" />

      <div className="relative z-10 mx-auto w-full max-w-5xl px-6">
        <Reveal className="max-w-xl">
          <SectionLabel>Mehr als Vokabeln</SectionLabel>
          <h2 className="mt-3 text-4xl font-bold leading-tight tracking-tight sm:text-5xl">
            Learn the language and the country
          </h2>
          <p className="mt-4 text-lg text-white/75">
            From the Brandenburger Tor to the Isar — culture and context, not just
            a wordlist.
          </p>
          <div className="mt-8 flex flex-wrap gap-2">
            {SIGHTS.map((s, i) => (
              <button
                key={s.name}
                onClick={() => setActive(i)}
                className={cn(
                  "rounded-full border px-4 py-2 text-sm font-semibold transition-colors",
                  i === active
                    ? "border-transparent text-white"
                    : "border-white/25 text-white/70 hover:text-white",
                )}
                style={i === active ? { background: brand } : undefined}
              >
                {s.name}
              </button>
            ))}
          </div>
          <p className="mt-3 text-sm text-white/50">{current.city}</p>
        </Reveal>
      </div>
    </section>
  )
}

/* ---- FAQ + final CTA + footer ---- */
const FAQS = [
  { q: "Is it free?", a: "Yes — the core features are free. Some (AI, speaking, drills) need a free account." },
  { q: "Do I need an account?", a: "Try grammar, exercises, and a taste of the drills as a guest. Sign in to save progress." },
  { q: "What level is it for?", a: "A1 to C1 — start at A1 or take a placement test, and content adapts as you grow." },
]

function FaqCta() {
  return (
    <Moment>
      <Reveal>
        <MomentHeader label="Questions" title="Good to know" />
      </Reveal>
      <div className="mx-auto mt-10 max-w-2xl divide-y divide-white/10">
        {FAQS.map((f) => (
          <Reveal key={f.q}>
            <div className="py-5">
              <p className="font-semibold">{f.q}</p>
              <p className="mt-1 text-sm text-white/60">{f.a}</p>
            </div>
          </Reveal>
        ))}
      </div>

      <Reveal>
        <div className="mx-auto mt-14 max-w-2xl rounded-2xl border border-white/10 bg-white/[0.03] p-10 text-center">
          <h2 className="text-3xl font-bold tracking-tight sm:text-4xl">
            Ready to start learning German?
          </h2>
          <p className="mx-auto mt-3 max-w-md text-white/70">
            Sign in with Google or GitHub and find your level in minutes.
          </p>
          <Link
            to="/login"
            className="mt-7 inline-block rounded-full px-8 py-3.5 text-base font-semibold text-white transition-transform hover:scale-105"
            style={{ background: brand }}
          >
            Start free
          </Link>
        </div>
      </Reveal>

      <footer className="mx-auto mt-14 flex w-full max-w-2xl flex-col items-center justify-between gap-3 border-t border-white/10 pt-6 text-sm text-white/50 sm:flex-row">
        <span>© {new Date().getFullYear()} einfachDeutsch</span>
        <div className="flex gap-4">
          <Link to="/privacy" className="hover:text-white">Privacy</Link>
          <Link to="/login" className="hover:text-white">Log in</Link>
        </div>
      </footer>
    </Moment>
  )
}

/* ---- building blocks ---- */

/** A full-viewport section so the reader focuses on one thing at a time.
    Defaults to a soft brand glow backdrop; pass `bg` for a photo backdrop. */
function Moment({
  children,
  className,
  bg,
}: {
  children: ReactNode
  className?: string
  bg?: ReactNode
}) {
  return (
    <section
      className={cn(
        "relative flex min-h-screen flex-col justify-center overflow-hidden px-6 py-24",
        className,
      )}
    >
      {bg ?? <GlowBg />}
      <div className="relative z-10 mx-auto w-full max-w-5xl">{children}</div>
    </section>
  )
}

/** Near-black canvas with a single soft brand-colored glow for depth. */
function GlowBg() {
  return (
    <>
      <div className="absolute inset-0 bg-[#0a0a0b]" />
      <div
        className="absolute left-1/2 top-1/2 size-[640px] -translate-x-1/2 -translate-y-1/2 rounded-full opacity-[0.14] blur-[130px]"
        style={{ background: brand }}
      />
    </>
  )
}

/** Full-bleed photo kept bright enough to hold the mood, with top/bottom fades
    to the page canvas so the section melts into its neighbours (no hard seam). */
function PhotoBg({ src }: { src: string }) {
  const [ok, setOk] = useState(true)
  return (
    <>
      <div className="absolute inset-0 bg-[#0a0a0b]" />
      {ok && (
        <img
          src={src}
          alt=""
          onError={() => setOk(false)}
          className="absolute inset-0 size-full object-cover opacity-[0.6]"
        />
      )}
      <div className="absolute inset-0 bg-[#0a0a0b]/45" />
      <div className="absolute inset-x-0 top-0 h-40 bg-gradient-to-b from-[#0a0a0b] to-transparent" />
      <div className="absolute inset-x-0 bottom-0 h-40 bg-gradient-to-t from-[#0a0a0b] to-transparent" />
    </>
  )
}

function MomentHeader({ label, title }: { label: string; title: string }) {
  return (
    <div className="mx-auto max-w-2xl text-center">
      <SectionLabel>{label}</SectionLabel>
      <h2 className="mt-3 text-3xl font-bold tracking-tight sm:text-4xl">{title}</h2>
    </div>
  )
}

function SectionLabel({ children }: { children: ReactNode }) {
  return (
    <p className="text-xs font-semibold uppercase tracking-[0.2em] text-white/50">{children}</p>
  )
}
