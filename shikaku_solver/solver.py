"""Backtracking solver for the Shikaku puzzle.

The code is directly solving the puzzle using backtracking, enhanced with
heuristics: MRV, LCV, forward checking, and unreachable cell pruning.
"""
from time import perf_counter

class ShikakuSolver:
    def __init__(self, board):
        if not board or not board[0]:
            raise ValueError("The board cannot be empty.")

        self.board = board
        self.rows = len(board)
        self.cols = len(board[0])

        for row in board:
            if len(row) != self.cols:
                raise ValueError("All rows must have the same length.")

        self.clues = self._find_clues()
        self.candidates_by_clue = self._generate_all_candidates()
        self._empty_stats()

    def _empty_stats(self):
        self.stats = {
            "recursive_calls": 0,
            "candidates_tested": 0,
            "placements": 0,
            "backtracks": 0,
            "overlap_rejections": 0,
            "forward_prunes": 0,
            "cell_prunes": 0,
            "max_depth": 0,
            "solutions_found": 0,
            "elapsed_ms": 0.0,
        }

    def _reset_stats(self):
        self._empty_stats()

    def get_stats(self):
        return self.stats

    def _elapsed_ms(self, start):
        return (perf_counter() - start) * 1000.0

    def _find_clues(self):
        clues = []
        for row in range(self.rows):
            for col in range(self.cols):
                value = self.board[row][col]
                if value > 0:
                    clues.append((row, col, value))
        return clues

    def _generate_all_candidates(self):
        candidates = {}
        for clue in self.clues:
            candidates[clue] = self._generate_candidates_for_clue(clue)
        return candidates

    def _generate_candidates_for_clue(self, clue):
        clue_row, clue_col, value = clue
        candidates = []

        for height in range(1, value + 1):
            if value % height != 0:
                continue
            width = value // height

            for top in range(clue_row - height + 1, clue_row + 1):
                bottom = top + height - 1
                if top < 0 or bottom >= self.rows:
                    continue

                for left in range(clue_col - width + 1, clue_col + 1):
                    right = left + width - 1
                    if left < 0 or right >= self.cols:
                        continue

                    rectangle = {
                        "clue": clue,
                        "top": top,
                        "left": left,
                        "bottom": bottom,
                        "right": right,
                    }

                    if self._contains_only_this_clue(rectangle, clue):
                        candidates.append(rectangle)

        return candidates

    def _contains_only_this_clue(self, rectangle, clue):
        clue_row, clue_col, _ = clue

        for row in range(rectangle["top"], rectangle["bottom"] + 1):
            for col in range(rectangle["left"], rectangle["right"] + 1):
                if self.board[row][col] > 0 and (row, col) != (clue_row, clue_col):
                    return False
        return True

    def _passes_initial_checks(self):
        if not self.clues:
            return False
            
        total_clue_area = sum(value for _, _, value in self.clues)
        if total_clue_area != self.rows * self.cols:
            return False
            
        for clue in self.clues:
            if len(self.candidates_by_clue[clue]) == 0:
                return False
                
        return True

    def solve(self):
        """Return a list of rectangles if there is a solution, otherwise None."""
        self._reset_stats()
        start = perf_counter()

        if not self._passes_initial_checks():
            self.stats["elapsed_ms"] = self._elapsed_ms(start)
            return None

        occupied = [[False for _ in range(self.cols)] for _ in range(self.rows)]
        solution = []
        remaining_clues = set(self.clues)

        if self._backtrack(remaining_clues, occupied, solution):
            self.stats["solutions_found"] = 1
            self.stats["elapsed_ms"] = self._elapsed_ms(start)
            return solution
            
        self.stats["elapsed_ms"] = self._elapsed_ms(start)
        return None

    def solve_all(self, limit=2):
        self._reset_stats()
        start = perf_counter()

        if not self._passes_initial_checks():
            self.stats["elapsed_ms"] = self._elapsed_ms(start)
            return []

        occupied = [[False for _ in range(self.cols)] for _ in range(self.rows)]
        solution = []
        remaining_clues = set(self.clues)
        
        found_solutions = []
        self._backtrack_collect(remaining_clues, occupied, solution, found_solutions, limit)

        self.stats["solutions_found"] = len(found_solutions)
        self.stats["elapsed_ms"] = self._elapsed_ms(start)
        return found_solutions

    def solve_with_steps(self):
        self._reset_stats()
        start = perf_counter()

        if not self._passes_initial_checks():
            self.stats["elapsed_ms"] = self._elapsed_ms(start)
            yield {
                "type": "no_solution",
                "rectangle": None,
                "solution": [],
                "stats": self.get_stats(),
            }
            return

        occupied = [[False for _ in range(self.cols)] for _ in range(self.rows)]
        solution = []
        remaining_clues = set(self.clues)

        solved = yield from self._backtrack_steps(remaining_clues, occupied, solution)

        if solved:
            self.stats["solutions_found"] = 1
            self.stats["elapsed_ms"] = self._elapsed_ms(start)
            yield {
                "type": "solution",
                "rectangle": None,
                "solution": solution.copy(),
                "stats": self.get_stats(),
            }
        else:
            self.stats["elapsed_ms"] = self._elapsed_ms(start)
            yield {
                "type": "no_solution",
                "rectangle": None,
                "solution": solution.copy(),
                "stats": self.get_stats(),
            }

    # -- Heuristics & Helpers --

    def _get_feasible_candidates(self, clue, occupied):
        return [rect for rect in self.candidates_by_clue[clue] if self._can_place(rect, occupied)]

    def _select_next_clue_mrv(self, remaining_clues, occupied):
        best_clue = None
        min_options = float('inf')
        
        for clue in remaining_clues:
            options = len(self._get_feasible_candidates(clue, occupied))
            if options < min_options:
                min_options = options
                best_clue = clue
                
        return best_clue, min_options

    def _order_candidates_lcv(self, candidates, remaining_clues, occupied):
        def score(rect):
            return self._candidate_flexibility_score(rect, remaining_clues, occupied)
        
        return sorted(candidates, key=score, reverse=True)

    def _candidate_flexibility_score(self, rectangle, remaining_clues, occupied):
        self._place(rectangle, occupied, True)
        total_remaining_options = 0
        for clue in remaining_clues:
            total_remaining_options += len(self._get_feasible_candidates(clue, occupied))
        self._place(rectangle, occupied, False)
        return total_remaining_options

    def _forward_check(self, remaining_clues, occupied):
        for clue in remaining_clues:
            if not self._get_feasible_candidates(clue, occupied):
                return False
        return True

    def _uncovered_cells_can_be_covered(self, remaining_clues, occupied):
        feasible_rectangles = []
        for clue in remaining_clues:
            feasible_rectangles.extend(self._get_feasible_candidates(clue, occupied))

        for row in range(self.rows):
            for col in range(self.cols):
                if not occupied[row][col]:
                    if not self._cell_can_be_covered(row, col, feasible_rectangles):
                        return False
        return True

    def _cell_can_be_covered(self, row, col, feasible_rectangles):
        for rect in feasible_rectangles:
            if self._rectangle_contains_cell(rect, row, col):
                return True
        return False

    def _rectangle_contains_cell(self, rectangle, row, col):
        return (rectangle["top"] <= row <= rectangle["bottom"] and
                rectangle["left"] <= col <= rectangle["right"])

    def _can_place(self, rectangle, occupied):
        for row in range(rectangle["top"], rectangle["bottom"] + 1):
            for col in range(rectangle["left"], rectangle["right"] + 1):
                if occupied[row][col]:
                    return False
        return True

    def _place(self, rectangle, occupied, value):
        for row in range(rectangle["top"], rectangle["bottom"] + 1):
            for col in range(rectangle["left"], rectangle["right"] + 1):
                occupied[row][col] = value

    # -- Backtracking Variants --

    def _backtrack(self, remaining_clues, occupied, solution):
        self.stats["recursive_calls"] += 1
        self.stats["max_depth"] = max(self.stats["max_depth"], len(solution))

        if not remaining_clues:
            return True

        clue, options_count = self._select_next_clue_mrv(remaining_clues, occupied)
        if options_count == 0:
            return False

        remaining_clues.remove(clue)
        candidates = self._get_feasible_candidates(clue, occupied)
        candidates = self._order_candidates_lcv(candidates, remaining_clues, occupied)

        for rectangle in candidates:
            self.stats["candidates_tested"] += 1

            if not self._can_place(rectangle, occupied):
                self.stats["overlap_rejections"] += 1
                continue

            self._place(rectangle, occupied, True)
            solution.append(rectangle)
            self.stats["placements"] += 1

            if not self._forward_check(remaining_clues, occupied):
                self.stats["forward_prunes"] += 1
            elif not self._uncovered_cells_can_be_covered(remaining_clues, occupied):
                self.stats["cell_prunes"] += 1
            else:
                if self._backtrack(remaining_clues, occupied, solution):
                    return True

            solution.pop()
            self._place(rectangle, occupied, False)
            self.stats["backtracks"] += 1

        remaining_clues.add(clue)
        return False

    def _backtrack_collect(self, remaining_clues, occupied, solution, found_solutions, limit):
        self.stats["recursive_calls"] += 1
        self.stats["max_depth"] = max(self.stats["max_depth"], len(solution))

        if not remaining_clues:
            found_solutions.append(solution.copy())
            return

        if len(found_solutions) >= limit:
            return

        clue, options_count = self._select_next_clue_mrv(remaining_clues, occupied)
        if options_count == 0:
            return

        remaining_clues.remove(clue)
        candidates = self._get_feasible_candidates(clue, occupied)
        candidates = self._order_candidates_lcv(candidates, remaining_clues, occupied)

        for rectangle in candidates:
            if len(found_solutions) >= limit:
                break
                
            self.stats["candidates_tested"] += 1

            if not self._can_place(rectangle, occupied):
                self.stats["overlap_rejections"] += 1
                continue

            self._place(rectangle, occupied, True)
            solution.append(rectangle)
            self.stats["placements"] += 1

            if not self._forward_check(remaining_clues, occupied):
                self.stats["forward_prunes"] += 1
            elif not self._uncovered_cells_can_be_covered(remaining_clues, occupied):
                self.stats["cell_prunes"] += 1
            else:
                self._backtrack_collect(remaining_clues, occupied, solution, found_solutions, limit)

            solution.pop()
            self._place(rectangle, occupied, False)
            self.stats["backtracks"] += 1

        remaining_clues.add(clue)

    def _backtrack_steps(self, remaining_clues, occupied, solution):
        self.stats["recursive_calls"] += 1
        self.stats["max_depth"] = max(self.stats["max_depth"], len(solution))

        if not remaining_clues:
            return True

        clue, options_count = self._select_next_clue_mrv(remaining_clues, occupied)
        if options_count == 0:
            yield {
                "type": "dead_end",
                "rectangle": None,
                "solution": solution.copy(),
                "stats": self.get_stats(),
            }
            return False

        remaining_clues.remove(clue)
        
        all_candidates_for_clue = self.candidates_by_clue[clue]
        feasible = [r for r in all_candidates_for_clue if self._can_place(r, occupied)]
        infeasible = [r for r in all_candidates_for_clue if not self._can_place(r, occupied)]
        
        feasible_sorted = self._order_candidates_lcv(feasible, remaining_clues, occupied)
        candidates_to_try = feasible_sorted + infeasible

        for rectangle in candidates_to_try:
            self.stats["candidates_tested"] += 1
            yield {
                "type": "try",
                "rectangle": rectangle,
                "solution": solution.copy(),
                "stats": self.get_stats(),
            }

            if not self._can_place(rectangle, occupied):
                self.stats["overlap_rejections"] += 1
                yield {
                    "type": "reject_overlap",
                    "rectangle": rectangle,
                    "solution": solution.copy(),
                    "stats": self.get_stats(),
                }
                continue

            self._place(rectangle, occupied, True)
            solution.append(rectangle)
            self.stats["placements"] += 1
            
            yield {
                "type": "place",
                "rectangle": rectangle,
                "solution": solution.copy(),
                "stats": self.get_stats(),
            }

            if not self._forward_check(remaining_clues, occupied):
                self.stats["forward_prunes"] += 1
                yield {
                    "type": "reject_forward_check",
                    "rectangle": rectangle,
                    "solution": solution.copy(),
                    "stats": self.get_stats(),
                }
            elif not self._uncovered_cells_can_be_covered(remaining_clues, occupied):
                self.stats["cell_prunes"] += 1
                yield {
                    "type": "reject_uncoverable_cell",
                    "rectangle": rectangle,
                    "solution": solution.copy(),
                    "stats": self.get_stats(),
                }
            else:
                solved = yield from self._backtrack_steps(remaining_clues, occupied, solution)
                if solved:
                    return True

            solution.pop()
            self._place(rectangle, occupied, False)
            self.stats["backtracks"] += 1
            
            yield {
                "type": "remove",
                "rectangle": rectangle,
                "solution": solution.copy(),
                "stats": self.get_stats(),
            }

        remaining_clues.add(clue)
        return False
