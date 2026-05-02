import { Component, NgZone, OnInit, computed, signal } from '@angular/core';
import { TransformService } from './services/transform.service';
import { AudioService } from './services/audio.service';
import { EnvelopeExportService } from './services/envelope-export.service';
import { ArchiveMatch } from './models/response.model';
import { InputPanelComponent } from './components/input-panel/input-panel.component';
import { LyricStreamComponent } from './components/lyric-stream/lyric-stream.component';
import { ArchiveEchoComponent } from './components/archive-echo/archive-echo.component';
import { DoorSceneComponent, DoorPhase } from './components/door-scene/door-scene.component';
import { EnvelopeSceneComponent } from './components/envelope-scene/envelope-scene.component';
import { SearchTheaterComponent } from './components/search-theater/search-theater.component';
import { OptionsPanelComponent } from './components/options-panel/options-panel.component';
import { EnvelopeFlightComponent } from './components/envelope-flight/envelope-flight.component';

type AppState =
  | 'waiting'
  | 'fetching'
  | 'lyric_revealing'
  | 'archive_showing'
  | 'door_appearing'
  | 'door_knocking'
  | 'options'
  | 'sealing'
  | 'sealed'
  | 'sending'
  | 'sent'
  | 'leaving'
  | 'gone';

@Component({
  selector: 'app-root',
  standalone: true,
  imports: [
    InputPanelComponent,
    LyricStreamComponent,
    ArchiveEchoComponent,
    DoorSceneComponent,
    EnvelopeSceneComponent,
    SearchTheaterComponent,
    OptionsPanelComponent,
    EnvelopeFlightComponent,
  ],
  templateUrl: './app.html',
  styleUrl: './app.scss',
})
export class App implements OnInit {
  state      = signal<AppState>('waiting');
  lyricLines = signal<string[]>([]);
  topMatch   = signal<ArchiveMatch | null>(null);
  error      = signal('');

  private lyricBuffer = '';
  private timers: ReturnType<typeof setTimeout>[] = [];
  private pendingBlob: Promise<Blob | null> = Promise.resolve(null);

  constructor(
    private svc: TransformService,
    private audio: AudioService,
    private exportSvc: EnvelopeExportService,
    private zone: NgZone,
  ) {}

  ngOnInit(): void {
    this.audio.preload();
  }

  /* ── Computed helpers ──────────────────────────────────── */

  readonly doorPhase = computed<DoorPhase>(() => {
    const s = this.state();
    if (s === 'door_appearing') return 'closed';
    if (s === 'door_knocking' || s === 'options') return 'knocking';
    if (s === 'sending') return 'opening';
    if (s === 'sent') return 'open';
    return 'hidden';
  });

  readonly isDoorVisible = computed(() => {
    const s = this.state();
    return (
      s === 'door_appearing' ||
      s === 'door_knocking'  ||
      s === 'options'
    );
  });

  readonly isSceneVisible = computed(() => {
    const s = this.state();
    return (
      s === 'lyric_revealing' ||
      s === 'archive_showing' ||
      s === 'door_appearing'  ||
      s === 'door_knocking'   ||
      s === 'options'
    );
  });

  readonly isArchiveVisible = computed(() => {
    const s = this.state();
    return (
      s === 'archive_showing' ||
      s === 'door_appearing'  ||
      s === 'door_knocking'   ||
      s === 'options'
    );
  });

  /* ── Submit ────────────────────────────────────────────── */

  onSubmit(userText: string): void {
    this.clearTimers();
    this.lyricBuffer = '';
    this.error.set('');
    this.state.set('fetching');

    this.svc.transformStream(
      userText,
      (token) =>           this.zone.run(() => { this.lyricBuffer += token; }),
      (matches, _track) => this.zone.run(() => { this.topMatch.set(matches[0] ?? null); }),
      () =>                this.zone.run(() => this.startReveal()),
      () =>                this.zone.run(() => {
        this.error.set('Something went wrong. The words did not travel.');
        this.state.set('waiting');
      }),
      () =>                this.zone.run(() => {
        this.error.set('say it nicer.');
        this.state.set('waiting');
      }),
    );
  }

  private startReveal(): void {
    this.lyricLines.set(this.lyricBuffer.split('\n'));
    this.state.set('lyric_revealing');

    const nonEmpty = this.lyricLines().filter((l) => l.trim()).length;
    const revealMs = nonEmpty * 1500 + 1200;

    this.addTimer(revealMs, () => this.state.set('archive_showing'));
    this.addTimer(revealMs + 3000, () => this.state.set('door_appearing'));
    this.addTimer(revealMs + 3000 + 1800, () => {
      this.state.set('door_knocking');
      this.audio.playKnock();
    });
    this.addTimer(revealMs + 3000 + 1800 + 2800, () => this.state.set('options'));
  }

  /* ── Options ───────────────────────────────────────────── */

  sealIt(): void {
    this.audio.stopKnock();
    this.state.set('sealing');
  }

  onSealingComplete(): void {
    this.state.set('sealed');
  }

  sendIt(): void {
    this.state.set('sending');

    // Start encoding immediately — canvas render completes in ~2-3s
    this.pendingBlob = this.exportSvc
      .prepareBlob(this.lyricLines())
      .catch(() => null);

    // t=4000ms: envelope reaches top-right corner — trigger download
    this.addTimer(4000, async () => {
      const blob = await this.pendingBlob;
      if (blob) this.exportSvc.download(blob, `untold_${Date.now()}.webm`);
    });

    // t=4200ms: animation complete — transition to 'sent'
    this.addTimer(4200, () => this.state.set('sent'));
  }

  leaveIt(): void {
    this.audio.stopKnock();
    this.state.set('leaving');
    this.addTimer(3500, () => this.state.set('gone'));
  }

  /* ── Reset ─────────────────────────────────────────────── */

  reset(): void {
    this.clearTimers();
    this.audio.stopKnock();
    this.state.set('waiting');
    this.lyricLines.set([]);
    this.topMatch.set(null);
    this.error.set('');
    this.pendingBlob = Promise.resolve(null);
  }

  /* ── Timer helpers ─────────────────────────────────────── */

  private addTimer(ms: number, fn: () => void): void {
    this.timers.push(setTimeout(fn, ms));
  }

  private clearTimers(): void {
    this.timers.forEach((t) => clearTimeout(t));
    this.timers = [];
  }
}
