import { useState } from "react"

import type { ExercisePayload } from "@/types"
import { cn } from "@/lib/utils"

/**
 * Tap an item on the left, then its partner on the right. Each left item has
 * its own colour; once matched, the left item and its partner both carry that
 * colour, so the pairs read at a glance without the columns changing height.
 * Tapping a matched left item again lets you change its partner. Right-hand
 * items can repeat (several nouns can all match "der"), so they never get used
 * up and may show several colours.
 *
 * After checking, `solution` turns each pair green (right) or red (wrong); the
 * pair colours never use green or red, so the two can't be confused.
 */
const PAIR_COLOURS = [1, 2, 3, 4, 5, 6].map((n) => `hsl(var(--pair-${n}))`)
const RIGHT = "hsl(var(--success))"
const WRONG = "hsl(var(--danger))"

export function MatchingInput({
  payload,
  value,
  onChange,
  disabled,
  solution,
}: {
  payload: ExercisePayload
  value: Record<string, string>
  onChange: (v: Record<string, string>) => void
  disabled: boolean
  solution?: [string, string][]
}) {
  const [selectedLeft, setSelectedLeft] = useState<string | null>(null)
  const left = payload.left ?? []
  const right = payload.right ?? []
  const colourOf = (l: string) => PAIR_COLOURS[left.indexOf(l) % PAIR_COLOURS.length]
  const answerFor = new Map(solution ?? [])
  const isRight = (l: string) => answerFor.get(l)?.toLowerCase() === value[l]?.toLowerCase()

  function pickRight(r: string) {
    if (!selectedLeft) return
    onChange({ ...value, [selectedLeft]: r })
    setSelectedLeft(null)
  }

  /** Border colour for a left item: green/red once checked, else its pair colour. */
  function leftBorder(l: string): string | undefined {
    if (solution) return isRight(l) ? RIGHT : WRONG
    return l in value || selectedLeft === l ? colourOf(l) : undefined
  }

  function rightBorder(partners: string[]): string | undefined {
    if (!partners.length) return undefined
    if (solution) return partners.every(isRight) ? RIGHT : WRONG
    return partners.length === 1 ? colourOf(partners[0]) : undefined
  }

  return (
    <div className="grid grid-cols-2 gap-3">
      <div className="flex flex-col gap-2">
        {left.map((l) => {
          const border = leftBorder(l)
          return (
            <button
              key={l}
              type="button"
              disabled={disabled}
              onClick={() => setSelectedLeft(selectedLeft === l ? null : l)}
              aria-pressed={selectedLeft === l}
              aria-label={l in value ? `${l}, matched with ${value[l]}` : l}
              className={cn(
                "flex min-h-11 items-center gap-2 rounded-xl border-2 px-3 py-2 text-left text-sm transition-colors",
                border ? "bg-surface" : "border-transparent bg-surface-2",
              )}
              style={border ? { borderColor: border } : undefined}
            >
              <Dot colour={colourOf(l)} filled={l in value} />
              <span className="flex-1">{l}</span>
            </button>
          )
        })}
      </div>
      <div className="flex flex-col gap-2">
        {right.map((r) => {
          const partners = left.filter((l) => value[l] === r)
          const border = rightBorder(partners)
          return (
            <button
              key={r}
              type="button"
              disabled={disabled || !selectedLeft}
              onClick={() => pickRight(r)}
              aria-label={partners.length ? `${r}, matched with ${partners.join(", ")}` : r}
              className={cn(
                "flex min-h-11 items-center gap-2 rounded-xl border-2 px-3 py-2 text-left text-sm transition-colors",
                border ? "bg-surface" : "border-transparent bg-surface-2",
                selectedLeft && !border && "hover:border-border",
                !selectedLeft && !partners.length && "text-muted-foreground",
              )}
              style={border ? { borderColor: border } : undefined}
            >
              <span className="flex-1">{r}</span>
              <span className="flex shrink-0 gap-1">
                {partners.map((l) => (
                  <Dot key={l} colour={colourOf(l)} filled />
                ))}
              </span>
            </button>
          )
        })}
      </div>
    </div>
  )
}

function Dot({ colour, filled }: { colour: string; filled: boolean }) {
  return (
    <span
      aria-hidden
      className="size-3 shrink-0 rounded-full border-2"
      style={{ borderColor: colour, background: filled ? colour : "transparent" }}
    />
  )
}
