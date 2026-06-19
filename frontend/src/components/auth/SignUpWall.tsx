import { Link } from "react-router-dom"
import { Sparkles } from "lucide-react"

import { Button } from "@/components/ui/button"

interface SignUpWallProps {
  open: boolean
  onClose: () => void
}

/** Modal shown when a guest exhausts their daily free actions. */
export function SignUpWall({ open, onClose }: SignUpWallProps) {
  if (!open) return null
  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/50 px-4">
      <div className="w-full max-w-sm rounded-xl border border-border bg-surface p-6 text-center shadow-xl">
        <div className="mx-auto flex size-12 items-center justify-center rounded-full bg-accent/10 text-accent">
          <Sparkles className="size-6" />
        </div>
        <h2 className="mt-4 text-lg font-semibold">That’s your free practice for today</h2>
        <p className="mt-2 text-sm text-muted-foreground">
          Create a free account to keep going without limits — and to save your
          progress so words come back at the right time.
        </p>
        <div className="mt-5 flex flex-col gap-2">
          <Button asChild>
            <Link to="/register">Create a free account</Link>
          </Button>
          <Button asChild variant="outline">
            <Link to="/login">Log in</Link>
          </Button>
          <button
            onClick={onClose}
            className="mt-1 text-xs text-muted-foreground hover:text-foreground"
          >
            Maybe later
          </button>
        </div>
      </div>
    </div>
  )
}
