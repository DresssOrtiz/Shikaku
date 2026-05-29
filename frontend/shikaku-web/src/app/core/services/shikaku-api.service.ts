import { HttpClient } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { Observable } from 'rxjs';
import { BoardMatrix } from '../models/board.model';
import { SolverStats } from '../models/solver-stats.model';
import { SolverStep } from '../models/solver-step.model';
import { Rectangle } from '../models/rectangle.model';

export interface SolveResponse {
  solved: boolean;
  solution: Rectangle[];
  stats: SolverStats;
}

export interface StepsResponse {
  steps: SolverStep[];
}

export interface BoardsResponse {
  boards: Record<string, BoardMatrix>;
}

@Injectable({
  providedIn: 'root',
})
export class ShikakuApiService {
  private readonly apiUrl = '/api';

  constructor(private readonly http: HttpClient) {}

  solve(board: BoardMatrix): Observable<SolveResponse> {
    return this.http.post<SolveResponse>(`${this.apiUrl}/solve`, { board });
  }

  getBoards(): Observable<BoardsResponse> {
    return this.http.get<BoardsResponse>(`${this.apiUrl}/boards`);
  }

  getSteps(board: BoardMatrix): Observable<StepsResponse> {
    return this.http.post<StepsResponse>(`${this.apiUrl}/steps`, { board });
  }

}
