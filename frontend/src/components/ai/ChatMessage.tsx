import { useRef, useState, type FormEvent } from "react"
import { useMutation, useQueryClient } from "@tanstack/react-query"
import ReactMarkdown from "react-markdown"
import remarkGfm from "remark-gfm"
import { BookmarkPlus, Check, Copy, Loader2, RotateCcw, Square, Volume2 } from "lucide-react"

import type { ConversationMessage } from "@/types"
import { readAloud } from "@/api/ai"
import { saveWord } from "@/api/vocabulary"
import { errorText } from "@/lib/apiError"
import { cn } from "@/lib/utils"

/*
 * One chat bubble. Every message can be read aloud (the selected text, or all
 * of it; Azure's multilingual voice reads English and German each correctly).
 * The tutor's answers also get copy, save a word to the Word Bank (the
 * selected text or the first bold word) and, on the last answer, retry.
 */

// One message plays at a time, across all bubbles.
let playing: { audio: HTMLAudioElement; stop: () => void } | null = null

/** The bold parts of an answer: the tutor puts German examples in **bold**. */
function boldParts(markdown: string): string[] {
  return [...markdown.matchAll(/\*\*(.+?)\*\*/g)].map((m) => m[1].trim()).filter(Boolean)
}

function selectionIn(el: HTMLElement | null): string {
  const sel = window.getSelection()
  if (!el || !sel || sel.isCollapsed || !el.contains(sel.anchorNode)) return ""
  return sel.toString().trim()
}

export function ChatMessage({
  message,
  canRetry,
  retrying,
  onRetry,
}: {
  message: ConversationMessage
  canRetry: boolean
  retrying: boolean
  onRetry: () => void
}) {
  const bubbleRef = useRef<HTMLDivElement>(null)
  const [copied, setCopied] = useState(false)
  const [saving, setSaving] = useState<string | null>(null)
  const mine = message.role === "user"

  const [speaking, setSpeaking] = useState(false)
  const voice = useMutation({
    mutationFn: readAloud,
    onSuccess: (mp3) => {
      playing?.stop()
      const url = URL.createObjectURL(mp3)
      const audio = new Audio(url)
      const stop = () => {
        audio.pause()
        URL.revokeObjectURL(url)
        setSpeaking(false)
        if (playing?.audio === audio) playing = null
      }
      audio.onended = stop
      playing = { audio, stop }
      setSpeaking(true)
      void audio.play().catch(stop)
    },
  })

  function toggleVoice() {
    if (speaking) return playing?.stop()
    const text = selectionIn(bubbleRef.current) || bubbleRef.current?.innerText || message.content
    voice.mutate(text.trim())
  }

  async function copy() {
    try {
      await navigator.clipboard.writeText(message.content)
      setCopied(true)
      window.setTimeout(() => setCopied(false), 1500)
    } catch {
      /* clipboard blocked: nothing to do */
    }
  }

  return (
    <div className={cn("flex flex-col animate-in fade-in-0 slide-in-from-bottom-1 duration-200", mine ? "items-end" : "items-start")}>
      <div
        ref={bubbleRef}
        className={cn(
          "max-w-[85%] rounded-[22px] px-4 py-3 text-[15px] leading-relaxed",
          mine ? "rounded-br-md bg-primary text-primary-foreground" : "rounded-bl-md bg-surface text-foreground shadow-card",
          "[&_code]:rounded [&_code]:bg-surface-2 [&_code]:px-1 [&_code]:font-mono",
          "[&_table]:my-2 [&_table]:w-full [&_table]:border-collapse",
          "[&_th]:border [&_th]:border-border [&_th]:px-2 [&_th]:py-1 [&_th]:text-left",
          "[&_td]:border [&_td]:border-border [&_td]:px-2 [&_td]:py-1",
          "[&_p]:my-1.5 [&_ul]:my-1.5 [&_ul]:list-disc [&_ul]:pl-5 [&_ol]:my-1.5 [&_ol]:list-decimal [&_ol]:pl-5 [&_strong]:font-semibold",
        )}
      >
        <ReactMarkdown remarkPlugins={[remarkGfm]}>{message.content}</ReactMarkdown>
      </div>

      <div className={cn("mt-1 flex flex-wrap items-center gap-0.5", mine ? "pr-1" : "pl-1")}>
        <Action
          label={speaking ? "Stop" : voice.isPending ? "Loading…" : voice.isError ? errorText(voice.error) : "Read aloud"}
          onClick={toggleVoice}
          disabled={voice.isPending}
        >
          {speaking ? <Square /> : voice.isPending ? <Loader2 className="animate-spin" /> : <Volume2 />}
        </Action>
        {!mine && (
          <>
            <Action label={copied ? "Copied" : "Copy"} onClick={copy}>
              {copied ? <Check /> : <Copy />}
            </Action>
            <Action
              label="Save a word"
              onClick={() => setSaving(selectionIn(bubbleRef.current) || boldParts(message.content)[0] || "")}
            >
              <BookmarkPlus />
            </Action>
            {canRetry && (
              <Action label={retrying ? "Retrying…" : "Retry"} onClick={onRetry} disabled={retrying}>
                <RotateCcw className={cn(retrying && "animate-spin")} />
              </Action>
            )}
          </>
        )}
      </div>
      {saving !== null && <SaveWordForm initial={saving} onClose={() => setSaving(null)} />}
    </div>
  )
}

