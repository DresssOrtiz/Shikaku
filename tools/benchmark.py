import sys
from examples import EXAMPLES
from solver import ShikakuSolver

def run_benchmarks():
    print(f"{'Tablero':<20} | {'Estado':<12} | {'Tiempo ms':>10} | {'Recursiones':>11} | {'Candidatos':>10} | {'Backtracks':>10} | {'Podas':>5}")
    print("-" * 92)

    for name, board in EXAMPLES.items():
        solver = ShikakuSolver(board)
        solution = solver.solve()
        stats = solver.get_stats()
        
        estado = "Solución" if solution is not None else "Sin solución"
        tiempo = f"{stats['elapsed_ms']:.2f}"
        recursiones = stats['recursive_calls']
        candidatos = stats['candidates_tested']
        backtracks = stats['backtracks']
        podas = stats['forward_prunes'] + stats['cell_prunes']
        
        print(f"{name:<20} | {estado:<12} | {tiempo:>10} | {recursiones:>11} | {candidatos:>10} | {backtracks:>10} | {podas:>5}")

if __name__ == "__main__":
    run_benchmarks()
