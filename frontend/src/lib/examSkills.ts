import { FileText, Headphones, type LucideIcon } from "lucide-react"

import {
  answerHoerenTeil,
  answerLesenTeil,
  fetchHoerenSet,
  fetchHoerenSets,
  fetchLesenSet,
  fetchLesenSets,
} from "@/api/curriculum"
import type { LesenAnswerResult, LesenSet, LesenSetDetail } from "@/types"

/** The exam sections that share the multiple-choice set pages (Lesen, Hören). */
export type QuizSkill = "lesen" | "hoeren"

export const QUIZ_SKILLS: Record<
  QuizSkill,
  {
    title: string
    path: string
    /** For screen readers and messages ("reading", "listening"). */
    label: string
    icon: LucideIcon
    subtitle: string
    retry: string
    fetchSets: () => Promise<LesenSet[]>
    fetchSet: (level: string, modul: number) => Promise<LesenSetDetail>
    answer: (exerciseId: number, answer: unknown) => Promise<LesenAnswerResult>
  }
> = {
  lesen: {
    title: "Lesen",
    path: "/lesen",
    label: "reading",
    icon: FileText,
    subtitle: "Reading like the Goethe exam: one set after every Modul. 60 % passes.",
    retry: "Read the texts again and retry.",
    fetchSets: fetchLesenSets,
    fetchSet: fetchLesenSet,
    answer: answerLesenTeil,
  },
  hoeren: {
    title: "Hören",
    path: "/hoeren",
    label: "listening",
    icon: Headphones,
    subtitle:
      "Listening like the Goethe exam: each recording plays once or twice, as in the exam. After checking, replay it and read the transcript.",
    retry: "Listen again and retry.",
    fetchSets: fetchHoerenSets,
    fetchSet: fetchHoerenSet,
    answer: answerHoerenTeil,
  },
}
