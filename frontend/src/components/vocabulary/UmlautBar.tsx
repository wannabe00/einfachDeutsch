import type { RefObject } from "react"

const CHARS = ["ä", "ö", "ü", "ß", "Ä", "Ö", "Ü"]

interface UmlautBarProps {
  inputRef: RefObject<HTMLInputElement | null>
  value: string
  onChange: (next: string) => void
}

/** A row of buttons that insert German special characters at the cursor. */
export function UmlautBar({ inputRef, value, onChange }: UmlautBarProps) {
  function insert(char: string) {
    const el = inputRef.current
    if (!el) {
      onChange(value + char)
      return
    }
    const start = el.selectionStart ?? value.length
    const end = el.selectionEnd ?? value.length
    const next = value.slice(0, start) + char + value.slice(end)
    onChange(next)
    // Restore focus + caret just after the inserted character.
    requestAnimationFrame(() => {
      el.focus()
      const pos = start + char.length
      el.setSelectionRange(pos, pos)
    })
  }

  return (
    <div className="flex flex-wrap justify-center gap-1.5">
      {CHARS.map((c) => (
        <button
          key={c}
          type="button"
          onClick={() => insert(c)}
          aria-label={`Insert ${c}`}
          className="rounded-md border border-border bg-surface px-2.5 py-1 text-sm font-medium text-foreground transition-colors hover:border-accent hover:bg-background"
        >
          {c}
        </button>
      ))}
    </div>
  )
}
