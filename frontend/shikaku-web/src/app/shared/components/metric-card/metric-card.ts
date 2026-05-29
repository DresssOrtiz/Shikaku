import { Component, Input } from '@angular/core';

@Component({
  selector: 'app-metric-card',
  standalone: true,
  templateUrl: './metric-card.html',
  styleUrl: './metric-card.css'
})
export class MetricCardComponent {
  @Input() title = '';
  @Input() value: number | string = 0;
  @Input() highlight = false;
}
