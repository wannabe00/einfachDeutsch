import { useState, useRef, useEffect, type FormEvent } from "react"
import { useMutation } from "@tanstack/react-query"
import ReactMarkdown from "react-markdown"
import remarkGfm from "remark-gfm"
import { Loader2, Send } from "lucide-react"
import { isAxiosError } from "axios"

import { aiChat, type ChatTurn } from "@/api/ai"
import { Button } from "@/components/ui/button"
import { cn } from "@/lib/utils"

const SUGGESTIONS = [
  "Suggest words for greetings",
  "Explain the German case system",
  "When do I use 'doch'?",
]

export default function AIAssistantPage() {
  const [messages, setMessages] = useState<ChatTurn[]>([])
  const [input, setInput] = useState("")
  const [error, setError] = useState("")
  const scrollRef = useRef<HTMLDivElement>(null)

  const mutation = useMutation({
    mutationFn: (message: string) => aiChat(message, messages),
    onSuccess: (text) => {
      setMessages((m) => [...m, { role: "assistant", content: text }])
      setError("")
    },
    onError: (err) => {
      if (isAxiosError(err) && err.response?.status === 503) {
        setError(
          "AI is not configured yet. Add GEMINI_API_KEY to backend/.env to enable it.",
        )
      } else {
        setError("Something went wrong. Please try again.")
      }
      // drop the optimistic user turn's pending state; keep the message shown
    },
  })

  useEffect(() => {
    scrollRef.current?.scrollTo({ top: scrollRef.current.scrollHeight })
  }, [messages, mutation.isPending])

  function send(text: string) {
    const trimmed = text.trim()
    if (!trimmed || mutation.isPending) return
    setMessages((m) => [...m, { role: "user", content: trimmed }])
    setInput("")
    mutation.mutate(trimmed)
  }

  function handleSubmit(e: FormEvent) {
    e.preventDefault()
    send(input)
  }

  const empty = messages.length === 0

  return (
    <div className="flex h-[calc(100vh-4rem)] flex-col">
      <h1 className="text-2xl font-semibold tracking-tight">AI Assistant</h1>
      <p className="mt-1 text-sm text-muted-foreground">
        Your German tutor. Conversations reset on refresh.
      </p>

      {/* Messages */}
      <div ref={scrollRef} className="mt-6 flex-1 overflow-y-auto">
        {empty ? (
          <div className="flex flex-col gap-3 py-8">
            <p className="text-sm text-muted-foreground">Try asking:</p>
            <div className="flex flex-wrap gap-2">
              {SUGGESTIONS.map((s) => (
                <button
                  key={s}
                  onClick={() => send(s)}
                  className="rounded-full border border-border bg-surface px-3 py-1.5 text-sm text-foreground transition-colors hover:border-accent"
                >
                  {s}
                </button>
              ))}
            </div>
          </div>
        ) : (
          <div className="flex flex-col gap-4 pb-4">
            {messages.map((m, i) => (
              <div
                key={i}
                className={cn(
                  "flex",
                  m.role === "user" ? "justify-end" : "justify-start",
                )}
              >
                <div
                  className={cn(
                    "max-w-[80%] rounded-xl px-4 py-2.5 text-sm leading-relaxed",
                    m.role === "user"
                      ? "bg-accent text-accent-foreground"
                      : "border border-border bg-surface text-foreground",
                    "[&_code]:rounded [&_code]:bg-background/50 [&_code]:px-1 [&_code]:font-mono",
                    "[&_table]:my-2 [&_table]:w-full [&_table]:border-collapse",
                    "[&_th]:border [&_th]:border-border [&_th]:px-2 [&_th]:py-1 [&_th]:text-left",
                    "[&_td]:border [&_td]:border-border [&_td]:px-2 [&_td]:py-1",
                    "[&_p]:my-1.5 [&_ul]:my-1.5 [&_ul]:list-disc [&_ul]:pl-5 [&_strong]:font-semibold",
                  )}
                >
                  <ReactMarkdown remarkPlugins={[remarkGfm]}>
                    {m.content}
                  </ReactMarkdown>
                </div>
              </div>
            ))}
            {mutation.isPending && (
              <div className="flex justify-start">
                <div className="flex items-center gap-2 rounded-xl border border-border bg-surface px-4 py-2.5 text-sm text-muted-foreground">
                  <Loader2 className="size-4 animate-spin" /> Thinking…
                </div>
              </div>
            )}
          </div>
        )}
      </div>

      {error && (
        <div className="mb-2 rounded-md border border-danger/40 bg-[hsl(var(--danger-bg))] px-3 py-2 text-sm text-[hsl(var(--danger))]">
          {error}
        </div>
      )}

      {/* Composer */}
      <form onSubmit={handleSubmit} className="mt-2 flex gap-2 border-t border-border pt-4">
        <input
          value={input}
          onChange={(e) => setInput(e.target.value)}
          placeholder="Ask about German…"
          aria-label="Message the AI tutor"
          className="flex-1 rounded-md border border-input bg-surface px-3 py-2 text-sm focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring"
        />
        <Button type="submit" disabled={mutation.isPending || !input.trim()}>
          <Send className="size-4" />
        </Button>
      </form>
    </div>
  )
}
