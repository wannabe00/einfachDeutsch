import { useState, type FormEvent, type ReactNode } from "react"
import { X } from "lucide-react"

import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import { errorText } from "@/lib/apiError"
import { Msg } from "./primitives"

/*
 * Confirms a sensitive action with the account password, asked only after the
 * button was pressed. `onConfirm` gets the password and throws (an API error)
 * when it fails; the message is shown and the dialog stays open.
 */
export function PasswordDialog({
  title,
  description,
  confirmLabel,
  danger,
  onConfirm,
  onClose,
  children,
}: {
  title: string
  description: string
  confirmLabel: string
  danger?: boolean
  onConfirm: (password: string) => Promise<void>
  onClose: () => void
  children?: ReactNode
}) {
  const [password, setPassword] = useState("")
  const [error, setError] = useState("")
  const [busy, setBusy] = useState(false)

  async function submit(e: FormEvent) {
    e.preventDefault()
    if (!password || busy) return
    setBusy(true)
    setError("")
    try {
      await onConfirm(password)
    } catch (err) {
      setError(errorText(err))
      setBusy(false)
    }
  }

  return (
    <div
      className="fixed inset-0 z-50 flex items-end justify-center sm:items-center"
      role="dialog"
      aria-modal="true"
      aria-labelledby="password-dialog-title"
      onKeyDown={(e) => e.key === "Escape" && onClose()}
    >
      <div className="absolute inset-0 bg-black/40 animate-in fade-in-0 duration-150" onClick={onClose} aria-hidden="true" />
      <form
        onSubmit={submit}
        className="relative flex w-full max-w-md flex-col gap-4 rounded-t-[24px] bg-surface p-5 shadow-card animate-in slide-in-from-bottom-8 duration-200 sm:rounded-[24px] sm:p-6"
      >
        <div className="flex items-start justify-between gap-3">
          <div>
            <h2 id="password-dialog-title" className="text-xl font-bold">{title}</h2>
            <p className="mt-1 text-sm text-muted-foreground">{description}</p>
          </div>
          <Button type="button" variant="secondary" size="icon" aria-label="Close" onClick={onClose}>
            <X />
          </Button>
        </div>
        {children}
        <Input
          type="password"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
          placeholder="Your password"
          aria-label="Your password"
          autoComplete="current-password"
          autoFocus
        />
        {error && <Msg tone="danger">{error}</Msg>}
        <div className="flex flex-wrap justify-end gap-2">
          <Button type="button" variant="outline" onClick={onClose}>
            Cancel
          </Button>
          <Button type="submit" variant={danger ? "destructive" : "default"} disabled={!password || busy}>
            {busy ? "Working…" : confirmLabel}
          </Button>
        </div>
      </form>
    </div>
  )
}
