from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional, Any, Dict
from app.solver import ShikakuSolver
from app.examples import EXAMPLES

app = FastAPI(title="Shikaku Solver API", root_path="/api")

class BoardRequest(BaseModel):
    board: List[List[int]]

class SolveResponse(BaseModel):
    solved: bool
    solution: List[Any]
    stats: Dict[str, Any]

def validate_board(board: List[List[int]]):
    if not board:
        raise HTTPException(status_code=400, detail="Board is empty")
    cols = len(board[0])
    for row in board:
        if len(row) != cols:
            raise HTTPException(status_code=400, detail="All rows must have the same length")
        for val in row:
            if not isinstance(val, int) or val < 0:
                raise HTTPException(status_code=400, detail="Values must be non-negative integers")
    if len(board) > 50 or cols > 50:
        raise HTTPException(status_code=400, detail="Board is too large")

@app.get("/health")
def health_check():
    return {"status": "ok"}

@app.get("/boards")
def get_boards():
    return {"boards": EXAMPLES}

@app.post("/solve", response_model=SolveResponse)
def solve_board(req: BoardRequest):
    validate_board(req.board)
    solver = ShikakuSolver(req.board)
    solution = solver.solve()
    stats = solver.get_stats()
    
    return SolveResponse(
        solved=solution is not None,
        solution=solution if solution is not None else [],
        stats=stats
    )

@app.post("/steps")
def solve_with_steps(req: BoardRequest):
    validate_board(req.board)
    solver = ShikakuSolver(req.board)
    steps = list(solver.solve_with_steps())
    return {"steps": steps}

@app.post("/solve-all")
def solve_all_boards(req: BoardRequest):
    validate_board(req.board)
    solver = ShikakuSolver(req.board)
    solutions = solver.solve_all(limit=2)
    stats = solver.get_stats()
    
    return {
        "solution_count": len(solutions),
        "solutions": solutions,
        "stats": stats
    }
