import type { ExerciseContent } from "@/types"

/** Whether an answer is complete enough to submit (Phase 23.5/23.14).

    Lives outside the component file so Fast Refresh keeps working — that file
    may only export components. */
export function isAnswered(content: ExerciseContent, value: unknown): boolean {
  if (content.type === "multiple_choice") return typeof value === "string" && !!value
  if (content.type === "sentence_order") {
    return Array.isArray(value) && value.length === (content.payload.tokens?.length ?? 0)
  }
  return typeof value === "string" && value.trim().length > 0
}
