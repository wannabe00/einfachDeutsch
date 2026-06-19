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
  // start fresh automatically — we only need to focus the input on mount.
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

  const borderClass =
    verdict === "correct"
      ? "border-success"
      : verdict === "close"
        ? "border-warning"
        : verdict === "wrong"
          ? "border-danger"
          : "border-border"

  const bgClass =
    verdict === "correct"
      ? "bg-[hsl(var(--success-bg))]"
      : verdict === "close"
        ? "bg-[hsl(var(--warning-bg))]"
        : verdict === "wrong"
          ? "bg-[hsl(var(--danger-bg))]"
          : "bg-surface"

  return (
    <div
      className={cn(
        "mx-auto w-full max-w-[480px] rounded-xl border-2 p-8 shadow-sm transition-colors duration-150",
        borderClass,
        bgClass,
      )}
    >
      {/* Chapter badge */}
      <div className="mb-6 flex justify-end">
        <span className="rounded-full bg-muted px-2.5 py-0.5 text-xs font-medium text-muted-foreground">
          {chapterTitle}
        </span>
      </div>

      {/* English prompt */}
      <p className="mb-8 text-center text-2xl font-semibold tracking-tight text-foreground">
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
            className="text-center text-base"
          />
          <UmlautBar inputRef={inputRef} value={input} onChange={setInput} />
          <Button type="submit" className="w-full">
            Check
          </Button>
          <button
            type="button"
            onClick={onSkip}
            className="mx-auto text-sm text-muted-foreground hover:text-accent"
          >
            Skip — review later
          </button>
        </form>
      ) : (
        <div className="flex flex-col gap-4">
          {/* Feedback message */}
          <p
            className={cn(
              "text-center text-sm font-medium",
              verdict === "correct"
                ? "text-[hsl(var(--success))]"
                : verdict === "close"
                  ? "text-[hsl(var(--warning))]"
                  : "text-[hsl(var(--danger))]",
            )}
          >
            {verdict === "correct"
              ? "✓ Correct!"
              : verdict === "close"
                ? "Almost — check your spelling"
                : `The answer is: ${word.german}`}
          </p>

          {/* SRS quality buttons */}
          <div className="grid grid-cols-4 gap-2">
            {(
              [
                { label: "Again", quality: 0, hint: "tomorrow", className: "border-danger/40 bg-[hsl(var(--danger-bg))] text-[hsl(var(--danger))] hover:bg-[hsl(var(--danger-bg))]" },
                { label: "Hard", quality: 2, hint: "3 days", className: "border-warning/40 bg-[hsl(var(--warning-bg))] text-[hsl(var(--warning))] hover:bg-[hsl(var(--warning-bg))]" },
                { label: "Good", quality: 4, hint: "1 week", className: "border-accent/40 bg-blue-50 text-accent dark:bg-blue-950/40 hover:bg-blue-100 dark:hover:bg-blue-900/40" },
                { label: "Easy", quality: 5, hint: "2+ weeks", className: "border-success/40 bg-[hsl(var(--success-bg))] text-[hsl(var(--success))] hover:bg-[hsl(var(--success-bg))]" },
              ] as const
            ).map(({ label, quality, hint, className }) => (
              <button
                key={label}
                onClick={() => onRate(quality)}
                className={cn(
                  "flex flex-col items-center rounded-lg border px-2 py-2.5 text-xs font-medium transition-opacity hover:opacity-80",
                  className,
                )}
              >
                <span className="text-sm font-semibold">{label}</span>
                <span className="mt-0.5 opacity-70">{hint}</span>
              </button>
            ))}
          </div>
        </div>
      )}
    </div>
  )
}
