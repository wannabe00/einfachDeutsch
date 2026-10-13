import { Link } from "react-router-dom"
import { ChevronLeft } from "lucide-react"

const CLS =
  "inline-flex min-h-[44px] w-fit items-center gap-0.5 font-medium text-primary hover:underline"

/** iOS-style "‹ Back" link: to a route, or a button when `onClick` is given. */
export function BackLink({ to, onClick, label }: { to?: string; onClick?: () => void; label: string }) {
  const body = (
    <>
      <ChevronLeft className="size-5" aria-hidden="true" /> {label}
    </>
  )
  if (onClick || !to) {
    return (
      <button onClick={onClick} className={CLS}>
        {body}
      </button>
    )
  }
  return (
    <Link to={to} className={CLS}>
      {body}
    </Link>
  )
}
