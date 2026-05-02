import { Injectable } from '@angular/core';

@Injectable({ providedIn: 'root' })
export class AudioService {
  private ctx: AudioContext | null = null;
  private knockTimer: ReturnType<typeof setInterval> | null = null;

  preload(): void {}

  /* ── Knock (synthesized) ─────────────────────────────────
     Three low-frequency thuds, loops every 3.2s until
     stopKnock() is called.                                  */
  playKnock(): void {
    this.stopKnock();
    const fire = () => {
      const ctx = this.getCtx();
      const knockAt = (t: number) => {
        const duration = 0.18;
        const buf = ctx.createBuffer(1, Math.floor(ctx.sampleRate * duration), ctx.sampleRate);
        const data = buf.getChannelData(0);
        for (let i = 0; i < data.length; i++) {
          const decay = Math.pow(1 - i / data.length, 4);
          data[i] = (Math.random() * 2 - 1) * decay;
        }

        const src = ctx.createBufferSource();
        src.buffer = buf;

        const filter = ctx.createBiquadFilter();
        filter.type = 'lowpass';
        filter.frequency.setValueAtTime(280, t);

        const gain = ctx.createGain();
        gain.gain.setValueAtTime(1.2, t);
        gain.gain.exponentialRampToValueAtTime(0.001, t + duration);

        src.connect(filter);
        filter.connect(gain);
        gain.connect(ctx.destination);
        src.start(t);
      };

      const now = ctx.currentTime;
      knockAt(now);
      knockAt(now + 0.9);
      knockAt(now + 1.8);
    };

    fire();
    this.knockTimer = setInterval(fire, 3200);
  }

  stopKnock(): void {
    if (this.knockTimer) {
      clearInterval(this.knockTimer);
      this.knockTimer = null;
    }
  }

  private getCtx(): AudioContext {
    if (!this.ctx) this.ctx = new AudioContext();
    if (this.ctx.state === 'suspended') this.ctx.resume();
    return this.ctx;
  }
}
