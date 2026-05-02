import { Component, EventEmitter, Input, OnInit, Output, signal } from '@angular/core';

type EnvPhase = 'folding' | 'sliding' | 'sealing' | 'sealed';

@Component({
  selector: 'app-envelope-scene',
  standalone: true,
  templateUrl: './envelope-scene.component.html',
  styleUrl: './envelope-scene.component.scss',
})
export class EnvelopeSceneComponent implements OnInit {
  @Input() lyricLines: string[] = [];
  @Output() complete = new EventEmitter<void>();

  phase = signal<EnvPhase>('folding');

  get paperLines(): number[] {
    const count = this.lyricLines.filter((l) => l.trim()).length;
    return Array.from({ length: Math.min(count, 10) }, (_, i) => i);
  }

  ngOnInit(): void {
    setTimeout(() => this.phase.set('sliding'), 2500);
    setTimeout(() => this.phase.set('sealing'), 5000);
    setTimeout(() => {
      this.phase.set('sealed');
      this.complete.emit();
    }, 7500);
  }
}
