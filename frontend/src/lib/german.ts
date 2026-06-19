/** Helpers for parsing German words. */

const ARTICLES = ["der", "die", "das"]

export function splitArticle(german: string): {
  article: string | null
  noun: string
} {
  const parts = german.trim().split(/\s+/)
  const first = parts[0]?.toLowerCase()
  if (ARTICLES.includes(first)) {
    return { article: first, noun: parts.slice(1).join(" ") }
  }
  return { article: null, noun: german.trim() }
}

export function normalize(s: string): string {
  return s.trim().toLowerCase().replace(/\s+/g, " ")
}

export function shuffle<T>(arr: T[]): T[] {
  const a = [...arr]
  for (let i = a.length - 1; i > 0; i--) {
    const j = Math.floor(Math.random() * (i + 1))
    ;[a[i], a[j]] = [a[j], a[i]]
  }
  return a
}
