import { useEffect, useRef, useState, type ReactNode } from "react"
import { Link } from "react-router-dom"
import { useQuery } from "@tanstack/react-query"

import { fetchPublicStats } from "@/api/stats"
import { SITE_NAME } from "@/lib/site"
import { cn } from "@/lib/utils"
import { Reveal } from "@/components/landing/Reveal"

/*
 * The page guests see at `/` (signed-in users get the dashboard). It's a run of
 * full-height sections, several over Berlin and Munich photos. Photos are free
 * Unsplash images; if one fails to load, the section falls back to plain dark.
 */
const HERO_IMG =
  "https://images.unsplash.com/photo-1595867818082-083862f3d630?auto=format&fit=crop&w=2400&q=80"
const PHOTO_ISAR =
  "https://images.unsplash.com/photo-1770983437965-a88b456f2305?auto=format&fit=crop&w=2000&q=80"
const PHOTO_BERLIN =
  "https://images.unsplash.com/photo-1745878136928-d1b3c10afc35?auto=format&fit=crop&w=2000&q=80"
const PHOTO_MARIEN =
  "https://images.unsplash.com/photo-1780545311196-f8b507b08b94?auto=format&fit=crop&w=1400&q=80"

const PRIMARY_LINK =
  "inline-block rounded-full bg-primary px-8 py-3.5 text-base font-semibold text-primary-foreground transition-colors hover:bg-accent-hover"

