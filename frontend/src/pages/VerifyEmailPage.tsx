import { useEffect, useState } from "react"
import { Link, useParams } from "react-router-dom"

import { verifyEmail } from "@/api/auth"
import { SITE_NAME } from "@/lib/site"

type Status = "verifying" | "success" | "error"

export default function VerifyEmailPage() {
  const { key } = useParams<{ key: string }>()
  const [status, setStatus] = useState<Status>(key ? "verifying" : "error")

  useEffect(() => {
    if (!key) return
    let active = true
    verifyEmail(key)
      .then(() => active && setStatus("success"))
      .catch(() => active && setStatus("error"))
    return () => {
      active = false
    }
  }, [key])

  return (
    <div className="flex min-h-screen items-center justify-center bg-background px-4">
      <div className="w-full max-w-sm text-center">
        <h1 className="text-2xl font-semibold tracking-tight">{SITE_NAME}</h1>
        <div className="mt-8 rounded-xl border border-border bg-surface p-6">
          {status === "verifying" && (
            <p className="text-sm text-muted-foreground">Verifying your email…</p>
          )}
          {status === "success" && (
            <>
              <h2 className="text-base font-semibold">Email verified</h2>
              <p className="mt-2 text-sm text-muted-foreground">
                Your account is now active. You can log in.
              </p>
              <Link
                to="/login"
                className="mt-4 inline-block text-sm font-medium text-accent hover:underline"
              >
                Go to log in
              </Link>
            </>
          )}
          {status === "error" && (
            <>
              <h2 className="text-base font-semibold">
                This link didn’t work
              </h2>
              <p className="mt-2 text-sm text-muted-foreground">
                The verification link is invalid or has expired. Try registering
                again or request a new link.
              </p>
              <Link
                to="/login"
                className="mt-4 inline-block text-sm font-medium text-accent hover:underline"
              >
                Back to log in
              </Link>
            </>
          )}
        </div>
      </div>
    </div>
  )
}
