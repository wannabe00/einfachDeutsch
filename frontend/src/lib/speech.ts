/*
 * Reading German aloud with the browser's own speech synthesis (no server, no
 * cost). Used by "which word do you hear?" and dictation. The text arrives
 * base64-encoded so it isn't readable at a glance in the page data.
 */

export function decodeSpeech(encoded: string): string {
  const bytes = Uint8Array.from(atob(encoded), (c) => c.charCodeAt(0))
  return new TextDecoder().decode(bytes)
}

export function canSpeak(): boolean {
  return typeof window !== "undefined" && "speechSynthesis" in window
}

/** Read `text` in German. `slow` reads it at about two-thirds speed. */
export function speak(text: string, slow = false) {
  if (!canSpeak()) return
  const synth = window.speechSynthesis
  synth.cancel()
  const utterance = new SpeechSynthesisUtterance(text)
  utterance.lang = "de-DE"
  utterance.rate = slow ? 0.65 : 0.95
  const voice = synth.getVoices().find((v) => v.lang.toLowerCase().startsWith("de"))
  if (voice) utterance.voice = voice
  synth.speak(utterance)
}
