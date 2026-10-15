import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query"
import { Trash2 } from "lucide-react"

import { deleteSavedWord, fetchSavedWords } from "@/api/vocabulary"
import { Card } from "@/components/ui/card"

/** The learner's own words: added here or saved from an AI chat. */
export function SavedWords() {
  const qc = useQueryClient()
  const { data: words } = useQuery({ queryKey: ["saved-words"], queryFn: fetchSavedWords })
  const remove = useMutation({
    mutationFn: deleteSavedWord,
    onSuccess: () => qc.invalidateQueries({ queryKey: ["saved-words"] }),
  })
  if (!words?.length) return null

  return (
    <section>
      <h2 className="mb-3 px-1 text-[22px] font-bold">
        Your words <span className="text-muted-foreground">{words.length}</span>
      </h2>
      <Card className="p-2 sm:p-3">
        <ul className="grid sm:grid-cols-2 sm:gap-x-4">
          {words.map((w) => (
            <li key={w.id} className="flex min-h-[48px] items-center gap-3 border-b border-border/60 px-3 py-2 last:border-0">
              <span className="min-w-0 flex-1">
                <span className="block truncate font-medium">{w.german}</span>
                {(w.english || w.notes) && (
                  <span className="block truncate text-sm text-muted-foreground">
                    {[w.english, w.notes].filter(Boolean).join(" · ")}
                  </span>
                )}
              </span>
              <button
                type="button"
                aria-label={`Remove ${w.german}`}
                onClick={() => remove.mutate(w.id)}
                className="flex size-9 shrink-0 items-center justify-center rounded-lg text-muted-foreground transition-colors hover:bg-surface-2 hover:text-danger"
              >
                <Trash2 className="size-4" />
              </button>
            </li>
          ))}
        </ul>
      </Card>
    </section>
  )
}
