import { isAxiosError } from "axios"

/** Pull a human-readable message out of a DRF error response body. */
export function errorText(e: unknown): string {
  if (isAxiosError(e) && e.response?.data) {
    const d = e.response.data as Record<string, unknown>
    const first = Object.values(d)[0]
    if (Array.isArray(first)) return String(first[0])
    if (typeof first === "string") return first
  }
  return "Something went wrong."
}
