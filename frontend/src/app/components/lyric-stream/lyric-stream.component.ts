import { Component, Input } from '@angular/core';

@Component({
  selector: 'app-lyric-stream',
  standalone: true,
  templateUrl: './lyric-stream.component.html',
  styleUrl: './lyric-stream.component.scss',
})
export class LyricStreamComponent {
  @Input() lines: string[] = [];
}
