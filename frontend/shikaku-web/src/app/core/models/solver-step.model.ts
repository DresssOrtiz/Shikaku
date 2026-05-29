import { Rectangle } from './rectangle.model';
import { SolverStats } from './solver-stats.model';

export type StepType = 
  | 'try' 
  | 'place' 
  | 'reject_overlap' 
  | 'reject_forward_check' 
  | 'reject_uncoverable_cell' 
  | 'backtrack';

export interface SolverStep {
  type: StepType;
  clue?: [number, number, number]; // [row, col, value]
  rectangle?: Rectangle;
  stats: SolverStats;
  solution?: Rectangle[];
}
