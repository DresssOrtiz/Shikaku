"""Backtracking solver for the Shikaku puzzle.

The code is intentionally direct: generate every valid rectangle for each
clue, then use backtracking with simple pruning to choose one rectangle per
clue without overlaps.
"""


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

    def solve(self):
        """Return a list of rectangles if there is a solution, otherwise None."""
        total_clue_area = sum(value for _, _, value in self.clues)
        if total_clue_area != self.rows * self.cols:
            return None

        # Pruning: start with the most restricted clues first.
        ordered_clues = sorted(
            self.clues,
            key=lambda clue: len(self.candidates_by_clue[clue]),
        )

        if any(len(self.candidates_by_clue[clue]) == 0 for clue in ordered_clues):
            return None

        occupied = [[False for _ in range(self.cols)] for _ in range(self.rows)]
        solution = []

        if self._backtrack(ordered_clues, 0, occupied, solution):
            return solution
        return None

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

            # Move the rectangle around the clue cell while keeping its size.
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

    def _backtrack(self, ordered_clues, index, occupied, solution):
        if index == len(ordered_clues):
            return self._all_cells_covered(occupied)

        clue = ordered_clues[index]

        for rectangle in self.candidates_by_clue[clue]:
            # Main pruning: do not try rectangles that overlap occupied cells.
            if self._can_place(rectangle, occupied):
                self._place(rectangle, occupied, True)
                solution.append(rectangle)

                if self._backtrack(ordered_clues, index + 1, occupied, solution):
                    return True

                # Undo the choice and try the next candidate.
                solution.pop()
                self._place(rectangle, occupied, False)

        return False

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

    def _all_cells_covered(self, occupied):
        for row in range(self.rows):
            for col in range(self.cols):
                if not occupied[row][col]:
                    return False
        return True
