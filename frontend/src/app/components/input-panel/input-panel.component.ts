import { Component, EventEmitter, Output } from '@angular/core';
import { FormsModule } from '@angular/forms';

@Component({
  selector: 'app-input-panel',
  standalone: true,
  imports: [FormsModule],
  templateUrl: './input-panel.component.html',
  styleUrl: './input-panel.component.scss',
})
export class InputPanelComponent {
  @Output() submitted = new EventEmitter<string>();

  userText = '';

  submit(): void {
    const text = this.userText.trim();
    if (text) {
      this.submitted.emit(text);
    }
  }

  onKeydown(event: KeyboardEvent): void {
    if ((event.metaKey || event.ctrlKey) && event.key === 'Enter') {
      this.submit();
    }
  }
}
