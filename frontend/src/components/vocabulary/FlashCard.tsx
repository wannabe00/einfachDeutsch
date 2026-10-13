import { useState, type FormEvent, useRef, useEffect } from "react"
import { levenshtein } from "@/lib/levenshtein"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { cn } from "@/lib/utils"
import type { Word } from "@/types"
import { UmlautBar } from "./UmlautBar"

type Verdict = "correct" | "close" | "wrong" | null

function normalize(s: string) {
  return s.trim().toLowerCase()
}

function parseArticleAndNoun(german: string): [string, string] {
  const articles = ["der", "die", "das", "ein", "eine"]
  const parts = german.trim().split(/\s+/)
  if (parts.length > 1 && articles.includes(parts[0].toLowerCase())) {
    return [parts[0].toLowerCase(), parts.slice(1).join(" ")]
  }
  return ["", german]
}

function checkAnswer(input: string, correct: string): Verdict {
  if (normalize(input) === normalize(correct)) return "correct"
  const [cArticle, cNoun] = parseArticleAndNoun(correct)
  const [iArticle, iNoun] = parseArticleAndNoun(input)
  if (cArticle && iArticle === cArticle) {
    const dist = levenshtein(normalize(iNoun), normalize(cNoun))
    if (dist >= 1 && dist <= 2) return "close"
  }
  return "wrong"
}

interface FlashCardProps {
  word: Word
  chapterTitle: string
  onRate: (quality: 0 | 2 | 4 | 5) => void
  onSkip: () => void
}

export function FlashCard({ word, chapterTitle, onRate, onSkip }: FlashCardProps) {
  // ReviewPage remounts this card per word (keyed on word.id), so input/verdict
  // start fresh automatically; we only need to focus the input on mount.
  const [input, setInput] = useState("")
  const [verdict, setVerdict] = useState<Verdict>(null)
  const inputRef = useRef<HTMLInputElement>(null)

  useEffect(() => {
    const t = setTimeout(() => inputRef.current?.focus(), 50)
    return () => clearTimeout(t)
  }, [])

  function handleSubmit(e: FormEvent) {
    e.preventDefault()
    if (!input.trim()) return
    setVerdict(checkAnswer(input, word.german))
  }

  // The card itself turns green / amber / red with the verdict.
  const toneClass =
    verdict === "correct"
      ? "ring-2 ring-success"
      : verdict === "close"
        ? "ring-2 ring-warning"
        : verdict === "wrong"
          ? "ring-2 ring-danger"
          : ""

  return (
    <div
      className={cn(
        "w-full rounded-[28px] bg-surface p-6 shadow-card transition-shadow duration-200 sm:p-8",
        toneClass,
      )}
    >
      {/* Chapter badge */}
      <div className="mb-6 flex justify-center">
        <span className="rounded-full bg-surface-2 px-3 py-1 text-xs font-semibold text-muted-foreground">
          {chapterTitle}
        </span>
      </div>

      {/* English prompt */}
      <p className="mb-8 text-center font-grotesk text-2xl font-extrabold tracking-tight text-foreground [overflow-wrap:anywhere] sm:text-4xl">
        {word.english}
      </p>

      {verdict === null ? (
        <form onSubmit={handleSubmit} className="flex flex-col gap-3">
          <Input
            ref={inputRef}
            value={input}
            onChange={(e) => setInput(e.target.value)}
            placeholder="Type in German with article…"
            aria-label="Type the German translation"
            className="h-14 text-center text-lg"
          />
          <UmlautBar inputRef={inputRef} value={input} onChange={setInput} />
          <Button type="submit" size="lg" className="mt-1 w-full">
            Check
          </Button>
          <button
            type="button"
            onClick={onSkip}
            className="mx-auto min-h-[44px] px-3 text-sm font-medium text-muted-foreground hover:text-foreground"
          >
            Skip for now
          </button>
        </form>
      ) : (
        <div className="flex flex-col gap-5 animate-in fade-in-0 slide-in-from-bottom-1 duration-200">
          {/* Feedback message */}
          <p
            className={cn(
              "text-center text-base font-semibold",
              verdict === "correct"
                ? "text-[hsl(var(--success))]"
                : verdict === "close"
                  ? "text-[hsl(var(--warning))]"
                  : "text-[hsl(var(--danger))]",
            )}
          >
            {verdict === "correct"
              ? "Correct"
              : verdict === "close"
                ? "Almost. Check your spelling."
                : `The answer is: ${word.german}`}
          </p>

          {/* SRS quality buttons */}
          <div className="grid grid-cols-2 gap-2 min-[400px]:grid-cols-4">
            {(
              [
                { label: "Again", quality: 0, hint: "tomorrow", className: "bg-danger-bg text-danger" },
                { label: "Hard", quality: 2, hint: "3 days", className: "bg-warning-bg text-warning" },
                { label: "Good", quality: 4, hint: "1 week", className: "bg-article-der/10 text-article-der" },
                { label: "Easy", quality: 5, hint: "2+ weeks", className: "bg-success-bg text-success" },
              ] as const
            ).map(({ label, quality, hint, className }) => (
              <button
                key={label}
                onClick={() => onRate(quality)}
                className={cn(
                  "flex min-h-[64px] flex-col items-center justify-center rounded-2xl px-2 py-2.5 text-xs font-medium transition-[filter,transform] hover:brightness-95 active:scale-95",
                  className,
                )}
              >
                <span className="text-[15px] font-bold">{label}</span>
                <span className="mt-0.5 opacity-70">{hint}</span>
              </button>
            ))}
          </div>
        </div>
      )}
    </div>
  )
}
