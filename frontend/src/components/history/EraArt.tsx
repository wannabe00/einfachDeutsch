import { useState } from "react"
import { Landmark } from "lucide-react"

import { cn } from "@/lib/utils"

/*
 * Hero artwork for a history article card (Phase 23.12).
 *
 * Same approach as `SourceArt` on Videos, and for the same reason: the prod CSP
 * only allows images from 'self', data:, images.unsplash.com and
 * res.cloudinary.com, so an arbitrary hotlinked photo is blocked in production —
 * and historical imagery is a copyright minefield unless it's public-domain or
 * royalty-free. So we DRAW the era when `image_url` is blank, and render the
 * image (with fallback) when the owner sets one to an asset they control.
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
  className,
}: {
  era: string
  imageUrl?: string
  title: string
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
        className={cn("size-full object-cover", className)}
      />
    )
  }

  const hue = hueFor(era)
  return (
    <div
      className={cn("flex size-full flex-col items-center justify-center gap-1.5", className)}
      style={{
        background: `linear-gradient(140deg, hsl(${hue} 45% 26%), hsl(${(hue + 35) % 360} 40% 14%))`,
      }}
      aria-hidden="true"
    >
      <Landmark className="size-6 text-white/45" />
      {era && (
        <span className="px-3 text-center text-[11px] font-semibold uppercase tracking-wider text-white/70">
          {era}
        </span>
      )}
    </div>
  )
}
