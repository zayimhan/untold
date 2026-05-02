import { Component, Input } from '@angular/core';

export type DoorPhase = 'hidden' | 'closed' | 'knocking' | 'opening' | 'open';

@Component({
  selector: 'app-door-scene',
  standalone: true,
  templateUrl: './door-scene.component.html',
  styleUrl: './door-scene.component.scss',
})
export class DoorSceneComponent {
  @Input() phase: DoorPhase = 'hidden';
}
