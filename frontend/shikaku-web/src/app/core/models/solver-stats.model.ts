export interface SolverStats {
  recursive_calls: number;
  candidates_tested: number;
  placements: number;
  backtracks: number;
  overlap_rejections: number;
  forward_prunes: number;
  cell_prunes: number;
  max_depth: number;
  solutions_found: number;
  elapsed_ms: number;
}
