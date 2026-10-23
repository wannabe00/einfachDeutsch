import { useState, type ReactNode } from "react"

import { cn } from "@/lib/utils"
import { MUNICH_PHOTO } from "@/lib/photos"
import { Logo } from "@/components/layout/TopBar"

/*
 * Layout for the pages before the app: sign in, profile setup and level
 * onboarding. Desktop: the Munich photo on the left, the form on the right.
 * Phones: just the form, with the logo above it.
 */
export function AuthShell({
  children,
  maxWidth = "max-w-md",
}: {
  children: ReactNode
  maxWidth?: string
}) {
  return (
    <div className="min-h-screen bg-background lg:grid lg:grid-cols-[1.1fr_1fr]">
      <AuthPhoto />
      <div className="flex min-h-screen items-center justify-center px-4 py-10 sm:px-8">
        <div className={cn("w-full", maxWidth)}>{children}</div>
      </div>
    </div>
  )
}

function AuthPhoto() {
  const [ok, setOk] = useState(true)
  return (
    <div className="sticky top-0 hidden h-screen overflow-hidden bg-[#111] text-white lg:block">
      {ok && (
        <img
          src={MUNICH_PHOTO}
          alt="Munich's old town at sunset"
          onError={() => setOk(false)}
          className="absolute inset-0 size-full object-cover"
        />
      )}
      <div className="absolute inset-0 bg-gradient-to-t from-black/85 via-black/30 to-black/40" />
      <div className="relative flex h-full flex-col justify-between p-10">
        <Logo className="text-white" />
        <div className="max-w-md">
          <p className="text-[44px] font-extrabold leading-[1.05] tracking-[-0.03em]">
            Learn German, one short lesson a day.
          </p>
          <p className="mt-3 text-lg text-white/80">
            A guided path, flashcards that come back at the right time, and quick drills.
          </p>
        </div>
      </div>
    </div>
  )
}

/** The logo above the form on phones (the photo panel shows it on desktop). */
export function AuthWordmark() {
  return (
    <div className="flex justify-center lg:hidden">
      <Logo />
    </div>
  )
}
