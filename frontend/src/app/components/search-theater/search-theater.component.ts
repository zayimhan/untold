import { Component, OnDestroy, OnInit, signal } from '@angular/core';
import { ARCHIVE_MANIFEST, ManifestFragment } from './archive-manifest';

@Component({
  selector: 'app-search-theater',
  standalone: true,
  templateUrl: './search-theater.component.html',
  styleUrl: './search-theater.component.scss',
})
export class SearchTheaterComponent implements OnInit, OnDestroy {
  private readonly fragments: ManifestFragment[] = ARCHIVE_MANIFEST;
  visibleFragments = signal<ManifestFragment[]>([]);
  activeId = signal<string>('');
  private interval?: ReturnType<typeof setInterval>;

  ngOnInit(): void {
    this.interval = setInterval(() => this.tick(), 280);
  }

  ngOnDestroy(): void {
    if (this.interval) clearInterval(this.interval);
  }

  private tick(): void {
    const pool = this.fragments;
    const next = [...this.visibleFragments()];
    if (next.length < 5) {
      next.push(pool[Math.floor(Math.random() * pool.length)]);
    } else {
      next.shift();
      next.push(pool[Math.floor(Math.random() * pool.length)]);
    }
    this.visibleFragments.set(next);
    this.activeId.set(next[next.length - 1].id);
  }
}
