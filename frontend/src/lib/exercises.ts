import type { ExerciseContent } from "@/types"

/** Whether an answer is complete enough to submit.

    Kept out of ExerciseInput.tsx because a component file may only export
    components (React fast refresh). */
export function isAnswered(content: ExerciseContent, value: unknown): boolean {
  if (content.type === "multiple_choice") return typeof value === "string" && !!value
  if (content.type === "sentence_order") {
    return Array.isArray(value) && value.length === (content.payload.tokens?.length ?? 0)
  }
  return typeof value === "string" && value.trim().length > 0
}
