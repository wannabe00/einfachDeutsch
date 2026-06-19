import { useState } from "react"
import { useMutation } from "@tanstack/react-query"
import ReactMarkdown from "react-markdown"
import remarkGfm from "remark-gfm"
import { X, Loader2 } from "lucide-react"
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
        className="fixed inset-0 z-40 bg-black/30"
        onClick={closePanel}
        aria-hidden="true"
      />
      {/* Panel */}
      <aside
        className="fixed right-0 top-0 z-50 flex h-full w-[480px] max-w-[90vw] flex-col border-l border-border bg-background shadow-xl
          motion-safe:animate-in motion-safe:slide-in-from-right motion-safe:duration-200"
        role="dialog"
        aria-label={panel.title}
      >
        <header className="flex items-center justify-between border-b border-border px-5 py-4">
          <h2 className="text-base font-semibold tracking-tight">{panel.title}</h2>
          <button
            onClick={closePanel}
            aria-label="Close AI panel"
            className="rounded-md p-1 text-muted-foreground hover:bg-surface hover:text-foreground"
          >
            <X className="size-5" />
          </button>
        </header>

        <div className="flex flex-1 flex-col gap-3 overflow-y-auto p-5">
          <textarea
            value={prompt}
            onChange={(e) => setPrompt(e.target.value)}
            rows={3}
            className="w-full rounded-md border border-input bg-surface px-3 py-2 text-sm focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring"
            placeholder="Ask the AI tutor…"
          />
          <Button
            onClick={() => prompt.trim() && mutation.mutate(prompt.trim())}
            disabled={mutation.isPending || !prompt.trim()}
          >
            {mutation.isPending ? (
              <>
                <Loader2 className="mr-2 size-4 animate-spin" /> Thinking…
              </>
            ) : (
              "Ask AI"
            )}
          </Button>

          {error && (
            <div className="rounded-md border border-danger/40 bg-[hsl(var(--danger-bg))] px-3 py-2 text-sm text-[hsl(var(--danger))]">
              {error}
            </div>
          )}

          {response && (
            <div
              className="mt-2 rounded-lg border border-border bg-surface p-4 text-sm leading-relaxed
                [&_code]:rounded [&_code]:bg-background [&_code]:px-1 [&_code]:font-mono
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
