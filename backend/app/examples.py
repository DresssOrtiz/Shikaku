"""Example boards for the Shikaku solver.

Use 0 for empty cells and positive integers for clues.
"""


# Small 2x2 board. Each clue with value 2 must become a domino.
BOARD_2X2 = [
    [2, 0],
    [0, 2],
]


# Small 3x3 board. The center clue occupies one cell, and the other
# clues form rectangles of area 2.
BOARD_3X3 = [
    [2, 0, 2],
    [0, 1, 0],
    [2, 0, 2],
]


# Slightly larger valid board with mixed rectangle sizes.
BOARD_4X4 = [
    [4, 0, 2, 0],
    [0, 0, 0, 0],
    [3, 0, 0, 3],
    [0, 0, 4, 0],
]


# 4x5 board with five rectangles of different sizes.
BOARD_4X5 = [
    [4, 0, 3, 0, 0],
    [0, 0, 3, 0, 6],
    [0, 0, 0, 0, 0],
    [4, 0, 0, 0, 0],
]


# 5x5 board with a full top row and several vertical rectangles.
BOARD_5X5 = [
    [5, 0, 0, 0, 0],
    [6, 0, 0, 0, 3],
    [0, 0, 6, 0, 0],
    [0, 0, 0, 0, 0],
    [4, 0, 0, 0, 1],
]


# Board where the sum of clues does not match the area (invalid sum)
BOARD_INVALID_SUM = [
    [5, 0],
    [0, 5],
]

# Board with no possible valid solution (real impossibility)
BOARD_NO_SOLUTION = [
    [3, 0],
    [0, 2],
]

# Board with multiple valid solutions (ambiguous)
BOARD_MULTIPLE_SOLUTIONS = [
    [2, 2],
    [0, 0],
]

# Medium board (for benchmarking)
BOARD_MEDIUM = [
    [6, 0, 0, 0, 0, 6],
    [0, 0, 0, 0, 0, 0],
    [4, 0, 4, 0, 4, 0],
    [0, 0, 0, 0, 0, 0],
    [8, 0, 0, 0, 0, 4],
    [0, 0, 0, 0, 0, 0],
]

# Hard board (for benchmarking the effectiveness of prunes)
BOARD_HARD = [
    [0, 9, 0, 0, 0, 12, 0],
    [0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0],
    [6, 0, 0, 4, 0, 0, 4],
    [0, 0, 0, 0, 0, 0, 0],
    [0, 0, 8, 0, 0, 6, 0],
    [0, 0, 0, 0, 0, 0, 0],
]

EXAMPLES = {
    "2x2": BOARD_2X2,
    "3x3": BOARD_3X3,
    "4x4": BOARD_4X4,
    "4x5": BOARD_4X5,
    "5x5": BOARD_5X5,
    "invalid_sum": BOARD_INVALID_SUM,
    "no_solution": BOARD_NO_SOLUTION,
    "multiple_solutions": BOARD_MULTIPLE_SOLUTIONS,
    "medium": BOARD_MEDIUM,
    "hard": BOARD_HARD,
}
