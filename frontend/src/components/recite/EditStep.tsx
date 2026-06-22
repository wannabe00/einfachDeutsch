import { Button } from "@/components/ui/button"

/** Step 1 — paste/type the German text to retell. */
export function EditStep({
  sourceText,
  onChange,
  onStudy,
  disabled,
}: {
  sourceText: string
  onChange: (v: string) => void
  onStudy: () => void
  disabled: boolean
}) {
  return (
    <div className="mt-6 flex flex-col gap-3 rounded-xl border border-border bg-surface p-5">
      <label className="text-sm font-medium">Text to retell</label>
      <textarea
        value={sourceText}
        onChange={(e) => onChange(e.target.value)}
        rows={6}
        placeholder="Paste or type a short German paragraph here…"
        className="w-full rounded-lg border border-border bg-background p-3 text-sm"
      />
      <Button className="self-start" disabled={disabled} onClick={onStudy}>
        Study it →
      </Button>
    </div>
  )
}
