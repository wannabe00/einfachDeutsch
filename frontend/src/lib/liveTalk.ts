import type { TalkTurn } from "@/types"

/*
 * A live voice conversation with Gemini, straight from the browser.
 *
 * This is the one place the frontend talks to an AI provider directly (an
 * approved exception, see AGENTS.md): Django hands out a short-lived token that
 * can open exactly one Live session, with the model, voice, role and level
 * locked into it. The API key never reaches the browser.
 *
 * Microphone -> AudioWorklet (public/mic-worklet.js) -> 16 kHz 16-bit PCM -> `realtimeInput`.
 * Model audio (24 kHz PCM) is queued back to back; when the learner speaks over
 * it, Gemini sends `interrupted` and the queue is dropped. Both sides arrive as
 * transcriptions too, which build the transcript for the report.
 */

const ENDPOINT =
  "wss://generativelanguage.googleapis.com/ws/google.ai.generativelanguage.v1alpha.GenerativeService.BidiGenerateContentConstrained"
const MIC_RATE = 16000
const AI_RATE = 24000
// Sent once the session is ready so the AI opens with its first line.
const KICKOFF = "(Das Gespräch beginnt. Bitte fang an.)"

/** connecting -> starting (Tako greets) -> listening / speaking -> ended. */
export type LiveState = "connecting" | "starting" | "listening" | "speaking" | "ended"

export interface LiveTalk {
  /** Hang up; resolves with the whole transcript. */
  stop: () => TalkTurn[]
}

/** "(unklar)" for a line with letters outside the Latin alphabet: the learner
    speaks German or English (äöüß are Latin), so other scripts are the speech
    recogniser guessing at noise. */
export function readable(text: string): string {
  const letters = text.match(/\p{L}/gu) ?? []
  return letters.every((c) => /\p{Script=Latin}/u.test(c)) ? text : "(unklar)"
}

export const liveTalkSupported =
  typeof window !== "undefined" &&
  "WebSocket" in window &&
  "AudioWorkletNode" in window &&
  !!navigator.mediaDevices?.getUserMedia

function toBase64(bytes: Uint8Array): string {
  let s = ""
  for (let i = 0; i < bytes.length; i += 0x8000) s += String.fromCharCode(...bytes.subarray(i, i + 0x8000))
  return btoa(s)
}

function pcm16(samples: Float32Array): Uint8Array {
  const out = new Int16Array(samples.length)
  for (let i = 0; i < samples.length; i++) out[i] = Math.max(-1, Math.min(1, samples[i])) * 0x7fff
  return new Uint8Array(out.buffer)
}

function floats(base64: string): Float32Array<ArrayBuffer> {
  const bin = atob(base64)
  const view = new DataView(new ArrayBuffer(bin.length))
  for (let i = 0; i < bin.length; i++) view.setUint8(i, bin.charCodeAt(i))
  const out = new Float32Array(bin.length / 2)
  for (let i = 0; i < out.length; i++) out[i] = view.getInt16(i * 2, true) / 0x8000
  return out
}

/**
 * Open the session. Throws if the microphone is refused. `onState` follows who
 * is speaking; `onTurns` gets the transcript so far (for live captions);
 * `onError` reports a dropped connection.
 */
export async function startLiveTalk(
  token: string,
  model: string,
  handlers: { onState: (s: LiveState) => void; onTurns: (t: TalkTurn[]) => void; onError: (m: string) => void },
): Promise<LiveTalk> {
  // After stop() nothing reaches the page, e.g. the error Chrome fires when a
  // socket is closed while it's still opening (React dev mode mounts twice).
  const onState = (st: LiveState) => !ended && handlers.onState(st)
  const onTurns = (t: TalkTurn[]) => !ended && handlers.onTurns(t)
  const onError = (m: string) => !ended && handlers.onError(m)
  const mic = await navigator.mediaDevices.getUserMedia({
    audio: { channelCount: 1, echoCancellation: true, noiseSuppression: true, autoGainControl: true },
  })
  const micCtx = new AudioContext({ sampleRate: MIC_RATE })
  const outCtx = new AudioContext({ sampleRate: AI_RATE })
  const turns: TalkTurn[] = []
  const playing = new Set<AudioBufferSourceNode>()
  let playAt = 0
  let ended = false
  let micOn = false
  let worklet: AudioWorkletNode | null = null

  const ws = new WebSocket(`${ENDPOINT}?access_token=${encodeURIComponent(token)}`)

  function say(role: TalkTurn["role"], text: string) {
    const last = turns[turns.length - 1]
    if (last?.role === role) last.text += text
    else turns.push({ role, text })
    onTurns(turns.map((t) => ({ role: t.role, text: readable(t.text) })))
  }

  function play(base64: string) {
    const samples = floats(base64)
    const buffer = outCtx.createBuffer(1, samples.length, AI_RATE)
    buffer.copyToChannel(samples, 0)
    const src = outCtx.createBufferSource()
    src.buffer = buffer
    src.connect(outCtx.destination)
    playAt = Math.max(playAt, outCtx.currentTime)
    src.start(playAt)
    playAt += buffer.duration
    playing.add(src)
    onState("speaking")
    src.onended = () => {
      playing.delete(src)
      if (!playing.size && micOn) onState("listening")
    }
  }

  function silence() {
    playing.forEach((s) => s.stop())
    playing.clear()
    playAt = 0
  }

  async function startMic() {
    micOn = true
    // A static file, so the strict CSP (script-src 'self') allows it.
    await micCtx.audioWorklet.addModule("/mic-worklet.js")
    worklet = new AudioWorkletNode(micCtx, "mic")
    worklet.port.onmessage = (e: MessageEvent<Float32Array>) => {
      if (ws.readyState !== WebSocket.OPEN) return
      const data = toBase64(pcm16(e.data))
      ws.send(JSON.stringify({ realtimeInput: { audio: { data, mimeType: `audio/pcm;rate=${MIC_RATE}` } } }))
    }
    micCtx.createMediaStreamSource(mic).connect(worklet)
  }

  ws.onopen = () => ws.send(JSON.stringify({ setup: { model: `models/${model}` } }))
  ws.onmessage = async (event) => {
    const raw = typeof event.data === "string" ? event.data : await (event.data as Blob).text()
    const msg = JSON.parse(raw)
    if (msg.setupComplete) {
      // Tako always speaks first; the microphone opens after her greeting.
      ws.send(JSON.stringify({ realtimeInput: { text: KICKOFF } }))
      onState("starting")
      return
    }
    const content = msg.serverContent
    if (!content) return
    if (content.interrupted) silence()
    for (const part of content.modelTurn?.parts ?? []) {
      if (part.inlineData?.data) play(part.inlineData.data)
    }
    if (content.inputTranscription?.text) say("user", content.inputTranscription.text)
    if (content.outputTranscription?.text) say("ai", content.outputTranscription.text)
    if (content.turnComplete && !micOn) {
      await startMic()
      if (!playing.size) onState("listening")
    }
  }
  ws.onerror = () => onError("The connection to the voice service failed. Please try again.")
  ws.onclose = (e) => {
    if (!ended) onError(e.reason || "The conversation was disconnected.")
  }

  return {
    stop() {
      ended = true
      silence()
      ws.close()
      worklet?.disconnect()
      mic.getTracks().forEach((t) => t.stop())
      void micCtx.close()
      void outCtx.close()
      return turns.map((t) => ({ role: t.role, text: readable(t.text.trim()) })).filter((t) => t.text)
    },
  }
}
