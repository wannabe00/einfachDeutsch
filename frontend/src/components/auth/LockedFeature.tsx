import type { ReactNode } from "react"
import { Link } from "react-router-dom"
import { Lock } from "lucide-react"

import { Button } from "@/components/ui/button"

interface LockedFeatureProps {
  /** What's behind the lock — rendered blurred and non-interactive. */
  children?: ReactNode
  title?: string
  description?: string
}

/**
 * Renders gated content blurred behind a "log in to use" overlay (instead of
 * redirecting). Used for account-only sections so guests can see what they're
 * missing.
 */
export function LockedFeature({
  children,
  title = "Members only",
  description = "Create a free account to use this feature.",
}: LockedFeatureProps) {
  return (
    <div className="relative min-h-[60vh]">
      {children && (
        <div
          aria-hidden
          className="pointer-events-none select-none blur-sm opacity-50"
        >
          {children}
        </div>
      )}
      <div className="absolute inset-0 flex items-center justify-center p-4">
        <div className="w-full max-w-sm rounded-xl border border-border bg-surface/95 p-6 text-center shadow-xl backdrop-blur">
          <div className="mx-auto flex size-12 items-center justify-center rounded-full bg-accent/10 text-accent">
            <Lock className="size-6" />
          </div>
          <h2 className="mt-4 text-lg font-semibold">{title}</h2>
          <p className="mt-2 text-sm text-muted-foreground">{description}</p>
          <div className="mt-5 flex flex-col gap-2">
            <Button asChild>
              <Link to="/register">Create a free account</Link>
            </Button>
            <Button asChild variant="outline">
              <Link to="/login">Log in</Link>
            </Button>
          </div>
        </div>
      </div>
    </div>
  )
}
