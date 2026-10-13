import { useState } from "react"

import { cn } from "@/lib/utils"

/*
 * The picture for a history lesson. The pictures are public-domain images
 * bundled with the app (`public/history/`), which keeps the CSP strict. When a
 * lesson has none, or it fails to load, a plain tile names the era instead.
 */

/** Deterministic hue per era, so an era always looks the same. */
function hueFor(era: string): number {
  let hash = 0
  for (const ch of era || "?") hash = (hash * 31 + ch.charCodeAt(0)) % 360
  return hash
}

export function EraArt({
  era,
  imageUrl,
  title,
  fit = "cover",
  className,
}: {
  era: string
  imageUrl?: string
  title: string
  /** "cover" fills a card (cropped near the top); "contain" shows it whole. */
  fit?: "cover" | "contain"
  className?: string
}) {
  const [failed, setFailed] = useState(false)

  if (imageUrl && !failed) {
    return (
      <img
        src={imageUrl}
        alt={title}
        loading="lazy"
        onError={() => setFailed(true)}
        className={cn(
          "size-full",
          fit === "cover" ? "object-cover object-[50%_25%]" : "object-contain",
          className,
        )}
      />
    )
  }

  const hue = hueFor(era)
  return (
    <div
      className={cn("flex size-full flex-col items-center justify-center gap-1.5", className)}
      style={{ background: `hsl(${hue} 30% 20%)` }}
      aria-hidden="true"
    >
      {era && (
        <span className="px-3 text-center text-[11px] font-semibold uppercase tracking-wider text-white/70">
          {era}
        </span>
      )}
    </div>
  )
}
