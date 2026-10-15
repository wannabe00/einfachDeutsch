import { useState } from "react"
import { Check, MessageSquarePlus, Pencil, Pin, PinOff, Search, Trash2, X } from "lucide-react"

import type { Conversation } from "@/types"
import { cn } from "@/lib/utils"
import { Button } from "@/components/ui/button"

/*
 * The AI page's list of saved chats: New chat, a search over titles and what
 * was said (done by the server), pinned chats on top, then the rest. Each row
 * can be pinned, renamed or deleted.
 */
export function ConversationSidebar({
  conversations,
  activeId,
  query,
  onQuery,
  onNew,
  onOpen,
  onRename,
  onPin,
  onDelete,
  onClose,
}: {
  conversations: Conversation[]
  activeId: number | null
  query: string
  onQuery: (q: string) => void
  onNew: () => void
  onOpen: (id: number) => void
  onRename: (id: number, title: string) => void
  onPin: (id: number, pinned: boolean) => void
  onDelete: (id: number) => void
  /** Phones: close the drawer. */
  onClose?: () => void
}) {
  const pinned = conversations.filter((c) => c.pinned)
  const rest = conversations.filter((c) => !c.pinned)

  const row = (c: Conversation) => (
    <ConversationRow
      key={c.id}
      conversation={c}
      active={c.id === activeId}
      onOpen={() => onOpen(c.id)}
      onRename={(title) => onRename(c.id, title)}
      onPin={() => onPin(c.id, !c.pinned)}
      onDelete={() => onDelete(c.id)}
    />
  )

  return (
    <div className="flex h-full min-h-0 w-full flex-col rounded-[24px] bg-surface p-3 shadow-card">
      <div className="flex gap-2">
        <Button className="flex-1" onClick={onNew}>
          <MessageSquarePlus /> New chat
        </Button>
        {onClose && (
          <Button variant="secondary" size="icon" aria-label="Close chat list" onClick={onClose}>
            <X />
          </Button>
        )}
      </div>
      <label className="mt-3 flex h-10 items-center gap-2 rounded-xl bg-surface-2 px-3 focus-within:ring-2 focus-within:ring-ring">
        <Search className="size-4 shrink-0 text-muted-foreground" aria-hidden="true" />
        <input
          value={query}
          onChange={(e) => onQuery(e.target.value)}
          placeholder="Search chats"
          aria-label="Search chats"
          className="min-w-0 flex-1 bg-transparent text-[15px] placeholder:text-muted-foreground focus-visible:outline-none"
        />
      </label>
      <div className="mt-2 min-h-0 flex-1 overflow-y-auto">
        {conversations.length === 0 ? (
          <p className="px-2 py-3 text-sm text-muted-foreground">{query ? "No chats match." : "No chats yet."}</p>
        ) : (
          <>
            {pinned.length > 0 && (
              <>
                <Heading>Pinned</Heading>
                <ul className="flex flex-col gap-0.5">{pinned.map(row)}</ul>
              </>
            )}
            {rest.length > 0 && (
              <>
                <Heading>{query ? "Results" : "Your chats"}</Heading>
                <ul className="flex flex-col gap-0.5">{rest.map(row)}</ul>
              </>
            )}
          </>
        )}
      </div>
    </div>
  )
}

function Heading({ children }: { children: React.ReactNode }) {
  return (
    <p className="mt-3 px-2 pb-1 text-[13px] font-semibold uppercase tracking-[0.04em] text-muted-foreground first:mt-1">
      {children}
    </p>
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
  onPin,
  onDelete,
}: {
  conversation: Conversation
  active: boolean
  onOpen: () => void
  onRename: (title: string) => void
  onPin: () => void
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
        aria-label={conversation.pinned ? "Unpin chat" : "Pin chat"}
        onClick={onPin}
        className={cn(ROW_ACTION, "hover:text-foreground", (active || conversation.pinned) && "lg:opacity-100")}
      >
        {conversation.pinned ? <PinOff className="size-3.5" /> : <Pin className="size-3.5" />}
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
