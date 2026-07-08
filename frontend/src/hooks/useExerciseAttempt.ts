import { useState } from "react"
import { useMutation } from "@tanstack/react-query"

import { attemptExercise, type UserAnswer } from "@/api/exercises"
import { aiCheckAnswer } from "@/api/ai"
import { useGuestLimit } from "@/contexts/GuestLimitContext"
import type { AttemptResult, Exercise } from "@/types"

const SIMPLE_TYPES = ["translation", "fill_blank", "article", "conjugation", "free_text"]

function answerReady(ans: UserAnswer): boolean {
  if (typeof ans === "string") return ans.trim().length > 0
  if (Array.isArray(ans)) return ans.length > 0
  return Object.keys(ans).length > 0
}

/**
 * Answer state + grading for one exercise. Holds whichever answer shape the
 * type needs (text / list / map), submits it, and — for simple text types —
 * fetches optional AI tutor feedback. The card just renders the returned state.
 */
export function useExerciseAttempt(exercise: Exercise) {
  const isSimple = SIMPLE_TYPES.includes(exercise.exercise_type)
  const [text, setText] = useState("")
  const [list, setList] = useState<string[]>([])
  const [map, setMap] = useState<Record<string, string>>({})
  const [selectedLeft, setSelectedLeft] = useState<string | null>(null)
  const [result, setResult] = useState<AttemptResult | null>(null)
  const [aiFeedback, setAiFeedback] = useState("")
  const { guard } = useGuestLimit()

  function currentAnswer(): UserAnswer {
    switch (exercise.exercise_type) {
      case "sentence_order":
      case "word_bank":
        return list
      case "matching":
        return map
      default:
        return text
    }
  }

  const aiMutation = useMutation({
    mutationFn: (correctAnswer: string) =>
      aiCheckAnswer(exercise.prompt, correctAnswer, text || JSON.stringify(currentAnswer())),
    onSuccess: setAiFeedback,
  })

  const mutation = useMutation({
    mutationFn: () => attemptExercise(exercise.id, currentAnswer()),
    onSuccess: (data) => {
      setResult(data)
      // Only ask the AI tutor for simple, text-based exercises.
      if (isSimple && typeof data.correct_answer === "string") {
        aiMutation.mutate(data.correct_answer)
      }
    },
  })

  function submit() {
    if (result || !answerReady(currentAnswer())) return
    if (!guard()) return // guests: blocked once the daily free cap is hit
    mutation.mutate()
  }

  return {
    isSimple,
    text,
    setText,
    list,
    setList,
    map,
    setMap,
    selectedLeft,
    setSelectedLeft,
    result,
    aiFeedback,
    aiPending: aiMutation.isPending,
    submitting: mutation.isPending,
    submit,
  }
}
