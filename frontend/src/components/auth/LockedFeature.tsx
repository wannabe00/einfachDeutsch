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
      <div className="w-full max-w-sm rounded-[28px] bg-surface p-8 text-center shadow-lift">
        <h2 className="text-2xl font-extrabold">{title}</h2>
        <p className="mt-2 text-muted-foreground">{description}</p>
        <Button asChild size="lg" className="mt-6 w-full">
          <Link to="/login">Sign in or create an account</Link>
        </Button>
      </div>
    </div>
  )
}
