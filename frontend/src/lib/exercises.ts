import type { PartContent } from "@/types"

/** Whether an answer is complete enough to submit.

    Kept out of ExerciseInput.tsx because a component file may only export
    components (React fast refresh). */
export function isAnswered(content: PartContent, value: unknown): boolean {
  if (content.type === "group") {
    const parts = content.payload.parts ?? []
    return Array.isArray(value) && parts.every((part, i) => isAnswered(part, value[i]))
  }
  if (content.type === "multiple_choice") return typeof value === "string" && !!value
  if (content.type === "error_spot") return typeof value === "number"
  if (content.type === "sentence_order") {
    return Array.isArray(value) && value.length === (content.payload.tokens?.length ?? 0)
  }
  if (content.type === "matching") {
    const map = value && typeof value === "object" && !Array.isArray(value) ? value : {}
    return (content.payload.left ?? []).every((l) => l in map)
  }
  if (content.type === "word_bank") {
    const gaps = (content.payload.text ?? "").split("___").length - 1
    return Array.isArray(value) && value.length === gaps && value.every((v) => !!v)
  }
  return typeof value === "string" && value.trim().length > 0
}
