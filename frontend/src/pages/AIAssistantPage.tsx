import { useEffect, useRef, useState, type FormEvent } from "react"
import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query"
import ReactMarkdown from "react-markdown"
import remarkGfm from "remark-gfm"
import {
  Check,
  Loader2,
  MessageSquarePlus,
  MessagesSquare,
  Pencil,
  Send,
  Sparkles,
  Trash2,
  X,
} from "lucide-react"
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
 * AI Assistant: saved conversations on the left, the open chat on the right.
 * Both sides of each chat are stored on the server, so chats survive a refresh
 * and can be resumed, renamed or deleted. Premium only (checked by the route
 * and by the API).
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
  // Phones show either the chat or the list of chats.
  const [showList, setShowList] = useState(false)
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

  const list = (
    <ConversationList
      conversations={conversations ?? []}
      activeId={activeId}
      onNew={() => {
        setActiveId(null)
        setShowList(false)
      }}
      onOpen={(id) => {
        setActiveId(id)
        setShowList(false)
      }}
      onRename={(id, title) => rename.mutate({ id, title })}
      onDelete={(id) => remove.mutate(id)}
    />
  )

  return (
    <div className="flex h-[calc(100svh-12.5rem)] min-h-[420px] flex-col gap-3 lg:h-[calc(100vh-9rem)] lg:flex-row lg:gap-5">
      {/* Phones: a bar to switch between the chat and the list of chats. */}
      <div className="flex items-center justify-between gap-2 lg:hidden">
        <h1 className="text-2xl font-extrabold">AI Assistant</h1>
        <div className="flex gap-2">
          <Button variant="secondary" size="sm" onClick={() => setShowList((v) => !v)} aria-expanded={showList}>
            <MessagesSquare /> {showList ? "Back to chat" : "Chats"}
          </Button>
          <Button
            size="icon"
            className="size-9"
            aria-label="New chat"
            onClick={() => {
              setActiveId(null)
              setShowList(false)
            }}
          >
            <MessageSquarePlus />
          </Button>
        </div>
      </div>

      {/* Conversation list: a side card on desktop, a full view on phones. */}
      <aside className="hidden w-64 shrink-0 lg:flex">{list}</aside>
      {showList && <div className="flex min-h-0 flex-1 lg:hidden">{list}</div>}

      {/* Thread */}
      <div className={cn("min-w-0 flex-1 flex-col", showList ? "hidden lg:flex" : "flex")}>
        <div ref={scrollRef} className="min-h-0 flex-1 overflow-y-auto">
          {messages.length === 0 && !send.isPending ? (
            <div className="flex h-full flex-col items-center justify-center gap-3 px-2 py-8 text-center">
              <span className="flex size-16 items-center justify-center rounded-2xl bg-[hsl(var(--section-3))] text-white">
                <Sparkles className="size-8" aria-hidden="true" />
              </span>
              <h2 className="mt-2 text-3xl font-extrabold">Ask me anything about German</h2>
              <p className="max-w-md text-muted-foreground">
                Grammar, words, how to say something. Your chats are saved, so you can come back to them.
              </p>
              <div className="mt-4 grid w-full max-w-xl gap-2.5 sm:grid-cols-3">
                {SUGGESTIONS.map((s) => (
                  <button
                    key={s}
                    onClick={() => send.mutate(s)}
                    className="lift min-h-[64px] rounded-2xl bg-surface p-4 text-left text-[15px] font-medium shadow-card"
                  >
                    {s}
                  </button>
                ))}
              </div>
            </div>
          ) : (
            <div className="mx-auto flex max-w-3xl flex-col gap-4 pb-4 pt-1">
              {messages.map((m) => (
                <div
                  key={m.id}
                  className={cn(
                    "flex animate-in fade-in-0 slide-in-from-bottom-1 duration-200",
                    m.role === "user" ? "justify-end" : "justify-start",
                  )}
                >
                  <div
                    className={cn(
                      "max-w-[85%] rounded-[22px] px-4 py-3 text-[15px] leading-relaxed",
                      m.role === "user"
                        ? "rounded-br-md bg-primary text-primary-foreground"
                        : "rounded-bl-md bg-surface text-foreground shadow-card",
                      "[&_code]:rounded [&_code]:bg-surface-2 [&_code]:px-1 [&_code]:font-mono",
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
                  <div className="flex items-center gap-2 rounded-[22px] rounded-bl-md bg-surface px-4 py-3 text-[15px] text-muted-foreground shadow-card">
                    <Loader2 className="size-4 animate-spin" /> Thinking…
                  </div>
                </div>
              )}
            </div>
          )}
        </div>

        {error && (
          <div className="mx-auto mb-2 w-full max-w-3xl rounded-xl bg-danger-bg px-4 py-2.5 text-sm font-medium text-danger" role="alert">
            {error}
          </div>
        )}

        <form
          onSubmit={submit}
          className="mx-auto mt-2 flex w-full max-w-3xl items-center gap-2 rounded-full bg-surface p-1.5 pl-5 shadow-card focus-within:ring-2 focus-within:ring-ring"
        >
          <input
            value={input}
            onChange={(e) => setInput(e.target.value)}
            placeholder="Ask about German…"
            aria-label="Message the AI tutor"
            className="min-w-0 flex-1 bg-transparent py-2 text-base placeholder:text-muted-foreground focus-visible:outline-none"
          />
          <Button
            type="submit"
            size="icon"
            aria-label="Send"
            className="shrink-0"
            disabled={send.isPending || !input.trim()}
          >
            <Send />
          </Button>
        </form>
      </div>
    </div>
  )
}

function ConversationList({
  conversations,
  activeId,
  onNew,
  onOpen,
  onRename,
  onDelete,
}: {
  conversations: Conversation[]
  activeId: number | null
  onNew: () => void
  onOpen: (id: number) => void
  onRename: (id: number, title: string) => void
  onDelete: (id: number) => void
}) {
  return (
    <div className="flex min-h-0 w-full flex-col rounded-[24px] bg-surface p-3 shadow-card">
      <Button className="w-full" onClick={onNew}>
        <MessageSquarePlus /> New chat
      </Button>
      <p className="mt-4 px-2 text-[13px] font-semibold uppercase tracking-[0.04em] text-muted-foreground">
        Your chats
      </p>
      <div className="mt-1.5 min-h-0 flex-1 overflow-y-auto">
        {conversations.length === 0 ? (
          <p className="px-2 py-3 text-sm text-muted-foreground">No chats yet.</p>
        ) : (
          <ul className="flex flex-col gap-0.5">
            {conversations.map((c) => (
              <ConversationRow
                key={c.id}
                conversation={c}
                active={c.id === activeId}
                onOpen={() => onOpen(c.id)}
                onRename={(title) => onRename(c.id, title)}
                onDelete={() => onDelete(c.id)}
              />
            ))}
          </ul>
        )}
      </div>
    </div>
  )
}

/* Row actions show on touch screens always; with a mouse, on hover or focus. */
const ROW_ACTION =
  "flex size-8 shrink-0 items-center justify-center rounded-lg text-muted-foreground transition-opacity lg:opacity-0 lg:group-hover:opacity-100 lg:group-focus-within:opacity-100"

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
      <li className="flex items-center gap-1 rounded-xl bg-surface-2 p-1">
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
          aria-label="Chat title"
          className="min-w-0 flex-1 rounded-lg bg-surface px-2.5 py-1.5 text-[15px] focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring"
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
        "group flex min-h-[44px] items-center gap-0.5 rounded-xl px-1 transition-colors",
        active ? "bg-primary/10" : "hover:bg-surface-2",
      )}
    >
      <button
        onClick={onOpen}
        className={cn("min-w-0 flex-1 truncate px-2 py-2.5 text-left text-[15px]", active && "font-semibold")}
      >
        {conversation.title || "New chat"}
      </button>
      <button
        aria-label="Rename chat"
        onClick={() => {
          setDraft(conversation.title)
          setEditing(true)
        }}
        className={cn(ROW_ACTION, "hover:text-foreground", active && "lg:opacity-100")}
      >
        <Pencil className="size-3.5" />
      </button>
      <button
        aria-label="Delete chat"
        onClick={onDelete}
        className={cn(ROW_ACTION, "hover:text-danger", active && "lg:opacity-100")}
      >
        <Trash2 className="size-3.5" />
      </button>
    </li>
  )
}
