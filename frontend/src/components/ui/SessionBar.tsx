import type { ReactNode } from "react"
import { X } from "lucide-react"

/*
 * The bar on top of every focused session (lessons, review, practice, drills):
 * a round close button, an optional label, a thick progress bar and a counter.
 */
export function SessionBar({
  onClose,
  closeLabel,
  progress,
  title,
  counter,
}: {
  /** Omit to hide the close button (e.g. mid-exam, where leaving loses answers). */
  onClose?: () => void
  closeLabel?: string
  /** 0-100; omit for sessions without a fixed length. */
  progress?: number
  title?: ReactNode
  counter?: ReactNode
}) {
  return (
    <div className="flex items-center gap-3 sm:gap-4">
      {onClose && (
        <button
          onClick={onClose}
          aria-label={closeLabel ?? "Close"}
          className="flex size-11 shrink-0 items-center justify-center rounded-full bg-surface-2 text-muted-foreground transition-colors hover:text-foreground"
        >
          <X className="size-5" />
        </button>
      )}
      <div className="min-w-0 flex-1">
        {title && <div className="mb-1.5 truncate text-[13px] font-semibold text-muted-foreground">{title}</div>}
        {progress !== undefined && (
          <div
            className="h-3 overflow-hidden rounded-full bg-surface-2"
            role="progressbar"
            aria-valuemin={0}
            aria-valuemax={100}
            aria-valuenow={Math.round(progress)}
          >
            <div
              className="h-full rounded-full bg-primary transition-[width] duration-500 ease-out"
              style={{ width: `${Math.min(Math.max(progress, 0), 100)}%` }}
            />
          </div>
        )}
      </div>
      {counter !== undefined && (
        <span className="shrink-0 text-sm font-semibold tabular-nums text-muted-foreground">{counter}</span>
      )}
    </div>
  )
}
