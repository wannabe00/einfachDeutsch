import { useState } from "react"
import { Tv } from "lucide-react"

import { cn } from "@/lib/utils"

/*
 * Artwork for a watch suggestion (Phase 23.11).
 *
 * If the suggestion has an `image_url` we show it; otherwise we DRAW the source
 * rather than fetching a logo. That's deliberate:
 *   - the prod CSP only allows images from 'self', data:, images.unsplash.com
 *     and res.cloudinary.com, so a hotlinked channel logo is blocked in prod;
 *   - channel logos belong to their owners, and their URLs rot.
 * A generated tile is stable, free, and always on-brand. Set `image_url` to a
 * Cloudinary asset you control to override it.
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
        alt={`${title} — ${platform}`}
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
      style={{
        background: `linear-gradient(140deg, hsl(${hue} 60% 28%), hsl(${(hue + 40) % 360} 55% 16%))`,
      }}
      aria-hidden="true"
    >
      <Tv className="size-5 text-white/50" />
      <span className="text-sm font-bold tracking-wide text-white/90">{initials(platform)}</span>
    </div>
  )
}
