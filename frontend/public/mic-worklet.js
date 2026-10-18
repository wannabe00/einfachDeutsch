// Talk to AI: collects 128-sample microphone frames into ~128 ms chunks (16 kHz)
// and posts them to the page (src/lib/liveTalk.ts), which sends them to Gemini Live.
class Mic extends AudioWorkletProcessor {
  constructor() {
    super()
    this.buf = new Float32Array(2048)
    this.n = 0
  }

  process(inputs) {
    const ch = inputs[0][0]
    if (!ch) return true
    for (let i = 0; i < ch.length; i++) {
      this.buf[this.n++] = ch[i]
      if (this.n === this.buf.length) {
        this.port.postMessage(this.buf.slice())
        this.n = 0
      }
    }
    return true
  }
}
registerProcessor("mic", Mic)
