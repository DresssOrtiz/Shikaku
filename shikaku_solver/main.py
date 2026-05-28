from examples import EXAMPLES
from gui import ShikakuGUI
from solver import ShikakuSolver


def print_board(board):
    for row in board:
        print(" ".join(str(value).rjust(2) for value in row))


def print_rectangles(solution):
    for index, rectangle in enumerate(solution, start=1):
        clue = rectangle["clue"]
        print(
            f"{index}. Clue {clue} -> "
            f"top={rectangle['top']}, left={rectangle['left']}, "
            f"bottom={rectangle['bottom']}, right={rectangle['right']}"
        )


def build_solution_matrix(board, solution):
    rows = len(board)
    cols = len(board[0])
    matrix = [["." for _ in range(cols)] for _ in range(rows)]

    for index, rectangle in enumerate(solution):
        label = get_label(index)
        for row in range(rectangle["top"], rectangle["bottom"] + 1):
            for col in range(rectangle["left"], rectangle["right"] + 1):
                matrix[row][col] = label

    return matrix


def get_label(index):
    """Return A, B, C... Z, then R27, R28... if there are many rectangles."""
    if index < 26:
        return chr(ord("A") + index)
    return f"R{index + 1}"


def print_solution_matrix(matrix):
    for row in matrix:
        print(" ".join(str(value).rjust(2) for value in row))


def run_console_example():
    board = EXAMPLES["4x4"]
    solver = ShikakuSolver(board)
    solution = solver.solve()

    print("Original board:")
    print_board(board)
    print()

    if solution is None:
        print("No solution was found for this board.")
        return

    print("Rectangles found:")
    print_rectangles(solution)
    print()

    print("Solution matrix:")
    solution_matrix = build_solution_matrix(board, solution)
    print_solution_matrix(solution_matrix)


def main():
    app = ShikakuGUI()
    app.run()


if __name__ == "__main__":
    main()
