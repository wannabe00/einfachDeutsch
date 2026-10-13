import { useId } from "react"

import "./streak.css"

/*
 * The streak flame, drawn (not an emoji) and only earned: callers show it from
 * 3 days on. It flickers gently; reduced-motion users get a still flame.
 */
export function StreakFlame({ size = 48, className = "" }: { size?: number; className?: string }) {
  const id = useId()
  return (
    <svg
      width={size}
      height={size}
      viewBox="0 0 48 48"
      aria-hidden="true"
      className={`streak-flame ${className}`}
    >
      <defs>
        <linearGradient id={`${id}-outer`} x1="0" y1="1" x2="0" y2="0">
          <stop offset="0" stopColor="hsl(var(--primary))" />
          <stop offset="1" stopColor="hsl(var(--section-2))" />
        </linearGradient>
        <linearGradient id={`${id}-inner`} x1="0" y1="1" x2="0" y2="0">
          <stop offset="0" stopColor="hsl(var(--section-2))" />
          <stop offset="1" stopColor="hsl(48 100% 70%)" />
        </linearGradient>
      </defs>
      <path
        className="streak-flame-outer"
        fill={`url(#${id}-outer)`}
        d="M24 3c2 7 11 12 11 24a11 11 0 0 1-22 0c0-5 2.5-8.5 5-11 .4 3 1.8 5 3.8 6C21 15 21.5 9 24 3z"
      />
      <path
        className="streak-flame-inner"
        fill={`url(#${id}-inner)`}
        d="M24 21c1 4 6 6.5 6 12a6 6 0 0 1-12 0c0-3 1.4-5 3-6.4.3 1.8 1 2.8 2 3.4-.2-3.4.2-6 1-9z"
      />
    </svg>
  )
}
