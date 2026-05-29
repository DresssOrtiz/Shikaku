import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { ShikakuApiService } from '../../core/services/shikaku-api.service';
import { SolverStats } from '../../core/models/solver-stats.model';
import { forkJoin, map, switchMap } from 'rxjs';

interface BenchmarkResult {
  boardName: string;
  stats: SolverStats;
}

@Component({
  selector: 'app-benchmark',
  standalone: true,
  imports: [CommonModule],
  templateUrl: './benchmark.html',
  styleUrl: './benchmark.css'
})
export class Benchmark implements OnInit {
  results: BenchmarkResult[] = [];
  isLoading = false;
  error = '';

  constructor(private api: ShikakuApiService) {}

  ngOnInit() {
    this.runBenchmark();
  }

  runBenchmark() {
    this.isLoading = true;
    this.error = '';
    this.results = [];

    this.api.getBoards().pipe(
      switchMap(res => {
        const boardNames = Object.keys(res.boards);
        const observables = boardNames.map(name =>
          this.api.solve(res.boards[name]).pipe(
            map(solveRes => ({ boardName: name, stats: solveRes.stats }))
          )
        );
        return forkJoin(observables);
      })
    ).subscribe({
      next: (results) => {
        this.results = results;
        this.isLoading = false;
      },
      error: () => {
        this.error = 'No se pudo conectar con el servidor para la prueba masiva.';
        this.isLoading = false;
      }
    });
  }
}
