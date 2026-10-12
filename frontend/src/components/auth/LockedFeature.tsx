import { Link } from "react-router-dom"

import { Button } from "@/components/ui/button"

/** Shown in place of an account-only page when nobody is signed in. */
export function LockedFeature({
  title = "You need an account for this",
  description = "Accounts are free. Sign in with Google or GitHub to keep your progress.",
}: {
  title?: string
  description?: string
}) {
  return (
    <div className="flex min-h-[60vh] items-center justify-center p-4">
      <div className="w-full max-w-sm rounded-xl border border-border bg-surface p-6 text-center">
        <h2 className="text-lg font-semibold">{title}</h2>
        <p className="mt-2 text-sm text-muted-foreground">{description}</p>
        <Button asChild className="mt-5 w-full">
          <Link to="/login">Sign in or create an account</Link>
        </Button>
      </div>
    </div>
  )
}
