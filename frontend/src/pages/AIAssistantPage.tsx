import { useEffect, useRef, useState, type FormEvent } from "react"
import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query"
import {
  BookOpenText,
  CheckCheck,
  HelpCircle,
  Loader2,
  MessageCircle,
  MessageSquarePlus,
  PanelLeft,
  Send,
  SlidersHorizontal,
  Sparkles,
  Theater,
} from "lucide-react"
import { isAxiosError } from "axios"

import {
  createConversation,
  deleteConversation,
  fetchConversation,
  fetchConversations,
  renameConversation,
  retryLastAnswer,
  sendMessage,
  setPinned,
} from "@/api/conversations"
import { fetchStarters } from "@/api/ai"
import type { ChatMode, ChatStarter } from "@/types"
import { Button } from "@/components/ui/button"
import { AISettingsDialog } from "@/components/ai/AISettingsDialog"
import { ChatMessage } from "@/components/ai/ChatMessage"
import { MicButton } from "@/components/ai/MicButton"
import { ConversationSidebar } from "@/components/ai/ConversationSidebar"
import { cn } from "@/lib/utils"

/*
 * AI Assistant: saved chats in a list you can hide (a drawer on phones), the
 * open chat on the right. Learning tools (quiz, correct my text, role-play,
 * explain) switch how the tutor answers; starters come from what you've
 * learned; "Personalise" sets the tutor's language, tone and corrections.
 * Premium only (checked by the route and by the API).
 */
const MODES: { id: ChatMode; label: string; icon: typeof MessageCircle; placeholder: string }[] = [
  { id: "chat", label: "Chat", icon: MessageCircle, placeholder: "Ask about German…" },
  { id: "quiz", label: "Quiz me", icon: HelpCircle, placeholder: "Answer, or say what to be quizzed on…" },
  { id: "correct", label: "Correct my text", icon: CheckCheck, placeholder: "Write German to check…" },
  { id: "roleplay", label: "Role-play", icon: Theater, placeholder: "Say what situation, or start talking…" },
  { id: "explain", label: "Explain", icon: BookOpenText, placeholder: "Which grammar should I explain?" },
]

const LIST_KEY = "ai.chatList" // remembered per browser: "open" | "closed"

function readListOpen(): boolean {
  try {
    return localStorage.getItem(LIST_KEY) !== "closed"
  } catch {
    return true
  }
}

