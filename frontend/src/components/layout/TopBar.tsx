import { Link } from "react-router-dom"

import { useAuth } from "@/contexts/AuthContext"
import { SITE_NAME } from "@/lib/site"
import { Button } from "@/components/ui/button"
import { AccountMenu } from "./AccountMenu"

export function TopBar() {
  const { user } = useAuth()
  return (
    <header className="sticky top-0 z-30 flex h-14 shrink-0 items-center justify-between border-b border-border bg-surface px-4">
      <Link
        to="/"
        className="text-base font-semibold tracking-tight text-foreground"
      >
        {SITE_NAME}
      </Link>

      <div className="flex items-center gap-2">
        {user ? (
          <AccountMenu />
        ) : (
          <>
            <Button asChild variant="ghost" size="sm">
              <Link to="/login">Log in</Link>
            </Button>
            <Button asChild size="sm">
              <Link to="/register">Sign up</Link>
            </Button>
          </>
        )}
      </div>
    </header>
  )
}
