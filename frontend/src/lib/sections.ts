/* Path units cycle through six accent colours (`--section-1` … `--section-6`).
   A unit's `accent_color` from the backend wins when set. */

const SECTION_COUNT = 6

function sectionColor(index: number): string {
  const n = (((index % SECTION_COUNT) + SECTION_COUNT) % SECTION_COUNT) + 1
  return `hsl(var(--section-${n}))`
}

/** A unit's accent: the backend value (a CSS colour or a `--token` name), or
    the cycled section colour when blank. */
export function resolveAccent(explicit: string | undefined, index: number): string {
  if (!explicit) return sectionColor(index)
  if (explicit.startsWith("--")) return `hsl(var(${explicit}))`
  return explicit
}
