import { Injectable } from '@angular/core';

const FONT_SIZE   = 22;
const LINE_H      = 36;
const PADDING     = 60;
const FOOTER_FONT = 15;
const FOOTER_GAP  = 48;

@Injectable({ providedIn: 'root' })
export class EnvelopeExportService {
  async prepareBlob(lyricLines: string[]): Promise<Blob | null> {
    const canvas = document.createElement('canvas');
    canvas.width  = 720;
    canvas.height = 1280;
    const ctx = canvas.getContext('2d');
    if (!ctx) return null;

    const canRecord =
      typeof MediaRecorder !== 'undefined' &&
      (MediaRecorder.isTypeSupported('video/webm;codecs=vp9') ||
        MediaRecorder.isTypeSupported('video/webm'));

    if (!canRecord) {
      return this.renderPngBlob(ctx, canvas, lyricLines);
    }

    const mimeType = MediaRecorder.isTypeSupported('video/webm;codecs=vp9')
      ? 'video/webm;codecs=vp9'
      : 'video/webm';

    const stream   = canvas.captureStream(30);
    const recorder = new MediaRecorder(stream, { mimeType });
    const chunks: Blob[] = [];
    recorder.ondataavailable = (e) => { if (e.data.size > 0) chunks.push(e.data); };

    recorder.start(100);
    await this.animateFrames(ctx, canvas, lyricLines);
    recorder.stop();

    await new Promise<void>((resolve) => { recorder.onstop = () => resolve(); });
    return new Blob(chunks, { type: 'video/webm' });
  }

  download(blob: Blob, filename: string): void {
    const url = URL.createObjectURL(blob);
    const a   = document.createElement('a');
    a.href     = url;
    a.download = filename;
    a.click();
    setTimeout(() => URL.revokeObjectURL(url), 5000);
  }

  /* ── Wrap a single line to fit maxWidth ────────────────── */
  private wrapLine(
    ctx: CanvasRenderingContext2D,
    text: string,
    maxWidth: number,
  ): string[] {
    const words   = text.split(' ');
    const wrapped: string[] = [];
    let current = '';

    for (const word of words) {
      const candidate = current ? `${current} ${word}` : word;
      if (ctx.measureText(candidate).width > maxWidth && current) {
        wrapped.push(current);
        current = word;
      } else {
        current = candidate;
      }
    }
    if (current) wrapped.push(current);
    return wrapped.length ? wrapped : [text];
  }

  /* ── Pre-compute rendered rows (source idx kept for timing) */
  private buildRows(
    ctx: CanvasRenderingContext2D,
    lines: string[],
    maxWidth: number,
  ): Array<{ text: string; srcIdx: number }> {
    const rows: Array<{ text: string; srcIdx: number }> = [];
    lines.forEach((line, i) => {
      if (!line.trim()) {
        rows.push({ text: '', srcIdx: i });
      } else {
        this.wrapLine(ctx, line, maxWidth).forEach((w) =>
          rows.push({ text: w, srcIdx: i }),
        );
      }
    });
    return rows;
  }

  private async animateFrames(
    ctx: CanvasRenderingContext2D,
    canvas: HTMLCanvasElement,
    lines: string[],
  ): Promise<void> {
    const maxW = canvas.width - PADDING * 2;
    ctx.font   = `italic ${FONT_SIZE}px Georgia, serif`;
    const rows = this.buildRows(ctx, lines, maxW);

    const totalH    = rows.length * LINE_H;
    const footerY   = canvas.height - FOOTER_GAP;
    // Centre vertically; push up if it would overlap footer
    const startY    = Math.min(
      Math.max(PADDING + FONT_SIZE, (canvas.height - totalH) / 2 + FONT_SIZE),
      footerY - totalH - 12,
    );

    const revealInterval = 200;
    const totalDuration  = lines.length * revealInterval + 800;
    const start          = performance.now();

    await new Promise<void>((resolve) => {
      const draw = (now: number) => {
        const elapsed = now - start;

        ctx.fillStyle = '#0a0a0a';
        ctx.fillRect(0, 0, canvas.width, canvas.height);
        ctx.textAlign = 'center';
        ctx.font      = `italic ${FONT_SIZE}px Georgia, serif`;

        rows.forEach((row, ri) => {
          if (!row.text) return;
          const revealAt    = row.srcIdx * revealInterval;
          if (elapsed < revealAt) return;
          const alpha       = Math.min((elapsed - revealAt) / 200, 1);
          ctx.globalAlpha   = alpha;
          ctx.fillStyle     = '#e8e0d0';
          ctx.fillText(row.text, canvas.width / 2, startY + ri * LINE_H);
        });

        ctx.globalAlpha = 0.35;
        ctx.fillStyle   = '#c9a870';
        ctx.font        = `${FOOTER_FONT}px Georgia, serif`;
        ctx.fillText('Untold — 1973', canvas.width / 2, footerY);
        ctx.globalAlpha = 1;

        if (elapsed < totalDuration) {
          requestAnimationFrame(draw);
        } else {
          resolve();
        }
      };
      requestAnimationFrame(draw);
    });
  }

  private renderPngBlob(
    ctx: CanvasRenderingContext2D,
    canvas: HTMLCanvasElement,
    lines: string[],
  ): Promise<Blob | null> {
    const maxW = canvas.width - PADDING * 2;
    ctx.font   = `italic ${FONT_SIZE}px Georgia, serif`;
    ctx.textAlign = 'center';
    const rows = this.buildRows(ctx, lines, maxW);

    const totalH  = rows.length * LINE_H;
    const footerY = canvas.height - FOOTER_GAP;
    const startY  = Math.min(
      Math.max(PADDING + FONT_SIZE, (canvas.height - totalH) / 2 + FONT_SIZE),
      footerY - totalH - 12,
    );

    ctx.fillStyle = '#0a0a0a';
    ctx.fillRect(0, 0, canvas.width, canvas.height);

    ctx.fillStyle = '#e8e0d0';
    rows.forEach((row, ri) => {
      if (row.text) ctx.fillText(row.text, canvas.width / 2, startY + ri * LINE_H);
    });

    ctx.globalAlpha = 0.35;
    ctx.fillStyle   = '#c9a870';
    ctx.font        = `${FOOTER_FONT}px Georgia, serif`;
    ctx.fillText('Untold — 1973', canvas.width / 2, footerY);
    ctx.globalAlpha = 1;

    return new Promise((resolve) => canvas.toBlob(resolve));
  }
}
