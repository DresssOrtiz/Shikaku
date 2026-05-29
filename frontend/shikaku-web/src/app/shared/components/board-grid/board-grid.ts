import { Component, Input, OnChanges, SimpleChanges } from '@angular/core';
import { CommonModule } from '@angular/common';
import { BoardMatrix } from '../../../core/models/board.model';
import { Rectangle } from '../../../core/models/rectangle.model';

@Component({
  selector: 'app-board-grid',
  standalone: true,
  imports: [CommonModule],
  templateUrl: './board-grid.html',
  styleUrl: './board-grid.css'
})
export class BoardGridComponent implements OnChanges {
  @Input() board: BoardMatrix = [];
  @Input() placements: Rectangle[] = [];
  @Input() testing: Rectangle | null = null;
  @Input() errorRectangle: Rectangle | null = null;

  gridRows = 0;
  gridCols = 0;

  ngOnChanges(changes: SimpleChanges): void {
    if (changes['board'] && this.board.length > 0) {
      this.gridRows = this.board.length;
      this.gridCols = this.board[0].length;
    }
  }

  getCellClass(r: number, c: number): string {
    if (this.errorRectangle && this.isInside(r, c, this.errorRectangle)) {
      return 'cell-error';
    }
    if (this.testing && this.isInside(r, c, this.testing)) {
      return 'cell-testing';
    }
    for (const rect of this.placements) {
      if (this.isInside(r, c, rect)) {
        return 'cell-placed';
      }
    }
    return 'cell-empty';
  }

  private isInside(row: number, col: number, rectangle: Rectangle): boolean {
    return (
      row >= rectangle.top &&
      row <= rectangle.bottom &&
      col >= rectangle.left &&
      col <= rectangle.right
    );
  }
}
