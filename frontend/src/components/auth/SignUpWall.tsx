import { Link } from "react-router-dom"

import { Button } from "@/components/ui/button"

interface SignUpWallProps {
  open: boolean
  onClose: () => void
}

/** Modal shown when a guest uses up their free actions for the day. */
export function SignUpWall({ open, onClose }: SignUpWallProps) {
  if (!open) return null
  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/60 px-4">
      <div className="w-full max-w-sm rounded-xl border border-border bg-surface p-6 text-center">
        <h2 className="text-lg font-semibold">That’s your free practice for today</h2>
        <p className="mt-2 text-sm text-muted-foreground">
          With a free account there’s no daily limit, and your progress is saved so
          words come back for review at the right time.
        </p>
        <Button asChild className="mt-5 w-full">
          <Link to="/login">Sign in or create an account</Link>
        </Button>
        <button
          onClick={onClose}
          className="mt-3 text-sm text-muted-foreground hover:text-foreground"
        >
          Not now
        </button>
      </div>
    </div>
  )
}