export default function LandingPage() {
  return (
    <div className="min-h-screen bg-background text-white">
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
        "fixed inset-x-0 top-0 z-30 flex items-center justify-between px-6 py-4 transition-colors duration-300",
        solid ? "border-b border-border bg-background" : "bg-transparent",
      )}
    >
      <span className="flex items-center gap-2 font-grotesk text-lg font-bold">
        {/* der / die / das in their gender colours and shapes. */}
        <span className="inline-flex gap-1" aria-hidden="true">
          <span className="size-2.5 rounded-full bg-article-der" />
          <span
            className="size-2.5 bg-article-die"
            style={{ clipPath: "polygon(50% 0, 100% 100%, 0 100%)" }}
          />
          <span className="size-2.5 bg-article-das" />
        </span>
        {SITE_NAME}
      </span>
      <div className="flex items-center gap-2 text-sm font-semibold">
        <Link to="/login" className="rounded-full px-4 py-2 text-white/80 hover:text-white">
          Log in
        </Link>
        <Link
          to="/login"
          className="rounded-full bg-primary px-5 py-2 text-primary-foreground transition-colors hover:bg-accent-hover"
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
    <section className="relative flex h-screen min-h-[620px] items-center justify-center overflow-hidden bg-surface-2">
      {ok && (
        <img
          ref={imgRef}
          src={HERO_IMG}
          alt="München"
          onError={() => setOk(false)}
          className="absolute inset-0 h-[135%] w-full object-cover"
        />
      )}
      <div className="absolute inset-0 bg-gradient-to-t from-background via-background/40 to-background/70" />
      <div className="relative z-10 mx-auto max-w-4xl px-6 text-center">
        <Reveal>
          <p className="mb-4 text-xs font-semibold uppercase tracking-[0.25em] text-white/70">
            Deutsch lernen · A1
          </p>
          <h1 className="text-5xl font-bold leading-[1.05] sm:text-7xl">
            Learn German,
            <br />
            one short lesson a day.
          </h1>
          <p className="mx-auto mt-6 max-w-xl text-lg text-white/80">
            A guided A1 course with flashcards that come back just before you forget
            them, quick drills, and short reads on German history. More levels are
            being written.
          </p>
          <div className="mt-9 flex flex-col items-center justify-center gap-3 sm:flex-row">
            <Link to="/login" className={cn(PRIMARY_LINK, "w-full sm:w-auto")}>
              Start free
            </Link>
            <Link
              to="/login"
              className="w-full rounded-full border border-white/40 px-8 py-3.5 text-base font-semibold text-white transition-colors hover:bg-white/10 sm:w-auto"
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
    <Section bg={<PhotoBg src={PHOTO_MARIEN} />}>
      <Reveal>
        <SectionHeader label="Try it" title="der, die or das?" />
        <div className="mx-auto mt-10 max-w-md rounded-xl border border-border bg-background/90 p-8 text-center">
          {done ? (
            <>
              <p className="text-lg font-semibold">
                You got {score} of {TEASER.length}.
              </p>
              <p className="mt-1 text-sm text-white/75">
                Noun genders are hard. The drills give you plenty of practice with them.
              </p>
              <Link to="/login" className={cn(PRIMARY_LINK, "mt-6 px-6 py-2.5 text-sm")}>
                Create a free account
              </Link>
            </>
          ) : (
            <>
              <p className="text-sm text-white/75">Which article? ({current.en})</p>
              <p className="mt-2 font-grotesk text-4xl font-bold">{current.noun}</p>
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
                          ? "border-success bg-success/15 text-success"
                          : isWrong
                            ? "border-danger bg-danger/15 text-danger"
                            : "border-white/20 hover:border-white/50",
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

const FEATURES = [
  {
    title: "The path",
    body: "A1 split into short daily lessons. Each one mixes exercises with words to review.",
  },
  {
    title: "Spaced review",
    body: "Flashcards scheduled with SM-2, so each word returns just before you'd forget it.",
  },
  {
    title: "Word Bank",
    body: "Every word you've reached, grouped by level and part of speech.",
  },
  { title: "Drills", body: "Quick games for articles, spelling and word order." },
  {
    title: "History",
    body: "Short reads on German history, first in English and then in German.",
  },
  {
    title: "AI tutor and Recite",
    body: "Premium: ask a tutor anything, or retell a text aloud and get feedback on it.",
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
            <div className="h-full rounded-xl border border-border bg-surface p-6">
              <h3 className="font-bold">{f.title}</h3>
              <p className="mt-1 text-sm text-white/70">{f.body}</p>
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
        <p className="mx-auto mt-3 max-w-md text-center text-white/70">
          These are counted live from the database.
        </p>
        <div className="mt-10 grid grid-cols-2 gap-6 sm:grid-cols-4">
          {items.map((s) => (
            <div key={s.label} className="text-center">
              <p className="font-grotesk text-4xl font-bold text-primary sm:text-5xl">
                {s.value.toLocaleString()}
              </p>
              <p className="mt-1 text-sm text-white/70">{s.label}</p>
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
    <section className="relative flex min-h-screen items-center overflow-hidden bg-surface-2">
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
      <div className="absolute inset-0 bg-gradient-to-r from-background via-background/55 to-background/10" />
      <div className="absolute inset-x-0 top-0 h-40 bg-gradient-to-b from-background to-transparent" />
      <div className="absolute inset-x-0 bottom-0 h-40 bg-gradient-to-t from-background to-transparent" />

      <div className="relative z-10 mx-auto w-full max-w-5xl px-6">
        <Reveal className="max-w-xl">
          <SectionLabel>Mehr als Vokabeln</SectionLabel>
          <h2 className="mt-3 text-4xl font-bold leading-tight sm:text-5xl">
            Learn the language and the country
          </h2>
          <p className="mt-4 text-lg text-white/80">
            The history track covers the places and events behind the words you're
            learning.
          </p>
          <div className="mt-8 flex flex-wrap gap-2">
            {SIGHTS.map((s, i) => (
              <button
                key={s.name}
                onClick={() => setActive(i)}
                className={cn(
                  "rounded-full border px-4 py-2 text-sm font-semibold transition-colors",
                  i === active
                    ? "border-transparent bg-primary text-primary-foreground"
                    : "border-white/30 text-white/80 hover:text-white",
                )}
              >
                {s.name}
              </button>
            ))}
          </div>
          <p className="mt-3 text-sm text-white/70">{current.city}</p>
        </Reveal>
      </div>
    </section>
  )
}

const FAQS = [
  {
    q: "Is it free?",
    a: "Yes. The A1 path, review, Word Bank, grammar, drills, videos and history are free. Premium adds unlimited energy, the AI tutor and Recite.",
  },
  {
    q: "Do I need an account?",
    a: "You can try review, grammar, exercises and one drill as a guest. Sign in with Google or GitHub to save progress and follow the path.",
  },
  {
    q: "What level is it for?",
    a: "Beginners, for now. The A1 course is being added a few lessons at a time, and higher levels come after. If you already know some German, the placement test picks your starting level.",
  },
]

function FaqCta() {
  return (
    <Section>
      <Reveal>
        <SectionHeader label="Questions" title="Good to know" />
      </Reveal>
      <div className="mx-auto mt-10 max-w-2xl divide-y divide-border">
        {FAQS.map((f) => (
          <Reveal key={f.q}>
            <div className="py-5">
              <p className="font-semibold">{f.q}</p>
              <p className="mt-1 text-sm text-white/70">{f.a}</p>
            </div>
          </Reveal>
        ))}
      </div>

      <Reveal>
        <div className="mx-auto mt-14 max-w-2xl rounded-xl border border-border bg-surface p-10 text-center">
          <h2 className="text-3xl font-bold sm:text-4xl">Ready to start?</h2>
          <p className="mx-auto mt-3 max-w-md text-white/75">
            Sign in with Google or GitHub. It takes about a minute.
          </p>
          <Link to="/login" className={cn(PRIMARY_LINK, "mt-7")}>
            Start free
          </Link>
        </div>
      </Reveal>

      <footer className="mx-auto mt-14 flex w-full max-w-2xl flex-col items-center justify-between gap-3 border-t border-border pt-6 text-sm text-white/70 sm:flex-row">
        <span>
          © {new Date().getFullYear()} {SITE_NAME}
        </span>
        <div className="flex gap-4">
          <Link to="/privacy" className="hover:text-white">
            Privacy
          </Link>
          <Link to="/login" className="hover:text-white">
            Log in
          </Link>
        </div>
      </footer>
    </Section>
  )
}

/** A full-height section, optionally over a background (e.g. a photo). */
function Section({ children, bg }: { children: ReactNode; bg?: ReactNode }) {
  return (
    <section className="relative flex min-h-screen flex-col justify-center overflow-hidden px-6 py-24">
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
          className="absolute inset-0 size-full object-cover opacity-60"
        />
      )}
      <div className="absolute inset-0 bg-background/45" />
      <div className="absolute inset-x-0 top-0 h-40 bg-gradient-to-b from-background to-transparent" />
      <div className="absolute inset-x-0 bottom-0 h-40 bg-gradient-to-t from-background to-transparent" />
    </>
  )
}

function SectionHeader({ label, title }: { label: string; title: string }) {
  return (
    <div className="mx-auto max-w-2xl text-center">
      <SectionLabel>{label}</SectionLabel>
      <h2 className="mt-3 text-3xl font-bold sm:text-4xl">{title}</h2>
    </div>
  )
}

function SectionLabel({ children }: { children: ReactNode }) {
  return (
    <p className="text-xs font-semibold uppercase tracking-[0.2em] text-white/70">{children}</p>
  )
}
