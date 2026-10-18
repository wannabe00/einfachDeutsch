import { useEffect, useRef, useState } from "react"
import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query"
import { ArrowLeft, Check, Mic, PhoneOff, Trash2 } from "lucide-react"

import { fetchTalk, fetchTalks, finishTalk, removeTalks, startTalk } from "@/api/talk"
import type { TalkDetail, TalkReport, TalkStart, TalkSummary, TalkTurn } from "@/types"
import { errorText } from "@/lib/apiError"
import { liveTalkSupported, startLiveTalk, type LiveState, type LiveTalk } from "@/lib/liveTalk"
import { cn } from "@/lib/utils"
import { PageHeader } from "@/components/layout/PageHeader"
import { Button } from "@/components/ui/button"
import { Card } from "@/components/ui/card"

/*
 * Talk to AI (premium): one button starts a spoken conversation with Gemini
 * (see lib/liveTalk). The AI greets you and you decide what to talk about.
 * Afterwards you read the report; past talks are listed under the button.
 */
type Screen = { kind: "pick" } | { kind: "call"; start: TalkStart } | { kind: "report"; talk: TalkDetail }

export default function TalkPage() {
  const [screen, setScreen] = useState<Screen>({ kind: "pick" })

  if (screen.kind === "call")
    return <Call start={screen.start} onDone={(talk) => setScreen({ kind: "report", talk })} />
  if (screen.kind === "report")
    return <Report talk={screen.talk} onBack={() => setScreen({ kind: "pick" })} />
  return (
    <Pick
      onStart={(start) => setScreen({ kind: "call", start })}
      onOpen={(talk) => setScreen({ kind: "report", talk })}
    />
  )
}

function Pick({ onStart, onOpen }: { onStart: (s: TalkStart) => void; onOpen: (t: TalkDetail) => void }) {
  const talks = useQuery({ queryKey: ["talks"], queryFn: fetchTalks })
  const start = useMutation({ mutationFn: startTalk, onSuccess: onStart })
  const open = useMutation({ mutationFn: fetchTalk, onSuccess: onOpen })

  return (
    <div className="flex flex-col gap-8">
      <PageHeader title="Sprechen" />
      <Card className="flex flex-col items-center gap-5 p-8 text-center">
        <span className="flex size-20 items-center justify-center rounded-full bg-primary text-primary-foreground">
          <Mic className="size-9" aria-hidden="true" />
        </span>
        <div className="max-w-md">
          <p className="text-lg font-bold">Speak German with Tako, your AI partner</p>
          <p className="mt-1 text-muted-foreground">
            Tako greets you, and you decide what to talk about: your own topic, one it suggests, or a
            short Vorstellung like in the Goethe exam. Afterwards you get a report with your mistakes
            and new words.
          </p>
        </div>
        {liveTalkSupported ? (
          <Button size="lg" className="w-full max-w-xs" disabled={start.isPending} onClick={() => start.mutate()}>
            <Mic className="size-4" aria-hidden="true" />
            {start.isPending ? "Connecting…" : "Start talking"}
          </Button>
        ) : (
          <p className="text-sm">This browser can't do live voice. Please use a recent Chrome, Edge, Firefox or Safari.</p>
        )}
        {start.isError && <p className="text-sm text-[hsl(var(--danger))]">{errorText(start.error)}</p>}
      </Card>

      {!!talks.data?.length && <History talks={talks.data} onOpen={(id) => open.mutate(id)} />}
    </div>
  )
}

/** Your past talks. "Select" turns the list into checkboxes; the bar at the
    bottom removes the chosen talks after one confirmation. */
