import { type ReactNode } from "react"

import { cn } from "@/lib/utils"

/** A titled card; `danger` tints the border + heading red. */
export function Section({
  title,
  children,
  danger,
}: {
  title: string
  children: ReactNode
  danger?: boolean
}) {
  return (
    <section
      className={cn(
        "flex flex-col rounded-2xl bg-surface p-5 shadow-card sm:p-6",
        danger && "ring-1 ring-[hsl(var(--danger))]/40",
      )}
    >
      <h2 className={cn("text-lg font-bold", danger && "text-[hsl(var(--danger))]")}>
        {title}
      </h2>
      <div className="mt-4">{children}</div>
    </section>
  )
}

/** A labelled form field wrapper. */
export function Field({ label, children }: { label: string; children: ReactNode }) {
  return (
    <label className="flex flex-col gap-1.5 text-sm font-medium text-muted-foreground">
      {label}
      {children}
    </label>
  )
}

/** A labelled switch row (label left, toggle right). */
export function Toggle({
  label,
  checked,
  onChange,
}: {
  label: string
  checked: boolean
  onChange: (v: boolean) => void
}) {
  return (
    <div className="flex min-h-[48px] items-center justify-between gap-3 py-1.5 text-[15px]">
      <span>{label}</span>
      <button
        type="button"
        role="switch"
        aria-checked={checked}
        aria-label={label}
        onClick={() => onChange(!checked)}
        className={cn(
          "relative inline-flex h-7 w-12 shrink-0 items-center rounded-full transition-colors",
          checked ? "bg-[hsl(var(--success))]" : "bg-surface-2",
        )}
      >
        <span
          className={cn(
            "inline-block size-6 rounded-full bg-white shadow transition-transform",
            checked ? "translate-x-[22px]" : "translate-x-0.5",
          )}
        />
      </button>
    </div>
  )
}

/** A success/error inline message. */
export function Msg({ tone, children }: { tone: "success" | "danger"; children: ReactNode }) {
  return (
    <p
      className={cn(
        "mt-2 text-sm",
        tone === "success" ? "text-[hsl(var(--success))]" : "text-[hsl(var(--danger))]",
      )}
    >
      {children}
    </p>
  )
}
