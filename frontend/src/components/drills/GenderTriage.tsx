import { useEffect, useMemo, useState } from "react"
import { useQuery } from "@tanstack/react-query"
import { ArrowRight, Check, X } from "lucide-react"

import { fetchDrillWords } from "@/api/vocabulary"
import { splitArticle, shuffle } from "@/lib/german"
import { useGuestLimit } from "@/contexts/GuestLimitContext"
import { Button } from "@/components/ui/button"
import { cn } from "@/lib/utils"
import { DrillShell } from "./DrillShell"

/*
 * der, die or das? One noun at a time from the words you've learned. A right
 * answer shows the noun with its article and moves on by itself; a wrong one
 * shows the correction and waits for "Next", so it gets read. The summary
 * lists the mistakes and can replay just those.
 *
 * Green and red only mean right and wrong. The articles are told apart by the
 * logo's shapes (der circle, die triangle, das square) in their own colours.
 */
const ROUNDS = 15
const ARTICLES = ["der", "die", "das"] as const
const AUTO_NEXT_MS = 700

type Noun = { article: string; noun: string; english: string }

export function GenderTriage({ onExit }: { onExit: () => void }) {
  const { data: words } = useQuery({ queryKey: ["drill-words"], queryFn: fetchDrillWords })
  const { guard } = useGuestLimit()
  const [round, setRound] = useState<Noun[] | null>(null)
  const [i, setI] = useState(0)
  const [picked, setPicked] = useState<string | null>(null)
  const [mistakes, setMistakes] = useState<Noun[]>([])
  const [streak, setStreak] = useState(0)

  const nouns = useMemo(
    () =>
      (words ?? []).flatMap((w) => {
        const { article, noun } = splitArticle(w.german)
        return article ? [{ article, noun, english: w.english }] : []
      }),
    [words],
  )
  // The first round is drawn once when the words arrive; later rounds via start().
  const firstRound = useMemo(() => shuffle(nouns).slice(0, ROUNDS), [nouns])
  const pool = round ?? firstRound
  const current = pool[i]
  const answered = picked !== null
  const right = answered && picked === current?.article

  function start(next: Noun[]) {
    setRound(shuffle(next))
    setI(0)
    setPicked(null)
    setMistakes([])
    setStreak(0)
  }

  function choose(article: string) {
    if (answered || !current) return
    if (!guard()) return // guests: blocked once the daily free cap is hit
    setPicked(article)
    if (article === current.article) {
      setStreak((s) => s + 1)
    } else {
      setStreak(0)
      setMistakes((m) => [...m, current])
    }
  }

  function next() {
    setPicked(null)
    setI((n) => n + 1)
  }

  // A right answer moves on by itself.
  useEffect(() => {
    if (!right) return
    const t = setTimeout(() => {
      setPicked(null)
      setI((n) => n + 1)
    }, AUTO_NEXT_MS)
    return () => clearTimeout(t)
  }, [right])

  // Keys 1, 2, 3 answer der, die, das; Enter goes on after a mistake.
  useEffect(() => {
    function onKey(e: KeyboardEvent) {
      const article = ARTICLES[Number(e.key) - 1]
      if (article) document.getElementById(`triage-${article}`)?.click()
      if (e.key === "Enter") document.getElementById("triage-next")?.click()
    }
    window.addEventListener("keydown", onKey)
    return () => window.removeEventListener("keydown", onKey)
  }, [])

  if (!words) {
    return (
      <DrillShell title="der, die, das" onExit={onExit}>
        <p className="py-10 text-center text-muted-foreground">Loading…</p>
      </DrillShell>
    )
  }
  if (nouns.length === 0) {
    return (
      <DrillShell title="der, die, das" onExit={onExit}>
        <p className="py-10 text-center text-muted-foreground">
          No nouns learned yet. Finish a lesson on your path to unlock them.
        </p>
      </DrillShell>
    )
  }
  if (!current) {
    return (
      <DrillShell title="der, die, das" onExit={onExit}>
        <Summary
          total={pool.length}
          mistakes={mistakes}
          onAgain={() => start(shuffle(nouns).slice(0, ROUNDS))}
          onMistakes={() => start(mistakes)}
          onExit={onExit}
        />
      </DrillShell>
    )
  }

  const rightSoFar = i + (answered ? 1 : 0) - mistakes.length

  return (
    <DrillShell
      title="der, die, das"
      onExit={onExit}
      progress={((i + (answered ? 1 : 0)) / pool.length) * 100}
      counter={`${i + 1} / ${pool.length}`}
    >
      <div className="mx-auto flex w-full max-w-xl flex-col gap-6">
        <p className="flex justify-center gap-5 text-sm text-muted-foreground">
          <span>
            <span className="font-semibold tabular-nums text-foreground">{rightSoFar}</span> right
          </span>
          <span>
            Streak <span className="font-semibold tabular-nums text-foreground">{streak}</span>
          </span>
        </p>

        <div
          key={i}
          className={cn(
            "rounded-[28px] border-2 bg-surface px-6 py-10 text-center shadow-card animate-in fade-in-0 slide-in-from-bottom-2 duration-300",
            !answered && "border-transparent",
            right && "border-[hsl(var(--success))]",
            answered && !right && "border-[hsl(var(--danger))]",
          )}
        >
          <p className="font-grotesk text-4xl font-extrabold tracking-tight [overflow-wrap:anywhere] sm:text-5xl">
            {answered ? (
              <>
                <ArticleWord article={current.article} /> {current.noun}
              </>
            ) : (
              <>
                <span className="text-muted-foreground/50">___</span> {current.noun}
              </>
            )}
          </p>
          <p className="mt-3 text-muted-foreground">{current.english}</p>
          {answered && (
            <p
              className={cn(
                "mt-4 inline-flex items-center gap-1.5 text-sm font-semibold",
                right ? "text-[hsl(var(--success))]" : "text-[hsl(var(--danger))]",
              )}
            >
              {right ? <Check className="size-4" /> : <X className="size-4" />}
              {right ? "Richtig!" : `Not ${picked}: it's ${current.article} ${current.noun}.`}
            </p>
          )}
        </div>

        <div className="grid grid-cols-3 gap-3">
          {ARTICLES.map((article, n) => {
            const isAnswer = answered && article === current.article
            const isWrongPick = answered && article === picked && !right
            return (
              <button
                key={article}
                id={`triage-${article}`}
                onClick={() => choose(article)}
                disabled={answered}
                className={cn(
                  "flex h-20 flex-col items-center justify-center gap-1 rounded-2xl border-2 bg-surface shadow-card transition-[transform,border-color,background-color] active:scale-95 sm:h-24",
                  isAnswer
                    ? "border-[hsl(var(--success))] bg-[hsl(var(--success-bg))]"
                    : isWrongPick
                      ? "border-[hsl(var(--danger))] bg-[hsl(var(--danger-bg))]"
                      : "border-transparent hover:border-border",
                  answered && !isAnswer && !isWrongPick && "opacity-50",
                )}
              >
                <span className="flex items-center gap-2 text-2xl font-bold sm:text-3xl">
                  <ArticleShape article={article} />
                  {article}
                </span>
                <span className="hidden text-[11px] text-muted-foreground sm:block">{n + 1}</span>
              </button>
            )
          })}
        </div>

        {answered && !right && (
          <Button id="triage-next" size="lg" onClick={next} className="self-center">
            Next <ArrowRight />
          </Button>
        )}
      </div>
    </DrillShell>
  )
}

