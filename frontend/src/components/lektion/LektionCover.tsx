import {
  Baby,
  BedDouble,
  Bike,
  BookOpen,
  Briefcase,
  Building2,
  Cake,
  ChefHat,
  Church,
  Clock,
  CloudSun,
  ConciergeBell,
  Croissant,
  Drama,
  Dumbbell,
  Factory,
  GraduationCap,
  Guitar,
  Hand,
  HeartPulse,
  House,
  IdCard,
  Lamp,
  Languages,
  Laptop,
  Library,
  Map,
  Mic,
  NotebookPen,
  Package,
  Palette,
  PartyPopper,
  Plane,
  Salad,
  Shirt,
  ShoppingBasket,
  Signpost,
  Smile,
  Sofa,
  Stethoscope,
  Sun,
  Ticket,
  TrafficCone,
  TramFront,
  Trees,
  Tv,
  Users,
  UtensilsCrossed,
  WashingMachine,
  type LucideIcon,
} from "lucide-react"

import { lektionColor } from "./lektionColor"

/*
 * A generated cover for a Lektion: its unit colour, a large icon for the topic
 * and one German word from it. No photos, so the picture always matches what
 * the Lektion teaches. A1 and A2 are mapped; other levels get a book icon.
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

const A2: Record<number, [LucideIcon, string]> = {
  1: [Croissant, "der Bäcker"],
  2: [Lamp, "die Kommode"],
  3: [Trees, "die Ruhe"],
  4: [ShoppingBasket, "das Kilo"],
  5: [Church, "der Dom"],
  6: [Ticket, "das Konzert"],
  7: [Dumbbell, "joggen"],
  8: [HeartPulse, "das Herz"],
  9: [Factory, "die Firma"],
  10: [ChefHat, "reserviert"],
  11: [Baby, "die Freude"],
  12: [Salad, "der Salat"],
  13: [Languages, "die Sprache"],
  14: [Package, "das Päckchen"],
  15: [Tv, "die Sendung"],
  16: [ConciergeBell, "die Rezeption"],
  17: [Map, "die Reise"],
  18: [Sun, "die Wärme"],
  19: [Drama, "die Kultur"],
  20: [Library, "das Buch"],
  21: [IdCard, "der Ausweis"],
  22: [Bike, "die Mobilität"],
  23: [GraduationCap, "der Beruf"],
  24: [Plane, "das Ausland"],
}

const LEVELS: Record<string, Record<number, [LucideIcon, string]>> = { A1, A2 }

export function LektionCover({
  order,
  level,
  size = "lg",
  className = "",
}: {
  order: number
  level: string
  /** "sm" for list thumbnails: a smaller icon, no word. */
  size?: "sm" | "lg"
  className?: string
}) {
  const sm = size === "sm"
  const [Icon, word] = LEVELS[level]?.[order] ?? [BookOpen, ""]
  const color = lektionColor(order)

  return (
    <div
      aria-hidden="true"
      className={`relative overflow-hidden ${className}`}
      style={{ background: `linear-gradient(145deg, ${color}, color-mix(in srgb, ${color} 55%, black))` }}
    >
      <Icon
        className={`absolute left-1/2 top-1/2 -translate-x-1/2 -translate-y-1/2 text-white ${sm ? "h-1/2 w-1/2" : "size-16"}`}
        strokeWidth={sm ? 2 : 1.75}
      />
      {word && !sm && (
        <span className="absolute bottom-3 left-4 rounded-full bg-black/25 px-2.5 py-1 text-xs font-semibold text-white backdrop-blur-sm">
          {word}
        </span>
      )}
    </div>
  )
}
