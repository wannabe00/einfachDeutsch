import { useState, type FormEvent } from "react"
import { Link, useParams } from "react-router-dom"
import { useMutation } from "@tanstack/react-query"
import { CheckCircle2 } from "lucide-react"

import { confirmPasswordReset, requestPasswordReset } from "@/api/auth"
import { errorText } from "@/lib/apiError"
import { AUTH_CARD } from "@/lib/authCard"
import { AuthShell, AuthWordmark } from "@/components/auth/AuthShell"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"

/*
 * Password reset, before sign-in: ask for an e-mail link, then choose a new
 * password from that link (/reset-password/:uid/:token). The server never says
 * whether an address has an account, so the first page always "succeeds".
 */

export function ForgotPasswordPage() {
  const [email, setEmail] = useState("")
  const send = useMutation({ mutationFn: () => requestPasswordReset(email.trim()) })

  function submit(e: FormEvent) {
    e.preventDefault()
    if (email.trim() && !send.isPending) send.mutate()
  }

  return (
    <Shell title="Forgot your password?" subtitle="We'll e-mail you a link to choose a new one.">
      {send.isSuccess ? (
        <Done>
          If an account uses <strong>{email.trim()}</strong>, a reset link is on its way. Check your
          inbox (and spam). The link works once.
        </Done>
      ) : (
        <form onSubmit={submit} className="flex flex-col gap-3">
          <Input
            type="email"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
            placeholder="E-mail address"
            aria-label="E-mail address"
            autoComplete="email"
            required
          />
          {send.isError && <ErrorNote>{errorText(send.error)}</ErrorNote>}
          <Button type="submit" size="lg" disabled={send.isPending}>
            {send.isPending ? "Sending…" : "Send reset link"}
          </Button>
        </form>
      )}
    </Shell>
  )
}

export function ResetPasswordPage() {
  const { uid = "", token = "" } = useParams()
  const [password, setPassword] = useState("")
  const [repeat, setRepeat] = useState("")
  const save = useMutation({ mutationFn: () => confirmPasswordReset(uid, token, password, repeat) })

  function submit(e: FormEvent) {
    e.preventDefault()
    if (!save.isPending) save.mutate()
  }

  return (
    <Shell title="Choose a new password" subtitle="At least 8 characters, not only numbers.">
      {save.isSuccess ? (
        <Done>Your password is changed. You were signed out on all devices; log in with the new one.</Done>
      ) : (
        <form onSubmit={submit} className="flex flex-col gap-3">
          <Input
            type="password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            placeholder="New password"
            aria-label="New password"
            autoComplete="new-password"
            required
          />
          <Input
            type="password"
            value={repeat}
            onChange={(e) => setRepeat(e.target.value)}
            placeholder="Repeat new password"
            aria-label="Repeat new password"
            autoComplete="new-password"
            required
          />
          {save.isError && (
            <ErrorNote>
              {errorText(save.error)} If the link is old or was already used,{" "}
              <Link to="/forgot-password" className="font-semibold underline">
                ask for a new one
              </Link>
              .
            </ErrorNote>
          )}
          <Button type="submit" size="lg" disabled={save.isPending}>
            {save.isPending ? "Saving…" : "Save new password"}
          </Button>
        </form>
      )}
    </Shell>
  )
}

function Shell({ title, subtitle, children }: { title: string; subtitle: string; children: React.ReactNode }) {
  return (
    <AuthShell maxWidth="max-w-sm">
      <div>
        <AuthWordmark />
        <h1 className="mt-6 text-center text-3xl font-extrabold lg:mt-0 lg:text-left">{title}</h1>
        <p className="mt-1 text-center text-muted-foreground lg:text-left">{subtitle}</p>
        <div className={`mt-8 ${AUTH_CARD}`}>{children}</div>
        <p className="mt-5 text-center text-sm">
          <Link to="/login" className="font-semibold text-primary hover:underline">
            Back to log in
          </Link>
        </p>
      </div>
    </AuthShell>
  )
}

function Done({ children }: { children: React.ReactNode }) {
  return (
    <p className="flex gap-3 text-[15px]" role="status">
      <CheckCircle2 className="mt-0.5 size-5 shrink-0 text-[hsl(var(--success))]" aria-hidden="true" />
      <span>
        {children}{" "}
        <Link to="/login" className="font-semibold text-primary hover:underline">
          Log in
        </Link>
      </span>
    </p>
  )
}

function ErrorNote({ children }: { children: React.ReactNode }) {
  return (
    <p className="rounded-xl bg-danger-bg px-3.5 py-2.5 text-sm font-medium text-danger" role="alert">
      {children}
    </p>
  )
}
