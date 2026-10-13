import { useState } from "react"

import { cn } from "@/lib/utils"

/*
 * Artwork for a video suggestion. If the suggestion has an `image_url` we show
 * it; otherwise we draw a tile for the platform instead of fetching a logo,
 * because:
 *   - the production CSP only allows images from 'self', data:,
 *     images.unsplash.com and res.cloudinary.com, so hotlinked logos break;
 *   - channel logos belong to their owners, and their URLs change.
 * Set `image_url` to a Cloudinary image you control to override the tile.
 */

/** Deterministic hue per platform, so a source always looks the same. */
function hueFor(platform: string): number {
  let hash = 0
  for (const ch of platform || "?") hash = (hash * 31 + ch.charCodeAt(0)) % 360
  return hash
}

function initials(platform: string): string {
  const trimmed = (platform || "").trim()
  if (!trimmed) return "?"
  // "DW" / "ZDF" are already initialisms; otherwise take the first two letters.
  if (trimmed.length <= 3) return trimmed.toUpperCase()
  return trimmed.slice(0, 2).toUpperCase()
}

export function SourceArt({
  platform,
  imageUrl,
  title,
  className,
}: {
  platform: string
  imageUrl?: string
  title: string
  className?: string
}) {
  const [failed, setFailed] = useState(false)
  const showImage = !!imageUrl && !failed

  if (showImage) {
    return (
      <img
        src={imageUrl}
        alt={`${title} on ${platform}`}
        loading="lazy"
        onError={() => setFailed(true)}
        className={cn("size-full object-cover", className)}
      />
    )
  }

  const hue = hueFor(platform)
  return (
    <div
      className={cn("flex size-full flex-col items-center justify-center gap-1", className)}
      style={{ background: `hsl(${hue} 35% 20%)` }}
      aria-hidden="true"
    >
      <span className="text-2xl font-bold tracking-wide text-white/90">{initials(platform)}</span>
      <span className="text-xs text-white/60">{platform}</span>
    </div>
  )
}
