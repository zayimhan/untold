import { Component, Input } from '@angular/core';
import { ArchiveMatch } from '../../models/response.model';

@Component({
  selector: 'app-archive-echo',
  standalone: true,
  imports: [],
  templateUrl: './archive-echo.component.html',
  styleUrl: './archive-echo.component.scss',
})
export class ArchiveEchoComponent {
  @Input() match: ArchiveMatch | null = null;

  get textLines(): string[] {
    if (!this.match?.text) return [];
    return this.splitToLines(this.match.text, 44);
  }

  get sigDelay(): string {
    return (this.textLines.length * 0.5 + 1.6) + 's';
  }

  private splitToLines(text: string, maxChars: number): string[] {
    const words = text.split(' ');
    const lines: string[] = [];
    let current = '';
    for (const word of words) {
      const candidate = current ? current + ' ' + word : word;
      if (candidate.length <= maxChars) {
        current = candidate;
      } else {
        if (current) lines.push(current);
        current = word;
      }
    }
    if (current) lines.push(current);
    return lines;
  }
}
