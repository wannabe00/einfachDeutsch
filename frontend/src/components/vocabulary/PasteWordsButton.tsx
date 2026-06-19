import { useMemo, useState } from "react"
import { useMutation, useQueryClient } from "@tanstack/react-query"
import { ClipboardList } from "lucide-react"

import { bulkAddWords } from "@/api/vocabulary"
import type { Chapter } from "@/types"
import { Button } from "@/components/ui/button"

interface PasteWordsButtonProps {
  chapters: Chapter[]
  defaultChapterId?: number
}

/** Parse pasted lines like "der Hund - dog" / "der Hund, dog" / "der Hund\tdog". */
function parseLines(text: string): { german: string; english: string }[] {
  return text
    .split("\n")
    .map((line) => line.trim())
    .filter(Boolean)
    .map((line) => {
      const m = line.split(/\s*[\t–—\-=,;|]\s*/)
      const german = (m[0] ?? "").trim()
      const english = (m.slice(1).join(" ") ?? "").trim()
      return { german, english }
    })
    .filter((r) => r.german && r.english)
}

export function PasteWordsButton({ chapters, defaultChapterId }: PasteWordsButtonProps) {
  const qc = useQueryClient()
  const [open, setOpen] = useState(false)
  const [text, setText] = useState("")
  const [chapterId, setChapterId] = useState(defaultChapterId ?? chapters[0]?.id ?? 0)
  const [result, setResult] = useState<{ created: number; skipped: number } | null>(null)

  const parsed = useMemo(() => parseLines(text), [text])

  const mutation = useMutation({
    mutationFn: () => bulkAddWords(chapterId, parsed),
    onSuccess: (data) => {
      setResult(data)
      setText("")
      qc.invalidateQueries({ queryKey: ["words"] })
      qc.invalidateQueries({ queryKey: ["due-counts"] })
      qc.invalidateQueries({ queryKey: ["stats"] })
    },
  })

  return (
    <div>
      <Button variant="secondary" onClick={() => setOpen((v) => !v)}>
        <ClipboardList className="mr-2 size-4" /> Paste list
      </Button>

      {open && (
        <div className="mt-3 rounded-xl border border-border bg-surface p-4">
          <p className="mb-2 text-sm text-muted-foreground">
            One word per line: <code className="font-mono">German - English</code>{" "}
            (separators <code className="font-mono">- , = tab</code> all work).
          </p>
          <select
            value={chapterId}
            onChange={(e) => setChapterId(Number(e.target.value))}
            className="mb-2 rounded-md border border-input bg-background px-3 py-2 text-sm"
          >
            {chapters.map((c) => (
              <option key={c.id} value={c.id}>
                {c.title}
              </option>
            ))}
          </select>
          <textarea
            value={text}
            onChange={(e) => {
              setText(e.target.value)
              setResult(null)
            }}
            rows={6}
            placeholder={"der Hund - dog\ndie Katze - cat\ndas Haus - house"}
            className="w-full rounded-md border border-input bg-background px-3 py-2 font-mono text-sm focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring"
          />
          <div className="mt-3 flex items-center gap-3">
            <Button
              onClick={() => mutation.mutate()}
              disabled={mutation.isPending || parsed.length === 0}
            >
              {mutation.isPending ? "Adding…" : `Add ${parsed.length} word${parsed.length === 1 ? "" : "s"}`}
            </Button>
            {result && (
              <span className="text-sm text-foreground">
                Added <span className="font-semibold">{result.created}</span>, skipped{" "}
                <span className="font-semibold">{result.skipped}</span>.
              </span>
            )}
          </div>
        </div>
      )}
    </div>
  )
}
