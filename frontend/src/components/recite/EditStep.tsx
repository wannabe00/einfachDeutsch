import { ArrowRight } from "lucide-react"

import { Button } from "@/components/ui/button"

/** Step 1: paste or type the German text to retell. */
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
    <div className="flex flex-col gap-4 rounded-[24px] bg-surface p-6 shadow-card sm:p-7">
      <div>
        <label htmlFor="recite-text" className="text-xl font-bold">
          Text to retell
        </label>
        <p className="mt-1 text-sm text-muted-foreground">
          A short paragraph works best: three to six sentences.
        </p>
      </div>
      <textarea
        id="recite-text"
        value={sourceText}
        onChange={(e) => onChange(e.target.value)}
        rows={7}
        placeholder="Paste or type a short German paragraph here…"
        className="w-full rounded-2xl border border-transparent bg-surface-2 p-4 text-base leading-relaxed transition-colors focus-visible:border-ring focus-visible:outline-none"
      />
      <Button size="lg" className="self-start" disabled={disabled} onClick={onStudy}>
        Study it <ArrowRight />
      </Button>
    </div>
  )
}
