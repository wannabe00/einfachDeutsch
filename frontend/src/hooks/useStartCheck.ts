import { useMutation, useQueryClient } from "@tanstack/react-query"
import { useNavigate } from "react-router-dom"

import { startCheck } from "@/api/curriculum"
import type { CheckStart } from "@/types"

/** Start (or resume) a review or Modul test and open it. */
export function useStartCheck() {
  const navigate = useNavigate()
  const queryClient = useQueryClient()
  return useMutation({
    mutationFn: (what: CheckStart) => startCheck(what),
    onSuccess: (check) => {
      queryClient.setQueryData(["check", check.id], check)
      navigate(`/check/${check.id}`)
    },
  })
}