function History({ talks, onOpen }: { talks: TalkSummary[]; onOpen: (id: number) => void }) {
  const queryClient = useQueryClient()
  const [selecting, setSelecting] = useState(false)
  const [chosen, setChosen] = useState<Set<number>>(new Set())
  const [confirming, setConfirming] = useState(false)
  const remove = useMutation({
    mutationFn: () => removeTalks([...chosen]),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ["talks"] })
      done()
    },
  })

  function done() {
    setSelecting(false)
    setChosen(new Set())
    setConfirming(false)
  }

  function toggle(id: number) {
    setConfirming(false)
    setChosen((c) => {
      const next = new Set(c)
      if (next.has(id)) next.delete(id)
      else next.add(id)
      return next
    })
  }

  const all = chosen.size === talks.length
  const n = chosen.size

  return (
    <section className={cn(selecting && "pb-28")}>
      <div className="mb-3 flex items-center justify-between px-1">
        <h2 className="text-[22px] font-bold">Your talks</h2>
        <Button variant="ghost" size="sm" onClick={() => (selecting ? done() : setSelecting(true))}>
          {selecting ? "Done" : "Select"}
        </Button>
      </div>
      <ul className="flex flex-col gap-2" aria-label="Your talks">
        {talks.map((t) => {
          const on = chosen.has(t.id)
          return (
            <li key={t.id}>
              <button
                type="button"
                onClick={() => (selecting ? toggle(t.id) : onOpen(t.id))}
                aria-pressed={selecting ? on : undefined}
                className={cn(
                  "flex w-full items-center gap-3 rounded-2xl border-2 p-4 text-left shadow-card transition-colors",
                  on
                    ? "border-[hsl(var(--choice))] bg-[hsl(var(--choice-bg))]"
                    : "border-transparent bg-surface hover:bg-surface-2",
                )}
              >
                {selecting && (
                  <span
                    className={cn(
                      "flex size-6 shrink-0 items-center justify-center rounded-full border-2 transition-colors",
                      on ? "border-[hsl(var(--choice))] bg-[hsl(var(--choice))] text-white" : "border-border",
                    )}
                    aria-hidden="true"
                  >
                    {on && <Check className="size-4" strokeWidth={3} />}
                  </span>
                )}
                <span className="min-w-0 flex-1">
                  <span className="block text-sm font-semibold">{new Date(t.started_at).toLocaleString()}</span>
                  {t.summary && <span className="mt-0.5 line-clamp-2 block text-sm text-muted-foreground">{t.summary}</span>}
                </span>
              </button>
            </li>
          )
        })}
      </ul>

      {selecting && (
        <div className="fixed inset-x-0 bottom-[calc(76px+env(safe-area-inset-bottom))] z-40 px-4 lg:bottom-6">
          <div className="glass mx-auto flex max-w-xl items-center gap-2 rounded-[22px] border border-border/60 p-2.5 pl-4 shadow-lift animate-in fade-in-0 slide-in-from-bottom-3 duration-200">
            {confirming ? (
              <>
                <p className="flex-1 text-sm font-semibold">
                  Remove {n} {n === 1 ? "talk" : "talks"} for good?
                </p>
                <Button size="sm" variant="ghost" onClick={() => setConfirming(false)} disabled={remove.isPending}>
                  Keep
                </Button>
                <Button size="sm" variant="destructive" onClick={() => remove.mutate()} disabled={remove.isPending}>
                  {remove.isPending ? "Removing…" : "Remove"}
                </Button>
              </>
            ) : (
              <>
                <p className="flex-1 text-sm text-muted-foreground" aria-live="polite">
                  {n ? `${n} selected` : "Tap talks to select them"}
                </p>
                <Button
                  size="sm"
                  variant="ghost"
                  onClick={() => setChosen(all ? new Set() : new Set(talks.map((t) => t.id)))}
                >
                  {all ? "Select none" : "Select all"}
                </Button>
                <Button size="sm" variant="destructive" disabled={!n} onClick={() => setConfirming(true)}>
                  <Trash2 className="size-4" aria-hidden="true" />
                  Remove{n ? ` (${n})` : ""}
                </Button>
              </>
            )}
          </div>
          {remove.isError && (
            <p className="mt-2 text-center text-sm text-[hsl(var(--danger))]">{errorText(remove.error)}</p>
          )}
        </div>
      )}
    </section>
  )
}

