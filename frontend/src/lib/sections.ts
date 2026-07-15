/* Per-unit "section" accent colours for the Design v3 path (Phase 23). Units
   cycle through 6 curated accents so the path reads as colourful Duolingo-style
   sections. A Unit's `accent_color` (from the backend) can override this; when
   blank, pick by the unit's index. */

export const SECTION_COUNT = 6

/** The CSS custom property name for a section accent, e.g. "--section-3". */
export function sectionVar(index: number): string {
  return `--section-${(((index % SECTION_COUNT) + SECTION_COUNT) % SECTION_COUNT) + 1}`
}

/** A ready-to-use CSS colour for a section accent, e.g. "hsl(var(--section-3))". */
export function sectionColor(index: number): string {
  return `hsl(var(${sectionVar(index)}))`
}

/** Resolve a unit's accent: an explicit backend value, else the cycled section
    colour. An explicit value may be a raw CSS colour or a token name. */
export function resolveAccent(explicit: string | undefined, index: number): string {
  if (!explicit) return sectionColor(index)
  if (explicit.startsWith("--")) return `hsl(var(${explicit}))`
  return explicit
}
