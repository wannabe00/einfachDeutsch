import { isAxiosError } from "axios"

/** Pull a human-readable message out of a DRF error response body. */
export function errorText(e: unknown): string {
  const data = isAxiosError(e) ? e.response?.data : undefined
  // Only a JSON object holds a message; a server error page is an HTML string.
  if (data && typeof data === "object") {
    const first = Object.values(data as Record<string, unknown>)[0]
    const text = Array.isArray(first) ? String(first[0] ?? "") : typeof first === "string" ? first : ""
    if (text.trim()) return text
  }
  return "Something went wrong. Please try again."
}
