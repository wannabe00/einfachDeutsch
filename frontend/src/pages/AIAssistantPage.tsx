import { useEffect, useRef, useState, type FormEvent } from "react"
import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query"
import ReactMarkdown from "react-markdown"
import remarkGfm from "remark-gfm"
import { Check, Loader2, MessageSquarePlus, Pencil, Send, Trash2, X } from "lucide-react"
import { isAxiosError } from "axios"

import {
  createConversation,
  deleteConversation,
  fetchConversation,
  fetchConversations,
  renameConversation,
  sendMessage,
} from "@/api/conversations"
import type { Conversation } from "@/types"
import { Button } from "@/components/ui/button"
import { cn } from "@/lib/utils"

/*
 * AI Assistant with ChatGPT-style history (Phase 23.13): a conversation list on
 * the left, the thread on the right. Both turns are persisted server-side, so a
 * chat survives a refresh and can be resumed, renamed or deleted. Premium-gated
 * (the route is wrapped in RequirePremium; the API enforces it too).
 */
const SUGGESTIONS = [
  "Suggest words for greetings",
  "Explain the German case system",
  "When do I use 'doch'?",
]

export default function AIAssistantPage() {
  const qc = useQueryClient()
  const [activeId, setActiveId] = useState<number | null>(null)
  const [input, setInput] = useState("")
  const [error, setError] = useState("")
  const scrollRef = useRef<HTMLDivElement>(null)

  const { data: conversations } = useQuery({
    queryKey: ["conversations"],
    queryFn: fetchConversations,
  })

  const { data: thread } = useQuery({
    queryKey: ["conversation", activeId],
    queryFn: () => fetchConversation(activeId!),
    enabled: activeId !== null,
  })

  const messages = thread?.messages ?? []

  const send = useMutation({
    mutationFn: async (text: string) => {
      // First message with no chat open? Start one, then send into it.
      const id = activeId ?? (await createConversation()).id
      if (activeId === null) setActiveId(id)
      return sendMessage(id, text)
    },
    onSuccess: (res) => {
      setError("")
      qc.invalidateQueries({ queryKey: ["conversation", res.conversation.id] })
      qc.invalidateQueries({ queryKey: ["conversations"] })
    },
    onError: (err) => {
      setError(
        isAxiosError(err) && err.response?.status === 503
          ? "AI is not configured yet. Add GEMINI_API_KEY to backend/.env to enable it."
          : "Something went wrong. Please try again.",
      )
    },
  })

  const remove = useMutation({
    mutationFn: deleteConversation,
    onSuccess: (_d, id) => {
      if (id === activeId) setActiveId(null)
      qc.invalidateQueries({ queryKey: ["conversations"] })
    },
  })

  const rename = useMutation({
    mutationFn: ({ id, title }: { id: number; title: string }) => renameConversation(id, title),
    onSuccess: () => qc.invalidateQueries({ queryKey: ["conversations"] }),
  })

  useEffect(() => {
    scrollRef.current?.scrollTo({ top: scrollRef.current.scrollHeight })
  }, [messages.length, send.isPending])

  function submit(e: FormEvent) {
    e.preventDefault()
    const text = input.trim()
    if (!text || send.isPending) return
    setInput("")
    send.mutate(text)
  }

  return (
    <div className="flex h-[calc(100vh-8rem)] gap-4">
      {/* Conversation list */}
      <aside className="hidden w-60 shrink-0 flex-col md:flex">
        <Button className="w-full" onClick={() => setActiveId(null)}>
          <MessageSquarePlus className="mr-2 size-4" /> New chat
        </Button>
        <div className="mt-3 flex-1 overflow-y-auto">
          {(conversations ?? []).length === 0 ? (
            <p className="px-2 py-3 text-xs text-muted-foreground">No chats yet.</p>
          ) : (
            <ul className="flex flex-col gap-1">
              {(conversations ?? []).map((c) => (
                <ConversationRow
                  key={c.id}
                  conversation={c}
                  active={c.id === activeId}
                  onOpen={() => setActiveId(c.id)}
                  onRename={(title) => rename.mutate({ id: c.id, title })}
                  onDelete={() => remove.mutate(c.id)}
                />
              ))}
            </ul>
          )}
        </div>
      </aside>

      {/* Thread */}
      <div className="flex min-w-0 flex-1 flex-col">
        <div ref={scrollRef} className="flex-1 overflow-y-auto">
          {messages.length === 0 && !send.isPending ? (
            <div className="flex flex-col gap-3 py-8">
              <h1 className="text-xl font-bold">AI Assistant</h1>
              <p className="text-sm text-muted-foreground">
                Your German tutor. Chats are saved — pick one on the left or start a new one.
              </p>
              <div className="mt-2 flex flex-wrap gap-2">
                {SUGGESTIONS.map((s) => (
                  <button
                    key={s}
                    onClick={() => send.mutate(s)}
                    className="rounded-full border border-border bg-surface px-3 py-1.5 text-sm transition-colors hover:border-primary/50"
                  >
                    {s}
                  </button>
                ))}
              </div>
            </div>
          ) : (
            <div className="flex flex-col gap-4 pb-4">
              {messages.map((m) => (
                <div
                  key={m.id}
                  className={cn("flex", m.role === "user" ? "justify-end" : "justify-start")}
                >
                  <div
                    className={cn(
                      "max-w-[80%] rounded-xl px-4 py-2.5 text-sm leading-relaxed",
                      m.role === "user"
                        ? "bg-primary text-primary-foreground"
                        : "border border-border bg-surface text-foreground",
                      "[&_code]:rounded [&_code]:bg-background/50 [&_code]:px-1 [&_code]:font-mono",
                      "[&_table]:my-2 [&_table]:w-full [&_table]:border-collapse",
                      "[&_th]:border [&_th]:border-border [&_th]:px-2 [&_th]:py-1 [&_th]:text-left",
                      "[&_td]:border [&_td]:border-border [&_td]:px-2 [&_td]:py-1",
                      "[&_p]:my-1.5 [&_ul]:my-1.5 [&_ul]:list-disc [&_ul]:pl-5 [&_strong]:font-semibold",
                    )}
                  >
                    <ReactMarkdown remarkPlugins={[remarkGfm]}>{m.content}</ReactMarkdown>
                  </div>
                </div>
              ))}
              {send.isPending && (
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
          <div className="mb-2 rounded-md border border-[hsl(var(--danger))]/40 bg-[hsl(var(--danger-bg))] px-3 py-2 text-sm text-[hsl(var(--danger))]">
            {error}
          </div>
        )}

        <form onSubmit={submit} className="mt-2 flex gap-2 border-t border-border pt-4">
          <input
            value={input}
            onChange={(e) => setInput(e.target.value)}
            placeholder="Ask about German…"
            aria-label="Message the AI tutor"
            className="flex-1 rounded-md border border-input bg-surface px-3 py-2 text-sm focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring"
          />
          <Button type="submit" disabled={send.isPending || !input.trim()}>
            <Send className="size-4" />
          </Button>
        </form>
      </div>
    </div>
  )
}

function ConversationRow({
  conversation,
  active,
  onOpen,
  onRename,
  onDelete,
}: {
  conversation: Conversation
  active: boolean
  onOpen: () => void
  onRename: (title: string) => void
  onDelete: () => void
}) {
  const [editing, setEditing] = useState(false)
  const [draft, setDraft] = useState(conversation.title)

  if (editing) {
    return (
      <li className="flex items-center gap-1 rounded-md bg-surface p-1">
        <input
          autoFocus
          value={draft}
          onChange={(e) => setDraft(e.target.value)}
          onKeyDown={(e) => {
            if (e.key === "Enter" && draft.trim()) {
              onRename(draft.trim())
              setEditing(false)
            }
            if (e.key === "Escape") setEditing(false)
          }}
          className="min-w-0 flex-1 rounded bg-background px-2 py-1 text-sm focus-visible:outline-none"
        />
        <button
          aria-label="Save title"
          onClick={() => {
            if (draft.trim()) onRename(draft.trim())
            setEditing(false)
          }}
          className="p-1 text-muted-foreground hover:text-foreground"
        >
          <Check className="size-3.5" />
        </button>
        <button
          aria-label="Cancel rename"
          onClick={() => setEditing(false)}
          className="p-1 text-muted-foreground hover:text-foreground"
        >
          <X className="size-3.5" />
        </button>
      </li>
    )
  }

  return (
    <li
      className={cn(
        "group flex items-center gap-1 rounded-md px-2 py-1.5 transition-colors",
        active ? "bg-primary/15" : "hover:bg-surface",
      )}
    >
      <button onClick={onOpen} className="min-w-0 flex-1 truncate text-left text-sm">
        {conversation.title || "New chat"}
      </button>
      <button
        aria-label="Rename chat"
        onClick={() => {
          setDraft(conversation.title)
          setEditing(true)
        }}
        className="p-1 text-muted-foreground opacity-0 transition-opacity hover:text-foreground group-hover:opacity-100"
      >
        <Pencil className="size-3.5" />
      </button>
      <button
        aria-label="Delete chat"
        onClick={onDelete}
        className="p-1 text-muted-foreground opacity-0 transition-opacity hover:text-[hsl(var(--danger))] group-hover:opacity-100"
      >
        <Trash2 className="size-3.5" />
      </button>
    </li>
  )
}