const ARTICLE_COLOUR: Record<string, string> = {
  der: "hsl(var(--article-der))",
  die: "hsl(var(--article-die))",
  das: "hsl(var(--article-das))",
}

/** The logo's marks: der a circle, die a triangle, das a square. */
function ArticleShape({ article }: { article: string }) {
  return (
    <svg viewBox="0 0 24 24" className="size-5 shrink-0" aria-hidden="true" fill={ARTICLE_COLOUR[article]}>
      {article === "der" && <circle cx="12" cy="12" r="10" />}
      {article === "die" && <path d="M12 2.5 22 21H2z" />}
      {article === "das" && <rect x="3" y="3" width="18" height="18" rx="2" />}
    </svg>
  )
}

function ArticleWord({ article }: { article: string }) {
  return <span style={{ color: ARTICLE_COLOUR[article] }}>{article}</span>
}

function Summary({
  total,
  mistakes,
  onAgain,
  onMistakes,
  onExit,
}: {
  total: number
  mistakes: Noun[]
  onAgain: () => void
  onMistakes: () => void
  onExit: () => void
}) {
  const right = total - mistakes.length
  return (
    <div className="mx-auto flex w-full max-w-md flex-col items-center gap-4 rounded-[28px] bg-surface px-6 py-10 text-center shadow-card">
      <h2 className="text-3xl font-extrabold">Done</h2>
      <p className="font-grotesk text-6xl font-extrabold tabular-nums tracking-tight">
        {right}
        <span className="text-3xl text-muted-foreground">/{total}</span>
      </p>
      {mistakes.length > 0 && (
        <div className="w-full text-left">
          <p className="mb-2 text-sm font-semibold">Learn these:</p>
          <ul className="divide-y divide-border rounded-2xl bg-surface-2">
            {mistakes.map((m) => (
              <li key={m.article + m.noun} className="flex items-center gap-3 px-4 py-2.5">
                <ArticleShape article={m.article} />
                <span className="font-semibold">
                  <ArticleWord article={m.article} /> {m.noun}
                </span>
                <span className="ml-auto truncate text-sm text-muted-foreground">{m.english}</span>
              </li>
            ))}
          </ul>
        </div>
      )}
      <div className="mt-3 flex w-full flex-col gap-2.5">
        {mistakes.length > 0 && (
          <Button size="lg" onClick={onMistakes}>
            Practise these again
          </Button>
        )}
        <Button size="lg" variant={mistakes.length ? "secondary" : "default"} onClick={onAgain}>
          New round
        </Button>
        <Button size="lg" variant="ghost" onClick={onExit}>
          Back to drills
        </Button>
      </div>
    </div>
  )
}
