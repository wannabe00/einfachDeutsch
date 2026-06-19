import { useRef, useState } from "react"
import { useMutation, useQueryClient } from "@tanstack/react-query"
import { Upload } from "lucide-react"

import { importWordsCsv } from "@/api/vocabulary"
import type { Chapter, ImportResult } from "@/types"
import { Button } from "@/components/ui/button"

interface CSVImportButtonProps {
  chapters: Chapter[]
  defaultChapterId?: number
}

export function CSVImportButton({ chapters, defaultChapterId }: CSVImportButtonProps) {
  const qc = useQueryClient()
  const [open, setOpen] = useState(false)
  const [chapterId, setChapterId] = useState(defaultChapterId ?? chapters[0]?.id ?? 0)
  const [result, setResult] = useState<ImportResult | null>(null)
  const fileRef = useRef<HTMLInputElement>(null)

  const mutation = useMutation({
    mutationFn: (file: File) => importWordsCsv(file, chapterId),
    onSuccess: (data) => {
      setResult(data)
      qc.invalidateQueries({ queryKey: ["words"] })
      qc.invalidateQueries({ queryKey: ["due-counts"] })
      qc.invalidateQueries({ queryKey: ["stats"] })
    },
  })

  function handleFile(file?: File) {
    if (file) mutation.mutate(file)
    if (fileRef.current) fileRef.current.value = ""
  }

  return (
    <div>
      <Button variant="secondary" onClick={() => setOpen((v) => !v)}>
        <Upload className="mr-2 size-4" /> Import CSV
      </Button>

      {open && (
        <div className="mt-3 rounded-xl border border-border bg-surface p-4">
          <p className="mb-2 text-sm text-muted-foreground">
            CSV columns: <code className="font-mono">english, german, notes</code>{" "}
            (notes optional). Rows duplicating an existing word in the chosen chapter are skipped.
          </p>
          <div className="flex flex-wrap items-center gap-2">
            <select
              value={chapterId}
              onChange={(e) => setChapterId(Number(e.target.value))}
              className="rounded-md border border-input bg-background px-3 py-2 text-sm"
            >
              {chapters.map((c) => (
                <option key={c.id} value={c.id}>
                  {c.title}
                </option>
              ))}
            </select>
            <input
              ref={fileRef}
              type="file"
              accept=".csv,text/csv"
              onChange={(e) => handleFile(e.target.files?.[0])}
              className="text-sm text-muted-foreground file:mr-3 file:rounded-md file:border file:border-input file:bg-background file:px-3 file:py-1.5 file:text-sm file:text-foreground"
            />
          </div>

          {mutation.isPending && (
            <p className="mt-3 text-sm text-muted-foreground">Importing…</p>
          )}
          {result && (
            <p className="mt-3 text-sm text-foreground">
              Imported <span className="font-semibold">{result.created}</span> new
              word{result.created === 1 ? "" : "s"}, skipped{" "}
              <span className="font-semibold">{result.skipped}</span>.
            </p>
          )}
          {mutation.isError && (
            <p className="mt-3 text-sm text-[hsl(var(--danger))]">
              Import failed. Check the file format and try again.
            </p>
          )}
        </div>
      )}
    </div>
  )
}