const LABEL: Record<LiveState, string> = {
  connecting: "Connecting…",
  starting: "Tako is starting…",
  listening: "Your turn: speak",
  speaking: "Tako is speaking",
  ended: "Ending…",
}

function Call({ start, onDone }: { start: TalkStart; onDone: (t: TalkDetail) => void }) {
  const queryClient = useQueryClient()
  const live = useRef<LiveTalk | null>(null)
  const [state, setState] = useState<LiveState>("connecting")
  const [turns, setTurns] = useState<TalkTurn[]>([])
  const [captions, setCaptions] = useState(false)
  const [seconds, setSeconds] = useState(0)
  const [problem, setProblem] = useState<string | null>(null)
  const [connected, setConnected] = useState(false)
  const limit = start.minutes * 60

  const finish = useMutation({
    mutationFn: (transcript: TalkTurn[]) => finishTalk(start.id, transcript),
    onSuccess: (talk) => {
      queryClient.invalidateQueries({ queryKey: ["talks"] })
      onDone(talk)
    },
  })

  function hangUp() {
    if (!live.current) return
    const transcript = live.current.stop()
    live.current = null
    setConnected(false)
    finish.mutate(transcript)
  }

  useEffect(() => {
    let cancelled = false
    startLiveTalk(start.token, start.model, {
      onState: setState,
      onTurns: setTurns,
      onError: (m) => setProblem(m),
    })
      .then((talk) => {
        if (cancelled) talk.stop()
        else {
          live.current = talk
          setConnected(true)
        }
      })
      .catch(() => setProblem("Please allow the microphone to talk."))
    return () => {
      cancelled = true
      live.current?.stop()
      live.current = null
    }
  }, [start.token, start.model])

  useEffect(() => {
    const id = window.setInterval(() => setSeconds((s) => s + 1), 1000)
    return () => window.clearInterval(id)
  }, [])

  // The talk ends by itself at the limit, like the token.
  const over = seconds >= limit
  useEffect(() => {
    if (over) hangUp()
    // eslint-disable-next-line react-hooks/exhaustive-deps -- only when the time runs out
  }, [over])

  const clock = (n: number) => `${Math.floor(n / 60)}:${String(n % 60).padStart(2, "0")}`

  return (
    <div className="mx-auto flex max-w-xl flex-col items-center gap-6 py-6 text-center">
      <div>
        <h1 className="text-2xl font-extrabold">Gespräch</h1>
        <p className="mt-1 text-muted-foreground">Tako greets you first. Then tell her what you'd like to talk about.</p>
      </div>

      <div
        className={cn(
          "flex size-40 items-center justify-center rounded-full transition-all duration-300",
          state === "speaking" ? "scale-105 bg-primary text-primary-foreground" : "bg-surface-2 text-foreground",
          state === "listening" && "ring-4 ring-primary/40",
        )}
        aria-live="polite"
      >
        <Mic className="size-12" aria-hidden="true" />
      </div>
      <p className="text-lg font-semibold">{finish.isPending ? "Writing your report…" : LABEL[state]}</p>
      <p className="tabular-nums text-sm text-muted-foreground">
        {clock(Math.min(seconds, limit))} / {clock(limit)} · headphones work best
      </p>

      {problem && !finish.isPending && (
        <p className="text-sm text-[hsl(var(--danger))]">{problem}</p>
      )}
      {finish.isError && <p className="text-sm text-[hsl(var(--danger))]">{errorText(finish.error)}</p>}

      <div className="flex w-full flex-col gap-2.5">
        <Button size="lg" variant="destructive" onClick={hangUp} disabled={!connected}>
          <PhoneOff className="size-4" aria-hidden="true" />
          End and get my report
        </Button>
        {finish.isError && (
          <Button size="lg" variant="secondary" onClick={() => finish.mutate(finish.variables ?? [])}>
            Try the report again
          </Button>
        )}
        <Button size="lg" variant="ghost" onClick={() => setCaptions((c) => !c)}>
          {captions ? "Hide captions" : "Show captions"}
        </Button>
      </div>

      {captions && (
        <ul className="flex w-full flex-col gap-2 text-left">
          {turns.map((t, i) => (
            <li
              key={i}
              className={cn(
                "max-w-[85%] rounded-2xl px-4 py-2.5 text-[15px]",
                t.role === "user" ? "self-end bg-primary/10" : "self-start bg-surface-2",
              )}
            >
              {t.text}
            </li>
          ))}
        </ul>
      )}
    </div>
  )
}

