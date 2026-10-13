/** The unit colour for a Lektion, cycled through the six `--section-*` tokens. */
export function lektionColor(order: number): string {
  return `hsl(var(--section-${((((order - 1) % 6) + 6) % 6) + 1}))`
}
