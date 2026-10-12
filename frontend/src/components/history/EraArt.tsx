import { useState } from "react"
import { Landmark } from "lucide-react"

import { cn } from "@/lib/utils"

/*
 * Artwork for a history article card. Works like `SourceArt` on Videos, for the
 * same reasons: the production CSP only allows images from 'self', data:,
 * images.unsplash.com and res.cloudinary.com, and historical photos are often
 * under copyright. So when `image_url` is blank we draw a tile for the era, and
 * when it's set (to an image the owner controls) we show it with a fallback.
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