function Report({ talk, onBack }: { talk: TalkDetail; onBack: () => void }) {
  const r = talk.report as Partial<TalkReport>
  const empty = !r.summary

  return (
    <div className="mx-auto flex max-w-2xl flex-col gap-5 py-4">
      <button
        type="button"
        onClick={onBack}
        className="inline-flex items-center gap-1.5 self-start text-sm font-semibold text-primary hover:underline"
      >
        <ArrowLeft className="size-4" aria-hidden="true" /> Back
      </button>
      <div>
        <h1 className="text-2xl font-extrabold">Your report</h1>
        <p className="mt-1 text-muted-foreground">{new Date(talk.started_at).toLocaleString()}</p>
      </div>

      {empty ? (
        <Card className="p-6">
          <p>You didn't say anything this time, so there's no report. Try again and answer out loud!</p>
        </Card>
      ) : (
        <>
          <Card className="p-6">
            <p className="text-[15px] leading-relaxed">{r.summary}</p>
          </Card>
          <Section title="Corrections">
            {r.corrections?.length ? (
              <ul className="flex flex-col gap-3">
                {r.corrections.map((c, i) => (
                  <li key={i} className="rounded-2xl bg-surface-2/70 p-4 text-[15px]">
                    <p className="text-muted-foreground line-through decoration-1">{c.you_said}</p>
                    <p className="mt-1 font-semibold">{c.better}</p>
                    <p className="mt-1 text-sm text-muted-foreground">{c.why}</p>
                  </li>
                ))}
              </ul>
            ) : (
              <p className="text-muted-foreground">No mistakes worth correcting. Super!</p>
            )}
          </Section>
          {!!r.phrases?.length && (
            <Section title="Useful phrases">
              <ul className="list-disc pl-5 text-[15px]">
                {r.phrases.map((p, i) => (
                  <li key={i}>{p}</li>
                ))}
              </ul>
            </Section>
          )}
          {!!r.new_words?.length && (
            <Section title="New words">
              <ul className="grid gap-2 sm:grid-cols-2">
                {r.new_words.map((w, i) => (
                  <li key={i} className="rounded-xl bg-surface-2/70 px-3 py-2 text-[15px]">
                    <span className="font-semibold">{w.german}</span>{" "}
                    <span className="text-muted-foreground">· {w.english}</span>
                  </li>
                ))}
              </ul>
            </Section>
          )}
          {!!r.practise?.length && (
            <Section title="Practise next">
              <ul className="list-disc pl-5 text-[15px]">
                {r.practise.map((p, i) => (
                  <li key={i}>{p}</li>
                ))}
              </ul>
            </Section>
          )}
        </>
      )}

      {!!talk.transcript.length && (
        <details className="rounded-2xl bg-surface-2/70 p-4 text-[15px]">
          <summary className="cursor-pointer font-semibold">Transcript</summary>
          <ul className="mt-3 flex flex-col gap-2">
            {talk.transcript.map((t, i) => (
              <li key={i}>
                <span className="font-semibold">{t.role === "user" ? "You" : "Tako"}:</span> {t.text}
              </li>
            ))}
          </ul>
        </details>
      )}
      <Button size="lg" onClick={onBack}>
        Talk again
      </Button>
    </div>
  )
}

function Section({ title, children }: { title: string; children: React.ReactNode }) {
  return (
    <section>
      <h2 className="mb-2 text-lg font-bold">{title}</h2>
      {children}
    </section>
  )
}
