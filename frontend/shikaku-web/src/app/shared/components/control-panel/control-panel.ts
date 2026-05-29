import { Component, EventEmitter, Input, Output } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';

@Component({
  selector: 'app-control-panel',
  standalone: true,
  imports: [CommonModule, FormsModule],
  templateUrl: './control-panel.html',
  styleUrl: './control-panel.css'
})
export class ControlPanelComponent {
  @Input() boards: string[] = [];
  @Input() selectedBoardId = '';
  @Input() isPlaying = false;
  @Input() isLoading = false;
  @Input() playbackSpeedMs = 500;

  @Output() boardSelected = new EventEmitter<string>();
  @Output() solveClicked = new EventEmitter<void>();
  @Output() stepsClicked = new EventEmitter<void>();
  @Output() playClicked = new EventEmitter<void>();
  @Output() pauseClicked = new EventEmitter<void>();
  @Output() nextClicked = new EventEmitter<void>();
  @Output() resetClicked = new EventEmitter<void>();
  @Output() speedChanged = new EventEmitter<number>();

  onBoardChange(event: Event) {
    const target = event.target as HTMLSelectElement;
    this.boardSelected.emit(target.value);
  }

  onSpeedChange(event: Event) {
    const target = event.target as HTMLSelectElement;
    this.speedChanged.emit(Number(target.value));
  }
}
