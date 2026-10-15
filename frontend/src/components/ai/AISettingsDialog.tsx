import { useEffect, useState } from "react"
import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query"
import { X } from "lucide-react"

import { fetchAISettings, saveAISettings } from "@/api/ai"
import type { AISettings } from "@/types"
import { errorText } from "@/lib/apiError"
import { Button } from "@/components/ui/button"
import { Select } from "@/components/ui/Select"

/*
 * "Personalise": how the AI tutor talks to this learner. Saved on the server
 * and sent with every chat. Reply language is the language the tutor explains
 * in; the German being learned is German in every setting.
 */
const LANGUAGE_NAMES = { en: "English", mixed: "Mixed", de: "German" } as const

export function AISettingsDialog({ onClose }: { onClose: () => void }) {
  const qc = useQueryClient()
  const { data } = useQuery({ queryKey: ["ai-settings"], queryFn: fetchAISettings })
  const [draft, setDraft] = useState<AISettings | null>(null)
  const save = useMutation({
    mutationFn: saveAISettings,
    onSuccess: (saved) => {
      qc.setQueryData(["ai-settings"], saved)
      onClose()
    },
  })

  useEffect(() => {
    function onKey(e: KeyboardEvent) {
      if (e.key === "Escape") onClose()
    }
    document.addEventListener("keydown", onKey)
    return () => document.removeEventListener("keydown", onKey)
  }, [onClose])

  const value = draft ?? data
  const set = (patch: Partial<AISettings>) => value && setDraft({ ...value, ...patch })
  const auto = value?.auto_language ? LANGUAGE_NAMES[value.auto_language] : null

  const field =
    "w-full rounded-xl bg-surface-2 px-3.5 py-2.5 text-base placeholder:text-muted-foreground focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring"
  return (
    <div className="fixed inset-0 z-40 flex items-end justify-center sm:items-center" role="dialog" aria-modal="true" aria-labelledby="ai-settings-title">
      <div className="absolute inset-0 bg-black/40 animate-in fade-in-0 duration-150" onClick={onClose} aria-hidden="true" />
      <div className="relative flex max-h-[90svh] w-full max-w-lg flex-col overflow-y-auto rounded-t-[24px] bg-surface p-5 shadow-card animate-in slide-in-from-bottom-8 duration-200 sm:rounded-[24px] sm:p-6">
        <div className="flex items-start justify-between gap-3">
          <div>
            <h2 id="ai-settings-title" className="text-xl font-bold">Personalise your tutor</h2>
            <p className="mt-1 text-sm text-muted-foreground">Used in every chat. Your level and learned words are always included.</p>
          </div>
          <Button variant="secondary" size="icon" aria-label="Close" onClick={onClose}>
            <X />
          </Button>
        </div>

        {!value ? (
          <p className="py-8 text-center text-muted-foreground">Loading…</p>
        ) : (
          <div className="mt-5 flex flex-col gap-4">
            <Field label="Reply language">
              <Select
                label="Reply language"
                value={value.reply_language}
                onChange={(v) => set({ reply_language: v })}
                options={[
                  { value: "auto", label: auto ? `By my level (now ${auto})` : "By my level", description: "English at A1, Mixed at A2, German from B1" },
                  { value: "en", label: "English", description: "Explains in English; German for examples and corrections" },
                  { value: "mixed", label: "Mixed", description: "Simple German, with English notes after harder parts" },
                  { value: "de", label: "German", description: "All German at your level; English only if you ask" },
                ]}
              />
            </Field>
            <div className="grid gap-4 sm:grid-cols-2">
              <Field label="Tone">
                <Select
                  label="Tone"
                  value={value.tone}
                  onChange={(v) => set({ tone: v })}
                  options={[
                    { value: "friendly", label: "Friendly tutor" },
                    { value: "strict", label: "Strict teacher" },
                  ]}
                />
              </Field>
              <Field label="Corrections">
                <Select
                  label="Corrections"
                  value={value.corrections}
                  onChange={(v) => set({ corrections: v })}
                  options={[
                    { value: "major", label: "Only big mistakes" },
                    { value: "all", label: "Every mistake" },
                  ]}
                />
              </Field>
            </div>
            <Field label="Interests (used in examples)">
              <input
                value={value.interests}
                maxLength={200}
                onChange={(e) => set({ interests: e.target.value })}
                placeholder="e.g. football, cooking, travel"
                className={field}
              />
            </Field>
            <Field label="About me">
              <textarea
                value={value.about}
                maxLength={500}
                rows={3}
                onChange={(e) => set({ about: e.target.value })}
                placeholder="e.g. I'm moving to Berlin for work and want to talk to colleagues."
                className={field}
              />
            </Field>
            {save.isError && <p className="text-sm text-danger">{errorText(save.error)}</p>}
            <Button size="lg" disabled={save.isPending || !draft} onClick={() => draft && save.mutate(draft)}>
              {save.isPending ? "Saving…" : "Save"}
            </Button>
          </div>
        )}
      </div>
    </div>
  )
}

function Field({ label, children }: { label: string; children: React.ReactNode }) {
  return (
    <label className="flex flex-col gap-1.5">
      <span className="text-sm font-medium text-muted-foreground">{label}</span>
      {children}
    </label>
  )
}
