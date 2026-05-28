import tkinter as tk
from tkinter import messagebox

from examples import EXAMPLES
from solver import ShikakuSolver


class ShikakuGUI:
    def __init__(self):
        # Window creation and basic layout.
        self.root = tk.Tk()
        self.root.title("Solucionador Shikaku")

        self.cell_size = 70
        self.board = None
        self.animation_job = None
        self.decision_steps = None
        self.colors = [
            "#F8BBD0",
            "#BBDEFB",
            "#C8E6C9",
            "#FFE0B2",
            "#D1C4E9",
            "#B2DFDB",
            "#FFF9C4",
            "#FFCCBC",
            "#DCEDC8",
            "#E1BEE7",
        ]

        self.canvas = tk.Canvas(self.root, bg="white")
        self.canvas.pack(padx=10, pady=10)

        examples_frame = tk.Frame(self.root)
        examples_frame.pack(pady=(0, 5))

        tk.Button(
            examples_frame,
            text="Cargar ejemplo 1",
            command=lambda: self.load_board(EXAMPLES["3x3"]),
        ).pack(side=tk.LEFT, padx=5)

        tk.Button(
            examples_frame,
            text="Cargar ejemplo 2",
            command=lambda: self.load_board(EXAMPLES["4x4"]),
        ).pack(side=tk.LEFT, padx=5)

        tk.Button(
            examples_frame,
            text="Cargar ejemplo 3",
            command=lambda: self.load_board(EXAMPLES["2x2"]),
        ).pack(side=tk.LEFT, padx=5)

        tk.Button(
            examples_frame,
            text="Cargar ejemplo 4",
            command=lambda: self.load_board(EXAMPLES["4x5"]),
        ).pack(side=tk.LEFT, padx=5)

        tk.Button(
            examples_frame,
            text="Cargar ejemplo 5",
            command=lambda: self.load_board(EXAMPLES["5x5"]),
        ).pack(side=tk.LEFT, padx=5)

        action_frame = tk.Frame(self.root)
        action_frame.pack(pady=(0, 10))

        tk.Button(action_frame, text="Resolver", command=self.solve_board).pack(
            side=tk.LEFT,
            padx=5,
        )

        tk.Button(
            action_frame,
            text="Ver decisiones",
            command=self.show_decisions,
        ).pack(side=tk.LEFT, padx=5)

        tk.Button(
            action_frame,
            text="Limpiar solución",
            command=self.clear_solution,
        ).pack(side=tk.LEFT, padx=5)

        speed_frame = tk.Frame(self.root)
        speed_frame.pack(pady=(0, 10))

        tk.Label(speed_frame, text="Velocidad:").pack(side=tk.LEFT, padx=5)

        self.speed_scale = tk.Scale(
            speed_frame,
            from_=50,
            to=1000,
            orient=tk.HORIZONTAL,
            length=250,
            label="Pausa entre pasos (ms)",
        )
        self.speed_scale.set(300)
        self.speed_scale.pack(side=tk.LEFT)

        self.load_board(EXAMPLES["3x3"])

    def run(self):
        self.root.mainloop()

    def load_board(self, board):
        self.stop_animation()
        self.board = board
        self.draw_board()

    def clear_solution(self):
        self.stop_animation()
        self.draw_board()

    def solve_board(self):
        self.stop_animation()

        if self.board is None:
            messagebox.showinfo("Sin tablero", "Primero carga un ejemplo.")
            return

        # Solver call: reuse the backtracking class from solver.py.
        solver = ShikakuSolver(self.board)
        solution = solver.solve()

        if solution is None:
            messagebox.showinfo("Sin solución", "No se encontró solución para este tablero.")
            return

        self.draw_solution(solution)

    def show_decisions(self):
        self.stop_animation()

        if self.board is None:
            messagebox.showinfo("Sin tablero", "Primero carga un ejemplo.")
            return

        solver = ShikakuSolver(self.board)
        self.decision_steps = self.generate_decision_steps(solver)
        self.play_next_step()

    def stop_animation(self):
        if self.animation_job is not None:
            self.root.after_cancel(self.animation_job)
            self.animation_job = None
        self.decision_steps = None

    def play_next_step(self):
        try:
            step_type, partial_solution, rectangle = next(self.decision_steps)
        except StopIteration:
            self.animation_job = None
            return

        if step_type == "try":
            self.draw_partial_solution(partial_solution, rectangle, "blue")
        elif step_type == "reject":
            self.draw_partial_solution(partial_solution, rectangle, "red")
        elif step_type == "place":
            self.draw_partial_solution(partial_solution)
        elif step_type == "remove":
            self.draw_partial_solution(partial_solution, rectangle, "orange")
        elif step_type == "solution":
            self.draw_solution(partial_solution)
            self.animation_job = None
            return
        elif step_type == "no_solution":
            self.draw_board()
            messagebox.showinfo("Sin solución", "No se encontró solución para este tablero.")
            self.animation_job = None
            return

        delay = self.speed_scale.get()
        self.animation_job = self.root.after(delay, self.play_next_step)

    def generate_decision_steps(self, solver):
        total_area = sum(value for _, _, value in solver.clues)
        if total_area != solver.rows * solver.cols:
            yield ("no_solution", [], None)
            return

        # Same pruning idea as the solver: start with the clue with fewer options.
        ordered_clues = sorted(
            solver.clues,
            key=lambda clue: len(solver.candidates_by_clue[clue]),
        )

        if any(len(solver.candidates_by_clue[clue]) == 0 for clue in ordered_clues):
            yield ("no_solution", [], None)
            return

        occupied = [[False for _ in range(solver.cols)] for _ in range(solver.rows)]
        solution = []

        solved = yield from self.backtracking_steps(
            solver,
            ordered_clues,
            0,
            occupied,
            solution,
        )

        if solved:
            yield ("solution", solution.copy(), None)
        else:
            yield ("no_solution", [], None)

    def backtracking_steps(self, solver, ordered_clues, index, occupied, solution):
        if index == len(ordered_clues):
            return solver._all_cells_covered(occupied)

        clue = ordered_clues[index]

        for rectangle in solver.candidates_by_clue[clue]:
            # Show the candidate before accepting or rejecting it.
            yield ("try", solution.copy(), rectangle)

            if solver._can_place(rectangle, occupied):
                solver._place(rectangle, occupied, True)
                solution.append(rectangle)
                yield ("place", solution.copy(), None)

                solved = yield from self.backtracking_steps(
                    solver,
                    ordered_clues,
                    index + 1,
                    occupied,
                    solution,
                )
                if solved:
                    return True

                removed = solution.pop()
                solver._place(removed, occupied, False)
                yield ("remove", solution.copy(), removed)
            else:
                # Main pruning shown visually: red means overlap with occupied cells.
                yield ("reject", solution.copy(), rectangle)

        return False

    def draw_board(self):
        # Grid drawing: every cell starts white and clues are drawn on top.
        rows = len(self.board)
        cols = len(self.board[0])

        self.canvas.config(
            width=cols * self.cell_size,
            height=rows * self.cell_size,
        )
        self.canvas.delete("all")

        for row in range(rows):
            for col in range(cols):
                self.draw_cell(row, col, "white")

        self.draw_clues()

    def draw_partial_solution(self, partial_solution, rectangle=None, outline_color=None):
        self.draw_board()

        for index, placed_rectangle in enumerate(partial_solution):
            color = self.colors[index % len(self.colors)]
            for row in range(placed_rectangle["top"], placed_rectangle["bottom"] + 1):
                for col in range(placed_rectangle["left"], placed_rectangle["right"] + 1):
                    self.draw_cell(row, col, color)

        if rectangle is not None and outline_color is not None:
            self.draw_rectangle_outline(rectangle, outline_color)

        self.draw_clues()

    def draw_solution(self, solution):
        self.draw_board()

        # Solution drawing: each selected rectangle receives a different color.
        for index, rectangle in enumerate(solution):
            color = self.colors[index % len(self.colors)]
            for row in range(rectangle["top"], rectangle["bottom"] + 1):
                for col in range(rectangle["left"], rectangle["right"] + 1):
                    self.draw_cell(row, col, color)

        self.draw_clues()

    def draw_rectangle_outline(self, rectangle, color):
        x1 = rectangle["left"] * self.cell_size
        y1 = rectangle["top"] * self.cell_size
        x2 = (rectangle["right"] + 1) * self.cell_size
        y2 = (rectangle["bottom"] + 1) * self.cell_size

        self.canvas.create_rectangle(
            x1,
            y1,
            x2,
            y2,
            outline=color,
            width=5,
        )

    def draw_cell(self, row, col, color):
        x1 = col * self.cell_size
        y1 = row * self.cell_size
        x2 = x1 + self.cell_size
        y2 = y1 + self.cell_size

        self.canvas.create_rectangle(
            x1,
            y1,
            x2,
            y2,
            fill=color,
            outline="black",
            width=2,
        )

    def draw_clues(self):
        for row in range(len(self.board)):
            for col in range(len(self.board[0])):
                value = self.board[row][col]
                if value > 0:
                    x = col * self.cell_size + self.cell_size / 2
                    y = row * self.cell_size + self.cell_size / 2
                    self.canvas.create_text(
                        x,
                        y,
                        text=str(value),
                        font=("Arial", 18, "bold"),
                        fill="black",
                    )


def main():
    app = ShikakuGUI()
    app.run()


if __name__ == "__main__":
    main()
