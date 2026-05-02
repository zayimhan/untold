import { Component, EventEmitter, OnInit, Output, signal } from '@angular/core';

@Component({
  selector: 'app-options-panel',
  standalone: true,
  templateUrl: './options-panel.component.html',
  styleUrl: './options-panel.component.scss',
})
export class OptionsPanelComponent implements OnInit {
  @Output() seal = new EventEmitter<void>();
  @Output() leave = new EventEmitter<void>();
  transitioned = signal(false);

  ngOnInit(): void {
    setTimeout(() => this.transitioned.set(true), 1200);
  }
}
