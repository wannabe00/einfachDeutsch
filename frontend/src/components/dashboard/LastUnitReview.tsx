import { useQuery } from "@tanstack/react-query"

import { fetchLastUnitReview } from "@/api/vocabulary"
import { NextUp } from "@/components/path/NextUp"

/*
 * "Review last unit" on the Dashboard: a short flashcard session over the words
 * of the unit finished most recently. Renders nothing until a unit is done.
 */
export function LastUnitReview() {
  const { data } = useQuery({ queryKey: ["last-unit"], queryFn: fetchLastUnitReview })
  if (!data?.unit || data.words.length === 0) return null

  const count = data.words.length
  return (
    <NextUp
      kicker="Review last unit"
      title={`Lektion ${data.unit.order}: ${data.unit.title}`}
      subtitle={`${count} ${count === 1 ? "word" : "words"}`}
      href="/review?scope=last-unit"
    />
  )
}
