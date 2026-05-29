import { Component, OnDestroy, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { Subscription, interval } from 'rxjs';
import { BoardGridComponent } from '../../shared/components/board-grid/board-grid';
import { ControlPanelComponent } from '../../shared/components/control-panel/control-panel';
import { MetricsPanelComponent } from '../../shared/components/metrics-panel/metrics-panel';
import { StepLegendComponent } from '../../shared/components/step-legend/step-legend';
import { ShikakuApiService } from '../../core/services/shikaku-api.service';
import { BoardMatrix } from '../../core/models/board.model';
import { SolverStep, StepType } from '../../core/models/solver-step.model';
import { SolverStats } from '../../core/models/solver-stats.model';
import { Rectangle } from '../../core/models/rectangle.model';

@Component({
  selector: 'app-demo',
  standalone: true,
  imports: [
    CommonModule,
    BoardGridComponent,
    ControlPanelComponent,
    MetricsPanelComponent,
    StepLegendComponent
  ],
  templateUrl: './demo.html',
  styleUrl: './demo.css'
})
export class Demo implements OnInit, OnDestroy {
  boardsMap: Record<string, BoardMatrix> = {};
  boardNames: string[] = [];
  selectedBoardId = '';
  currentBoard: BoardMatrix = [];

  steps: SolverStep[] = [];
  currentStepIndex = -1;
  isPlaying = false;
  isLoading = false;
  playbackSpeedMs = 500;
  private playbackSub?: Subscription;

  activeStepType?: StepType | string;
  currentStepMessage = 'Listo para iniciar.';
  stats?: SolverStats;
  
  solution: Rectangle[] = [];
  testingRectangle: Rectangle | null = null;
  errorRectangle: Rectangle | null = null;

  constructor(private api: ShikakuApiService) {}

  ngOnInit() {
    this.isLoading = true;
    this.api.getBoards().subscribe({
      next: (res) => {
        this.boardsMap = res.boards;
        this.boardNames = Object.keys(this.boardsMap);
        if (this.boardNames.length > 0) {
          this.onBoardSelected(this.boardNames[0]);
        }
        this.isLoading = false;
      },
      error: () => {
        this.isLoading = false;
        this.currentStepMessage = 'Error al cargar tableros.';
      }
    });
  }

  ngOnDestroy() {
    this.pause();
  }

  onBoardSelected(boardId: string) {
    this.selectedBoardId = boardId;
    this.currentBoard = this.boardsMap[boardId];
    this.resetState();
    this.currentStepMessage = `Tablero ${boardId} cargado.`;
  }

  onSolveInstant() {
    this.resetState();
    this.isLoading = true;
    this.currentStepMessage = 'Resolviendo...';
    this.api.solve(this.currentBoard).subscribe({
      next: (res) => {
        this.stats = res.stats;
        this.solution = res.solution;
        this.currentStepMessage = res.solved ? 'Solución encontrada instantáneamente.' : 'No hay solución.';
        this.isLoading = false;
      },
      error: () => {
        this.isLoading = false;
        this.currentStepMessage = 'Error en el servidor.';
      }
    });
  }

  onLoadSteps(autoPlay = false) {
    this.resetState();
    this.isLoading = true;
    this.currentStepMessage = 'Calculando y descargando pasos...';
    this.api.getSteps(this.currentBoard).subscribe({
      next: (res) => {
        this.steps = res.steps;
        this.currentStepMessage = `¡${this.steps.length} pasos cargados! Presiona Play.`;
        this.isLoading = false;
        if (autoPlay) {
          this.startPlayback();
        }
      },
      error: () => {
        this.isLoading = false;
        this.currentStepMessage = 'Error al generar los pasos.';
      }
    });
  }

  play() {
    if (this.isPlaying || (this.steps.length > 0 && this.currentStepIndex >= this.steps.length - 1)) {
      return;
    }
    
    if (this.steps.length === 0) {
      this.onLoadSteps(true);
      return;
    }

    this.startPlayback();
  }

  private startPlayback() {
    this.isPlaying = true;
    this.currentStepMessage = 'Reproduciendo algoritmo...';
    
    this.playbackSub = interval(this.playbackSpeedMs).subscribe(() => {
      this.nextStep();
    });
  }

  pause() {
    this.isPlaying = false;
    this.playbackSub?.unsubscribe();
    this.playbackSub = undefined;
    if (this.steps.length > 0 && this.currentStepIndex < this.steps.length - 1) {
      this.currentStepMessage = 'Pausado.';
    }
  }

  nextStep() {
    if (this.currentStepIndex < this.steps.length - 1) {
      this.currentStepIndex++;
      this.applyStep(this.steps[this.currentStepIndex]);
    } else {
      this.pause();
      this.currentStepMessage = 'Demostración finalizada.';
    }
  }

  resetState() {
    this.pause();
    this.steps = [];
    this.currentStepIndex = -1;
    this.stats = undefined;
    this.activeStepType = undefined;
    this.solution = [];
    this.testingRectangle = null;
    this.errorRectangle = null;
    this.currentStepMessage = 'Listo.';
  }

  onSpeedChanged(speed: number) {
    this.playbackSpeedMs = speed;
    if (this.isPlaying) {
      this.pause();
      this.play();
    }
  }

  private applyStep(step: SolverStep) {
    this.activeStepType = step.type;
    this.stats = step.stats;
    
    this.testingRectangle = null;
    this.errorRectangle = null;

    if (step.solution) {
      this.solution = step.solution;
    }

    switch (step.type) {
      case 'try':
        this.testingRectangle = step.rectangle || null;
        this.currentStepMessage = 'Probando candidato...';
        break;
      case 'place':
        this.currentStepMessage = 'Rectángulo válido, colocado.';
        break;
      case 'reject_overlap':
        this.errorRectangle = step.rectangle || null;
        this.currentStepMessage = 'Rechazo: Solapamiento con otra figura.';
        break;
      case 'reject_forward_check':
        this.errorRectangle = step.rectangle || null;
        this.currentStepMessage = 'Poda: Forward checking detectó callejón sin salida.';
        break;
      case 'reject_uncoverable_cell':
        this.errorRectangle = step.rectangle || null;
        this.currentStepMessage = 'Poda: Una celda quedó imposible de cubrir.';
        break;
      case 'backtrack':
      case 'remove' as any:
        this.currentStepMessage = 'Backtrack: Removiendo y retrocediendo...';
        break;
    }

    if (step.type as any === 'solution') {
      this.currentStepMessage = '¡Solución final encontrada!';
    } else if (step.type as any === 'no_solution' || step.type as any === 'dead_end') {
      this.currentStepMessage = 'Sin opciones (Dead End).';
    }
  }
}