export default function AIAssistantPage() {
  const qc = useQueryClient()
  const [activeId, setActiveId] = useState<number | null>(null)
  const [input, setInput] = useState("")
  const [mode, setMode] = useState<ChatMode>("chat")
  const [error, setError] = useState("")
  const [query, setQuery] = useState("")
  const [listOpen, setListOpen] = useState(readListOpen) // wide screens
  const [drawerOpen, setDrawerOpen] = useState(false) // phones
  const [settingsOpen, setSettingsOpen] = useState(false)
  const scrollRef = useRef<HTMLDivElement>(null)
  const inputRef = useRef<HTMLTextAreaElement>(null)

  const { data: conversations } = useQuery({
    queryKey: ["conversations", query.trim()],
    queryFn: () => fetchConversations(query.trim()),
    placeholderData: (previous) => previous,
  })
  const { data: thread } = useQuery({
    queryKey: ["conversation", activeId],
    queryFn: () => fetchConversation(activeId!),
    enabled: activeId !== null,
  })
  const { data: starters } = useQuery({ queryKey: ["ai-starters"], queryFn: fetchStarters })

  const messages = thread?.messages ?? []

  function toggleList() {
    if (window.matchMedia("(min-width: 1024px)").matches) {
      const next = !listOpen
      setListOpen(next)
      try {
        localStorage.setItem(LIST_KEY, next ? "open" : "closed")
      } catch {
        /* storage blocked: the choice just isn't remembered */
      }
    } else {
      setDrawerOpen((v) => !v)
    }
  }

  function showError(err: unknown) {
    setError(
      isAxiosError(err) && err.response?.status === 503
        ? "AI is not configured yet. Add GEMINI_API_KEY to backend/.env to enable it."
        : "Something went wrong. Please try again.",
    )
  }

  const send = useMutation({
    mutationFn: async ({ text, as }: { text: string; as: ChatMode }) => {
      // First message with no chat open? Start one, then send into it.
      const id = activeId ?? (await createConversation()).id
      if (activeId === null) setActiveId(id)
      return sendMessage(id, text, as)
    },
    onSuccess: (res) => {
      setError("")
      qc.invalidateQueries({ queryKey: ["conversation", res.conversation.id] })
      qc.invalidateQueries({ queryKey: ["conversations"] })
    },
    onError: showError,
  })

  const retry = useMutation({
    mutationFn: () => retryLastAnswer(activeId!),
    onSuccess: () => {
      setError("")
      qc.invalidateQueries({ queryKey: ["conversation", activeId] })
    },
    onError: showError,
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
  const pin = useMutation({
    mutationFn: ({ id, pinned }: { id: number; pinned: boolean }) => setPinned(id, pinned),
    onSuccess: () => qc.invalidateQueries({ queryKey: ["conversations"] }),
  })

  useEffect(() => {
    scrollRef.current?.scrollTo({ top: scrollRef.current.scrollHeight })
  }, [messages.length, send.isPending])

  function submit(e?: FormEvent) {
    e?.preventDefault()
    const text = input.trim()
    if (!text || send.isPending) return
    setInput("")
    send.mutate({ text, as: mode })
  }

  function startFrom(s: ChatStarter) {
    setMode(s.mode)
    if (s.send) send.mutate({ text: s.message, as: s.mode })
    else inputRef.current?.focus()
  }

  function newChat() {
    setActiveId(null)
    setMode("chat")
    setDrawerOpen(false)
  }

  const sidebar = (onClose?: () => void) => (
    <ConversationSidebar
      conversations={conversations ?? []}
      activeId={activeId}
      query={query}
      onQuery={setQuery}
      onNew={newChat}
      onOpen={(id) => {
        setActiveId(id)
        // A chat opens with the tool it was last used with.
        setMode(conversations?.find((c) => c.id === id)?.mode ?? "chat")
        setDrawerOpen(false)
      }}
      onRename={(id, title) => rename.mutate({ id, title })}
      onPin={(id, pinned) => pin.mutate({ id, pinned })}
      onDelete={(id) => remove.mutate(id)}
      onClose={onClose}
    />
  )

  const lastAnswerId = [...messages].reverse().find((m) => m.role === "assistant")?.id
  const lastIsAnswer = messages.length > 0 && messages[messages.length - 1].role === "assistant"
  const current = MODES.find((m) => m.id === mode) ?? MODES[0]

  return (
    <div className="flex h-[calc(100svh-12.5rem)] min-h-[420px] flex-col gap-3 lg:h-[calc(100vh-9rem)]">
      <div className="flex items-center gap-2">
        <Button
          variant="secondary"
          size="icon"
          onClick={toggleList}
          aria-label={listOpen ? "Hide chat list" : "Show chat list"}
          aria-expanded={drawerOpen || listOpen}
          title="Chats"
        >
          <PanelLeft />
        </Button>
        <h1 className="min-w-0 flex-1 truncate text-2xl font-extrabold">AI Assistant</h1>
        <Button variant="secondary" size="sm" onClick={() => setSettingsOpen(true)}>
          <SlidersHorizontal /> <span className="hidden sm:inline">Personalise</span>
        </Button>
        <Button size="icon" aria-label="New chat" title="New chat" onClick={newChat}>
          <MessageSquarePlus />
        </Button>
      </div>

      <div className="flex min-h-0 flex-1 gap-5">
        {/* Wide screens: a side card you can hide. */}
        {listOpen && <aside className="hidden w-64 shrink-0 lg:flex">{sidebar()}</aside>}

        {/* Phones: the list slides in as a drawer. */}
        {drawerOpen && (
          <div className="fixed inset-0 z-40 flex lg:hidden" role="dialog" aria-modal="true" aria-label="Chats">
            <div className="absolute inset-0 bg-black/40 animate-in fade-in-0 duration-150" onClick={() => setDrawerOpen(false)} aria-hidden="true" />
            <div className="relative h-full w-[min(20rem,85vw)] p-3 animate-in slide-in-from-left duration-200">
              {sidebar(() => setDrawerOpen(false))}
            </div>
          </div>
        )}

        {/* Thread */}
        <div className="flex min-w-0 flex-1 flex-col">
          <div ref={scrollRef} className="min-h-0 flex-1 overflow-y-auto">
            {messages.length === 0 && !send.isPending ? (
              <div className="flex h-full flex-col items-center justify-center gap-3 px-2 py-8 text-center">
                <span className="flex size-16 items-center justify-center rounded-2xl bg-[hsl(var(--section-3))] text-white">
                  <Sparkles className="size-8" aria-hidden="true" />
                </span>
                <h2 className="mt-2 text-3xl font-extrabold">Ask me anything about German</h2>
                <p className="max-w-md text-muted-foreground">
                  Pick a tool below, or start from what you've learned. Your chats are saved.
                </p>
                <div className="mt-4 grid w-full max-w-2xl gap-2.5 sm:grid-cols-2 lg:grid-cols-3">
                  {(starters ?? []).map((s) => (
                    <button
                      key={s.label}
                      onClick={() => startFrom(s)}
                      className="lift min-h-[64px] rounded-2xl bg-surface p-4 text-left text-[15px] font-medium shadow-card"
                    >
                      {s.label}
                    </button>
                  ))}
                </div>
              </div>
            ) : (
              <div className="mx-auto flex max-w-3xl flex-col gap-4 pb-4 pt-1">
                {messages.map((m) => (
                  <ChatMessage
                    key={m.id}
                    message={m}
                    canRetry={m.id === lastAnswerId && lastIsAnswer && !send.isPending}
                    retrying={retry.isPending}
                    onRetry={() => retry.mutate()}
                  />
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

          {/* Learning tools: how the tutor answers the next message. */}
          <div className="mx-auto mt-2 flex w-full max-w-3xl gap-1.5 overflow-x-auto pb-1" role="radiogroup" aria-label="Learning tool">
            {MODES.map(({ id, label, icon: Icon }) => (
              <button
                key={id}
                type="button"
                role="radio"
                aria-checked={mode === id}
                onClick={() => setMode(id)}
                className={cn(
                  "inline-flex h-9 shrink-0 items-center gap-1.5 rounded-full border-2 px-3 text-sm font-semibold transition-colors",
                  mode === id
                    ? "border-[hsl(var(--choice))] bg-[hsl(var(--choice-bg))]"
                    : "border-transparent bg-surface-2 text-muted-foreground hover:text-foreground",
                )}
              >
                <Icon className="size-4" aria-hidden="true" /> {label}
              </button>
            ))}
          </div>

          <form
            onSubmit={submit}
            className="mx-auto mt-1 flex w-full max-w-3xl items-end gap-2 rounded-[24px] bg-surface p-1.5 pl-5 shadow-card focus-within:ring-2 focus-within:ring-ring"
          >
            <textarea
              ref={inputRef}
              value={input}
              rows={mode === "correct" ? 3 : 1}
              onChange={(e) => setInput(e.target.value)}
              onKeyDown={(e) => {
                if (e.key === "Enter" && !e.shiftKey) {
                  e.preventDefault()
                  submit()
                }
              }}
              placeholder={current.placeholder}
              aria-label="Message the AI tutor"
              className="max-h-40 min-w-0 flex-1 resize-none bg-transparent py-2.5 text-base placeholder:text-muted-foreground focus-visible:outline-none"
            />
            <MicButton onText={(text) => setInput((prev) => (prev.trim() ? `${prev.trim()} ${text}` : text))} />
            <Button type="submit" size="icon" aria-label="Send" className="shrink-0" disabled={send.isPending || !input.trim()}>
              <Send />
            </Button>
          </form>
        </div>
      </div>

      {settingsOpen && <AISettingsDialog onClose={() => setSettingsOpen(false)} />}
    </div>
  )
}
