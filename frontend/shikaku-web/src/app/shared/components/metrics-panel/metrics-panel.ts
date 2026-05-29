import { Component, Input } from '@angular/core';
import { CommonModule } from '@angular/common';
import { MetricCardComponent } from '../metric-card/metric-card';
import { SolverStats } from '../../../core/models/solver-stats.model';

@Component({
  selector: 'app-metrics-panel',
  standalone: true,
  imports: [CommonModule, MetricCardComponent],
  templateUrl: './metrics-panel.html',
  styleUrl: './metrics-panel.css'
})
export class MetricsPanelComponent {
  @Input() stats?: SolverStats;

  get metrics() {
    return [
      { label: 'Tiempo (ms)', value: this.stats?.elapsed_ms?.toFixed(2) ?? 0, highlight: true },
      { label: 'Recursiones', value: this.stats?.recursive_calls ?? 0, highlight: false },
      { label: 'Candidatos', value: this.stats?.candidates_tested ?? 0, highlight: false },
      { label: 'Colocaciones', value: this.stats?.placements ?? 0, highlight: false },
      { label: 'Backtracks', value: this.stats?.backtracks ?? 0, highlight: false },
      { label: 'Rechazos (Overlap)', value: this.stats?.overlap_rejections ?? 0, highlight: false },
      { label: 'Podas (Forward)', value: this.stats?.forward_prunes ?? 0, highlight: false },
      { label: 'Podas (Celdas)', value: this.stats?.cell_prunes ?? 0, highlight: false },
      { label: 'Profundidad Max', value: this.stats?.max_depth ?? 0, highlight: false },
      { label: 'Soluciones', value: this.stats?.solutions_found ?? 0, highlight: false },
    ];
  }
}
