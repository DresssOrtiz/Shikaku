import sys
import os
sys.path.insert(0, os.path.abspath('c:/Users/sebas/Shikaku/Shikaku/backend'))
from app.solver import ShikakuSolver
from app.examples import EXAMPLES

board = EXAMPLES["4x4"]
solver = ShikakuSolver(board)
steps = list(solver.solve_with_steps())
print(f"Total steps: {len(steps)}")
if len(steps) > 0:
    print(f"First step: {steps[0]['type']}")
    print(f"Last step: {steps[-1]['type']}")
