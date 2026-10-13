import { useState } from "react"
import { useMutation } from "@tanstack/react-query"
import ReactMarkdown from "react-markdown"
import remarkGfm from "remark-gfm"
import { Loader2, Sparkles, X } from "lucide-react"
import { isAxiosError } from "axios"

import { aiChat } from "@/api/ai"
import { useAIPanel } from "@/contexts/AIPanelContext"
import { Button } from "@/components/ui/button"

export function AIPanel() {
  const { panel, closePanel } = useAIPanel()
  const [prompt, setPrompt] = useState("")
  const [response, setResponse] = useState("")
  const [error, setError] = useState("")

  const mutation = useMutation({
    mutationFn: (text: string) => aiChat(text),
    onSuccess: (text) => {
      setResponse(text)
      setError("")
    },
    onError: (err) => {
      setResponse("")
      if (isAxiosError(err) && err.response?.status === 503) {
        setError(
          "AI is not configured yet. Add GEMINI_API_KEY to backend/.env to enable it.",
        )
      } else {
        setError("Something went wrong. Please try again.")
      }
    },
  })

  // Reset whenever a new panel is opened (render-time, keyed on panel identity).
  const [lastPanel, setLastPanel] = useState(panel)
  if (panel !== lastPanel) {
    setLastPanel(panel)
    setPrompt(panel?.initialPrompt ?? "")
    setResponse("")
    setError("")
  }

  if (!panel) return null

  return (
    <>
      {/* Backdrop */}
      <div
        className="fixed inset-0 z-40 bg-black/40 motion-safe:animate-in motion-safe:fade-in-0"
        onClick={closePanel}
        aria-hidden="true"
      />
      {/* Panel */}
      <aside
        className="fixed right-0 top-0 z-50 flex h-full w-[480px] max-w-[92vw] flex-col rounded-l-[28px] bg-background shadow-lift
          motion-safe:animate-in motion-safe:slide-in-from-right motion-safe:duration-200"
        role="dialog"
        aria-label={panel.title}
      >
        <header className="flex items-center justify-between gap-3 px-5 py-4">
          <h2 className="flex items-center gap-2.5 text-lg font-bold">
            <span className="flex size-8 items-center justify-center rounded-xl bg-[hsl(var(--section-3))] text-white">
              <Sparkles className="size-4" aria-hidden="true" />
            </span>
            {panel.title}
          </h2>
          <button
            onClick={closePanel}
            aria-label="Close AI panel"
            className="flex size-10 items-center justify-center rounded-full bg-surface-2 text-muted-foreground hover:text-foreground"
          >
            <X className="size-5" />
          </button>
        </header>

        <div className="flex flex-1 flex-col gap-3 overflow-y-auto px-5 pb-5">
          <textarea
            value={prompt}
            onChange={(e) => setPrompt(e.target.value)}
            rows={3}
            aria-label="Your question"
            className="w-full rounded-2xl border border-transparent bg-surface px-4 py-3 text-base shadow-card focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring"
            placeholder="Ask the AI tutor…"
          />
          <Button
            onClick={() => prompt.trim() && mutation.mutate(prompt.trim())}
            disabled={mutation.isPending || !prompt.trim()}
          >
            {mutation.isPending ? (
              <>
                <Loader2 className="animate-spin" /> Thinking…
              </>
            ) : (
              "Ask AI"
            )}
          </Button>

          {error && (
            <div className="rounded-xl bg-danger-bg px-4 py-2.5 text-sm font-medium text-danger" role="alert">
              {error}
            </div>
          )}

          {response && (
            <div
              className="mt-2 rounded-[22px] bg-surface p-5 text-[15px] leading-relaxed shadow-card animate-in fade-in-0 duration-200
                [&_code]:rounded [&_code]:bg-surface-2 [&_code]:px-1 [&_code]:font-mono
                [&_table]:my-2 [&_table]:w-full [&_table]:border-collapse
                [&_th]:border [&_th]:border-border [&_th]:px-2 [&_th]:py-1 [&_th]:text-left
                [&_td]:border [&_td]:border-border [&_td]:px-2 [&_td]:py-1
                [&_p]:my-2 [&_ul]:my-2 [&_ul]:list-disc [&_ul]:pl-5 [&_strong]:font-semibold"
            >
              <ReactMarkdown remarkPlugins={[remarkGfm]}>{response}</ReactMarkdown>
            </div>
          )}
        </div>
      </aside>
    </>
  )
}
