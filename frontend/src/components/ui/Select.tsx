import { useEffect, useId, useLayoutEffect, useRef, useState, type ReactNode } from "react"
import { createPortal } from "react-dom"
import { Check, ChevronDown } from "lucide-react"

import { cn } from "@/lib/utils"

/*
 * A styled dropdown used instead of the browser's <select>, which looks
 * different (and sits differently) in every browser. On wide screens the list
 * opens as a popover under the field (above it when there's no room); on
 * phones it opens as a bottom sheet. Options can carry a small leading picture
 * and a second line, and can be grouped under headings.
 *
 * Keyboard: Enter, Space or the arrow keys open it; arrows, Home and End move;
 * Enter picks; Escape or Tab closes; typing a letter jumps to the next option
 * starting with it.
 */

export interface SelectOption<T extends string | number> {
  value: T
  label: string
  description?: string
  leading?: ReactNode
  /** Options with the same group are listed together under that heading. */
  group?: string
}

const PHONE = "(max-width: 639px)"
const GAP = 6
const MAX_HEIGHT = 340

export function Select<T extends string | number>({
  value,
  onChange,
  options,
  label,
  className,
}: {
  value: T
  onChange: (value: T) => void
  options: SelectOption<T>[]
  /** The accessible name (shown as the sheet title on phones). */
  label: string
  className?: string
}) {
  const id = useId()
  const triggerRef = useRef<HTMLButtonElement>(null)
  const listRef = useRef<HTMLDivElement>(null)
  const [open, setOpen] = useState(false)
  const [active, setActive] = useState(0)
  const [phone, setPhone] = useState(false)
  const [place, setPlace] = useState<{ top: number; left: number; width: number; up: boolean }>()

  const selected = options.find((o) => o.value === value) ?? options[0]

  function show() {
    setPhone(window.matchMedia(PHONE).matches)
    setActive(Math.max(0, options.indexOf(selected)))
    setOpen(true)
  }

  function close(refocus = true) {
    setOpen(false)
    if (refocus) triggerRef.current?.focus()
  }

  function pick(index: number) {
    const option = options[index]
    if (option) onChange(option.value)
    close()
  }

  // Popover position, kept in place while the page scrolls or resizes.
  useLayoutEffect(() => {
    if (!open || phone) return
    function measure() {
      const r = triggerRef.current?.getBoundingClientRect()
      if (!r) return
      const below = window.innerHeight - r.bottom
      const up = below < Math.min(MAX_HEIGHT, 220) && r.top > below
      setPlace({ top: up ? r.top - GAP : r.bottom + GAP, left: r.left, width: r.width, up })
    }
    measure()
    window.addEventListener("resize", measure)
    window.addEventListener("scroll", measure, true)
    return () => {
      window.removeEventListener("resize", measure)
      window.removeEventListener("scroll", measure, true)
    }
  }, [open, phone])

  // Focus the list when it opens; close on a click outside it.
  useEffect(() => {
    if (!open) return
    listRef.current?.focus({ preventScroll: true })
    function outside(e: PointerEvent) {
      const target = e.target as Node
      if (!listRef.current?.contains(target) && !triggerRef.current?.contains(target)) close(false)
    }
    document.addEventListener("pointerdown", outside)
    return () => document.removeEventListener("pointerdown", outside)
  }, [open])

  // Keep the active option in view.
  useEffect(() => {
    if (open) document.getElementById(`${id}-${active}`)?.scrollIntoView({ block: "nearest" })
  }, [open, active, id])

  function onListKey(e: React.KeyboardEvent) {
    const last = options.length - 1
    const moves: Record<string, number> = {
      ArrowDown: Math.min(last, active + 1),
      ArrowUp: Math.max(0, active - 1),
      Home: 0,
      End: last,
      PageDown: Math.min(last, active + 8),
      PageUp: Math.max(0, active - 8),
    }
    if (e.key in moves) {
      e.preventDefault()
      setActive(moves[e.key])
    } else if (e.key === "Enter" || e.key === " ") {
      e.preventDefault()
      pick(active)
    } else if (e.key === "Escape") {
      e.preventDefault()
      close()
    } else if (e.key === "Tab") {
      close(false)
    } else if (e.key.length === 1) {
      const letter = e.key.toLowerCase()
      const order = [...options.slice(active + 1), ...options.slice(0, active + 1)]
      const hit = order.find((o) => o.label.toLowerCase().startsWith(letter))
      if (hit) setActive(options.indexOf(hit))
    }
  }

  const list = (
    <div
      ref={listRef}
      role="listbox"
      tabIndex={-1}
      aria-label={label}
      aria-activedescendant={`${id}-${active}`}
      onKeyDown={onListKey}
      className={cn("overflow-y-auto overscroll-contain p-1.5 focus:outline-none", phone ? "max-h-[65vh]" : "")}
      style={phone ? undefined : { maxHeight: MAX_HEIGHT }}
    >
      {options.map((option, i) => {
        const heading = option.group && option.group !== options[i - 1]?.group ? option.group : null
        const isSelected = option.value === selected?.value
        return (
          <div key={String(option.value)}>
            {heading && (
              <p className="px-3 pb-1 pt-3 text-xs font-semibold uppercase tracking-[0.06em] text-muted-foreground first:pt-1.5">
                {heading}
              </p>
            )}
            <div
              id={`${id}-${i}`}
              role="option"
              aria-selected={isSelected}
              onPointerMove={() => setActive(i)}
              onClick={() => pick(i)}
              className={cn(
                "flex min-h-[48px] cursor-pointer items-center gap-3 rounded-xl px-3 py-2",
                i === active && "bg-surface-2",
              )}
            >
              {option.leading}
              <span className="min-w-0 flex-1">
                <span className={cn("block truncate", isSelected && "font-semibold")}>{option.label}</span>
                {option.description && (
                  <span className="block truncate text-sm text-muted-foreground">{option.description}</span>
                )}
              </span>
              {isSelected && <Check className="size-[18px] shrink-0 text-[hsl(var(--choice))]" aria-hidden="true" />}
            </div>
          </div>
        )
      })}
    </div>
  )

  return (
    <>
      <button
        ref={triggerRef}
        type="button"
        aria-haspopup="listbox"
        aria-expanded={open}
        aria-label={`${label}: ${selected?.label ?? ""}`}
        onClick={() => (open ? close() : show())}
        onKeyDown={(e) => {
          if (!open && ["ArrowDown", "ArrowUp", "Enter", " "].includes(e.key)) {
            e.preventDefault()
            show()
          }
        }}
        className={cn(
          "flex h-12 w-full items-center gap-3 rounded-xl border border-transparent bg-surface-2 pl-3 pr-3.5 text-left text-base font-normal text-foreground transition-colors hover:bg-border/60 focus-visible:border-ring focus-visible:outline-none",
          open && "border-ring",
          className,
        )}
      >
        {selected?.leading}
        <span className="min-w-0 flex-1 truncate">{selected?.label}</span>
        <ChevronDown
          className={cn("size-5 shrink-0 text-muted-foreground transition-transform", open && "rotate-180")}
          aria-hidden="true"
        />
      </button>
      {open &&
        createPortal(
          phone ? (
            <div className="fixed inset-0 z-50 flex flex-col justify-end">
              <div className="absolute inset-0 bg-black/40 animate-in fade-in-0 duration-150" aria-hidden="true" />
              <div className="relative rounded-t-[24px] bg-popover pb-[max(12px,env(safe-area-inset-bottom))] text-popover-foreground shadow-card animate-in slide-in-from-bottom-8 duration-200">
                <div className="mx-auto mt-2.5 h-1 w-10 rounded-full bg-border" aria-hidden="true" />
                <p className="px-5 pb-1 pt-3 font-semibold">{label}</p>
                {list}
              </div>
            </div>
          ) : (
            place && (
              <div
                className="fixed z-50 rounded-2xl bg-popover text-popover-foreground shadow-[0_12px_40px_rgb(0_0_0/0.18)] ring-1 ring-border animate-in fade-in-0 zoom-in-95 duration-100"
                style={{
                  left: place.left,
                  width: Math.max(place.width, 260),
                  ...(place.up ? { bottom: window.innerHeight - place.top } : { top: place.top }),
                }}
              >
                {list}
              </div>
            )
          ),
          document.body,
        )}
    </>
  )
}
