import { useState, type FormEvent } from "react"
import { Link } from "react-router-dom"
import { useQueryClient } from "@tanstack/react-query"
import { ArrowRight, Sparkles } from "lucide-react"

import { askLessonGuide, createCustomLesson } from "@/api/history"
import { useAuth } from "@/contexts/AuthContext"
import { errorText } from "@/lib/apiError"
import { cn } from "@/lib/utils"
import { Button } from "@/components/ui/button"
import { Card } from "@/components/ui/card"
import { Input } from "@/components/ui/input"

type Message = { role: "user" | "assistant"; content: string }

/*
 * "Ask for a lesson" (premium): the learner says what they'd like to read
 * about, the AI may ask a follow-up question or decline anything that isn't
 * about Germany or the German language, and once the topic is clear it writes
 * a lesson at the learner's level. The rules are enforced on the server
 * (history/custom.py); this is only the conversation.
 */
export function LessonBuilder({ onCreated }: { onCreated: (id: number) => void }) {
  const { user } = useAuth()
  const qc = useQueryClient()
  const [messages, setMessages] = useState<Message[]>([])
  const [input, setInput] = useState("")
  const [topic, setTopic] = useState("")
  const [busy, setBusy] = useState<"asking" | "writing" | null>(null)
  const [error, setError] = useState<string | null>(null)

  if (!user?.has_premium) {
    return (
      <Card className="flex flex-col gap-4 p-6 sm:flex-row sm:items-center">
        <div className="flex-1">
          <h2 className="text-xl font-bold">Ask for a lesson</h2>
          <p className="mt-1 text-sm text-muted-foreground">
            With Premium, ask for a lesson on any German topic and the AI writes it at your
            level, with a picture and a quiz.
          </p>
        </div>
        <Button asChild variant="secondary">
          <Link to="/ai">See Premium</Link>
        </Button>
      </Card>
    )
  }

  function reset() {
    setMessages([])
    setTopic("")
    setError(null)
    setInput("")
  }

  async function send(e: FormEvent) {
    e.preventDefault()
    const text = input.trim()
    if (!text || busy) return
    const next: Message[] = [...messages, { role: "user", content: text }]
    setMessages(next)
    setInput("")
    setError(null)
    setBusy("asking")
    try {
      const res = await askLessonGuide(next)
      setMessages([...next, { role: "assistant", content: res.reply }])
      setTopic(res.status === "ready" ? res.topic : "")
    } catch (err) {
      setError(errorText(err))
      setMessages(messages)
    } finally {
      setBusy(null)
    }
  }

  async function write() {
    setBusy("writing")
    setError(null)
    try {
      const lesson = await createCustomLesson(topic)
      qc.invalidateQueries({ queryKey: ["history"] })
      reset()
      onCreated(lesson.id)
    } catch (err) {
      setError(errorText(err))
    } finally {
      setBusy(null)
    }
  }

  return (
    <Card className="p-6">
      <div className="flex items-start justify-between gap-3">
        <div>
          <h2 className="flex items-center gap-2 text-xl font-bold">
            <Sparkles className="size-5 text-primary" aria-hidden="true" /> Ask for a lesson
          </h2>
          <p className="mt-1 text-sm text-muted-foreground">
            Anything about Germany, its history and culture, or the German language. The AI
            writes it at your level ({user.cefr_level}), with a picture and a quiz.
          </p>
        </div>
        {messages.length > 0 && !busy && (
          <button onClick={reset} className="shrink-0 text-sm text-muted-foreground underline">
            Start over
          </button>
        )}
      </div>

      {messages.length > 0 && (
        <ul className="mt-5 flex flex-col gap-2">
          {messages.map((m, i) => (
            <li
              key={i}
              className={cn(
                "max-w-[85%] rounded-2xl px-4 py-2.5 text-sm",
                m.role === "user"
                  ? "self-end bg-primary text-primary-foreground"
                  : "self-start bg-surface-2",
              )}
            >
              {m.content}
            </li>
          ))}
          {busy === "asking" && (
            <li className="self-start rounded-2xl bg-surface-2 px-4 py-2.5 text-sm text-muted-foreground">
              Thinking…
            </li>
          )}
        </ul>
      )}

      {topic ? (
        <div className="mt-5 flex flex-col gap-3 rounded-2xl bg-surface-2 p-4 sm:flex-row sm:items-center">
          <p className="flex-1 text-sm">
            Lesson topic: <span className="font-semibold">{topic}</span>
          </p>
          <Button onClick={write} disabled={!!busy}>
            {busy === "writing" ? "Writing your lesson…" : "Write the lesson"}
            {busy !== "writing" && <ArrowRight />}
          </Button>
        </div>
      ) : (
        <form onSubmit={send} className="mt-5 flex gap-2">
          <Input
            value={input}
            onChange={(e) => setInput(e.target.value)}
            maxLength={500}
            placeholder={
              messages.length ? "Your answer" : "e.g. the Brothers Grimm, Oktoberfest, Bauhaus"
            }
            aria-label="What would you like a lesson about?"
            disabled={!!busy}
          />
          <Button type="submit" disabled={!input.trim() || !!busy}>
            Send
          </Button>
        </form>
      )}

      {busy === "writing" && (
        <p className="mt-3 text-xs text-muted-foreground">This takes about half a minute.</p>
      )}
      {error && <p className="mt-3 text-sm text-[hsl(var(--danger))]">{error}</p>}
    </Card>
  )
}
