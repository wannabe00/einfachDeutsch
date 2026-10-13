import {
  BedDouble,
  BookOpen,
  Briefcase,
  Building2,
  Cake,
  Clock,
  CloudSun,
  Guitar,
  Hand,
  House,
  Laptop,
  Mic,
  NotebookPen,
  Palette,
  PartyPopper,
  Shirt,
  Signpost,
  Smile,
  Sofa,
  Stethoscope,
  TrafficCone,
  TramFront,
  Users,
  UtensilsCrossed,
  WashingMachine,
  type LucideIcon,
} from "lucide-react"

import { lektionColor } from "./lektionColor"

/*
 * A generated cover for a Lektion: its unit colour, a large icon for the topic
 * and one German word from it. No photos, so the picture always matches what
 * the Lektion teaches. Only A1 is mapped so far; other levels get a book icon.
 */
const A1: Record<number, [LucideIcon, string]> = {
  1: [Hand, "Hallo!"],
  2: [Briefcase, "der Beruf"],
  3: [Users, "die Familie"],
  4: [Sofa, "das Sofa"],
  5: [Palette, "die Farbe"],
  6: [Laptop, "das Büro"],
  7: [Guitar, "das Hobby"],
  8: [Clock, "die Uhrzeit"],
  9: [UtensilsCrossed, "das Essen"],
  10: [TramFront, "die U-Bahn"],
  11: [NotebookPen, "gemacht"],
  12: [PartyPopper, "das Fest"],
  13: [Signpost, "der Weg"],
  14: [House, "das Haus"],
  15: [Building2, "das Viertel"],
  16: [BedDouble, "das Hotel"],
  17: [Mic, "der Wunsch"],
  18: [Stethoscope, "der Tee"],
  19: [Smile, "der Bauch"],
  20: [WashingMachine, "der Haushalt"],
  21: [TrafficCone, "die Ampel"],
  22: [Shirt, "die Schuhe"],
  23: [CloudSun, "das Wetter"],
  24: [Cake, "feiern"],
}

export function LektionCover({
  order,
  level,
  size = "lg",
  className = "",
}: {
  order: number
  level: string
  /** "sm" for list thumbnails: smaller icons, no word. */
  size?: "sm" | "lg"
  className?: string
}) {
  const sm = size === "sm"
  const [Icon, word] = (level === "A1" && A1[order]) || [BookOpen, ""]
  const color = lektionColor(order)

  return (
    <div
      aria-hidden="true"
      className={`relative overflow-hidden ${className}`}
      style={{ background: `linear-gradient(145deg, ${color}, color-mix(in srgb, ${color} 55%, black))` }}
    >
      <Icon
        className={
          sm
            ? "absolute -bottom-2 -right-3 size-14 text-white/25"
            : "absolute -bottom-4 -right-4 size-32 text-white/25"
        }
        strokeWidth={1.5}
      />
      <Icon
        className={sm ? "absolute left-2.5 top-2.5 size-6 text-white" : "absolute left-4 top-4 size-9 text-white"}
        strokeWidth={2}
      />
      {word && !sm && (
        <span className="absolute bottom-3 left-4 rounded-full bg-black/25 px-2.5 py-1 text-xs font-semibold text-white backdrop-blur-sm">
          {word}
        </span>
      )}
    </div>
  )
}
