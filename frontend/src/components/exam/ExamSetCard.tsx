import type { ReactNode } from "react"
import { Link } from "react-router-dom"
import { Lock, type LucideIcon } from "lucide-react"

import { cn } from "@/lib/utils"

/** One Modul's set on the Lesen and Schreiben pages: locked until its Lektionen are done. */
export function ExamSetCard({
  to,
  icon: Icon,
  label,
  modul,
  first,
  last,
  locked,
  status,
}: {
  to: string
  icon: LucideIcon
  /** What the set is, for screen readers ("reading", "writing"). */
  label: string
  modul: number
  first: number
  last: number
  locked: boolean
  status: ReactNode
}) {
  const body = (
    <>
      <span
        className={cn(
          "mb-1 flex size-10 items-center justify-center rounded-xl",
          locked ? "bg-surface-2 text-muted-foreground" : "bg-primary text-primary-foreground",
        )}
      >
        {locked ? <Lock className="size-5" aria-hidden="true" /> : <Icon className="size-5" aria-hidden="true" />}
      </span>
      <span className="font-semibold">Modul {modul}</span>
      <span className="text-sm text-muted-foreground">
        Lektionen {first}–{last}
      </span>
      <span className={cn("mt-1 text-sm font-semibold", locked ? "text-muted-foreground" : "text-foreground")}>
        {locked ? `After Lektion ${last}` : status}
      </span>
    </>
  )
  const card = "flex h-full w-full flex-col items-start gap-1 rounded-[20px] bg-surface p-4 text-left shadow-card"
  if (locked) {
    return (
      <div className={cn(card, "opacity-70")} aria-label={`Modul ${modul} ${label}, locked until Lektion ${last}`}>
        {body}
      </div>
    )
  }
  return (
    <Link to={to} className={cn(card, "transition-colors hover:bg-surface-2")}>
      {body}
    </Link>
  )
}
