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


EXAMPLES = {
    "2x2": BOARD_2X2,
    "3x3": BOARD_3X3,
    "4x4": BOARD_4X4,
    "4x5": BOARD_4X5,
    "5x5": BOARD_5X5,
}
