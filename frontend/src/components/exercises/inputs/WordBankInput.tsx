import type { ExercisePayload } from "@/types"
import { cn } from "@/lib/utils"

/**
 * A text with `___` gaps and a bank of words. Tapping a word puts it in the
 * first empty gap; tapping a filled gap empties it again. Each bank word can be
 * used once (duplicates in the bank can each be used once).
 *
 * `value` holds one entry per gap, with "" for an empty gap. After checking,
 * `solution` (the right word per gap) colours each gap green or red.
 */
export function WordBankInput({
  payload,
  value,
  onChange,
  disabled,
  solution,
}: {
  payload: ExercisePayload
  value: string[]
  onChange: (v: string[]) => void
  disabled: boolean
  solution?: string[]
}) {
  const parts = (payload.text ?? "").split("___")
  const gaps = parts.length - 1
  const bank = payload.bank ?? []
  const slots = Array.from({ length: gaps }, (_, i) => value[i] ?? "")

  // How many times each word is already placed, so duplicates stay available.
  const placed = new Map<string, number>()
  for (const w of slots) if (w) placed.set(w, (placed.get(w) ?? 0) + 1)
  const seen = new Map<string, number>()

  function fill(word: string) {
    const i = slots.indexOf("")
    if (i === -1) return
    onChange(slots.map((s, j) => (j === i ? word : s)))
  }

  function clear(i: number) {
    onChange(slots.map((s, j) => (j === i ? "" : s)))
  }

  return (
    <div className="flex flex-col gap-4">
      <p className="whitespace-pre-line text-base leading-9">
        {parts.map((part, i) => (
          <span key={i}>
            {part}
            {i < gaps && (
              <button
                type="button"
                disabled={disabled || !slots[i]}
                onClick={() => clear(i)}
                className={cn(
                  "mx-1 inline-flex min-w-16 justify-center rounded-md border-b-2 px-2 align-baseline",
                  solution
                    ? same(slots[i], solution[i])
                      ? "border-[hsl(var(--success))] bg-[hsl(var(--success-bg))]"
                      : "border-[hsl(var(--danger))] bg-[hsl(var(--danger-bg))]"
                    : slots[i]
                      ? "border-[hsl(var(--choice))] bg-[hsl(var(--choice-bg))]"
                      : "border-muted-foreground text-muted-foreground",
                )}
              >
                {slots[i] || " "}
              </button>
            )}
          </span>
        ))}
      </p>
      <div className="flex flex-wrap gap-2">
        {bank.map((w, i) => {
          const n = (seen.get(w) ?? 0) + 1
          seen.set(w, n)
          const used = n <= (placed.get(w) ?? 0)
          return (
            <button
              key={`${w}-${i}`}
              type="button"
              disabled={disabled || used || !slots.includes("")}
              onClick={() => fill(w)}
              className="min-h-[44px] rounded-xl bg-surface-2 px-3.5 py-2 text-[15px] font-medium transition-colors hover:bg-border disabled:opacity-40"
            >
              {w}
            </button>
          )
        })}
      </div>
    </div>
  )
}

/** Loose comparison, like the server's grading (case and spaces ignored). */
function same(a = "", b = "") {
  return a.trim().toLowerCase() === b.trim().toLowerCase()
}