function Action({
  label,
  onClick,
  disabled,
  children,
}: {
  label: string
  onClick: () => void
  disabled?: boolean
  children: React.ReactNode
}) {
  return (
    <button
      type="button"
      onClick={onClick}
      disabled={disabled}
      aria-label={label}
      title={label}
      className="flex size-8 items-center justify-center rounded-lg text-muted-foreground transition-colors hover:bg-surface-2 hover:text-foreground disabled:opacity-50 [&_svg]:size-4"
    >
      {children}
    </button>
  )
}

/** Save a word from the chat to the learner's own words in the Word Bank. */
function SaveWordForm({ initial, onClose }: { initial: string; onClose: () => void }) {
  const qc = useQueryClient()
  const [german, setGerman] = useState(initial)
  const [english, setEnglish] = useState("")
  const save = useMutation({
    mutationFn: () => saveWord({ german: german.trim(), english: english.trim() }),
    onSuccess: () => {
      qc.invalidateQueries({ queryKey: ["saved-words"] })
      window.setTimeout(onClose, 900)
    },
  })

  function submit(e: FormEvent) {
    e.preventDefault()
    if (german.trim() && !save.isPending) save.mutate()
  }

  const field =
    "h-10 min-w-0 flex-1 rounded-xl bg-surface-2 px-3 text-[15px] placeholder:text-muted-foreground focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring"
  return (
    <form onSubmit={submit} className="mt-2 flex w-full max-w-[85%] flex-col gap-2 rounded-2xl bg-surface p-3 shadow-card">
      <p className="text-sm font-semibold">Save to your Word Bank</p>
      <div className="flex flex-col gap-2 sm:flex-row">
        <input autoFocus value={german} onChange={(e) => setGerman(e.target.value)} placeholder="German (e.g. der Tisch)" aria-label="German" className={field} />
        <input value={english} onChange={(e) => setEnglish(e.target.value)} placeholder="English (optional)" aria-label="English" className={field} />
      </div>
      <div className="flex items-center gap-2">
        <button
          type="submit"
          disabled={!german.trim() || save.isPending || save.isSuccess}
          className="inline-flex h-9 items-center gap-1.5 rounded-full bg-primary px-4 text-sm font-semibold text-primary-foreground disabled:opacity-50"
        >
          {save.isSuccess ? (
            <>
              <Check className="size-4" /> Saved
            </>
          ) : save.isPending ? (
            "Saving…"
          ) : (
            "Save"
          )}
        </button>
        <button type="button" onClick={onClose} className="h-9 rounded-full px-3 text-sm font-semibold text-muted-foreground hover:text-foreground">
          Cancel
        </button>
        {save.isError && <span className="text-sm text-danger">{errorText(save.error)}</span>}
      </div>
    </form>
  )
}
