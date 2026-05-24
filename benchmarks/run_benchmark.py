"""
Run every solver against every puzzle in the bank and print a summary.

Usage: python benchmarks/run_benchmark.py

Output is a markdown table you can paste into the progress report.
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from sudoku import (
    parse_string, to_string, is_solved,
    PlainBacktrackingSolver, CSPSolver, XSolver
)
from puzzles.bank import all_puzzles


SOLVERS = [PlainBacktrackingSolver, CSPSolver, XSolver]
TIMEOUT_SECONDS = 30  # skip plain bt on very hard puzzles to avoid hanging


def run_one(solver_cls, puzzle_str, skip_if_hard=False, difficulty=""):
    """Run a solver on a single puzzle. Returns the stats dict."""
    grid = parse_string(puzzle_str)
    solver = solver_cls()

    # rough heuristic: skip plain backtracking on 17-clue and expert
    # since it can take 200+ seconds (Hira et al.)
    if skip_if_hard and difficulty in ("expert", "17-clue") \
            and solver_cls.name == "plain_backtracking":
        return {
            "solver": solver_cls.name,
            "solved": None,
            "time_seconds": None,
            "nodes_expanded": None,
            "backtracks": None,
            "skipped": True,
        }

    solved, stats = solver.solve(grid)
    if solved is not None:
        assert is_solved(solved), f"{solver_cls.name} returned an invalid solution!"
    stats["skipped"] = False
    return stats


def main():
    bank = all_puzzles()
    print(f"Running {len(SOLVERS)} solvers on {len(bank)} puzzles\n")

    # results[solver_name][difficulty] = list of stats dicts
    results = {s.name: {} for s in SOLVERS}

    for difficulty, puzzle_str in bank:
        print(f"--- {difficulty}: {puzzle_str[:20]}... ---")
        for solver_cls in SOLVERS:
            stats = run_one(solver_cls, puzzle_str,
                           skip_if_hard=True, difficulty=difficulty)
            if stats["skipped"]:
                print(f"  {solver_cls.name}: SKIPPED (too slow on {difficulty})")
            else:
                print(f"  {solver_cls.name}: "
                      f"{stats['time_seconds']:.4f}s, "
                      f"{stats['nodes_expanded']} nodes, "
                      f"{stats['backtracks']} backtracks")
            results[solver_cls.name].setdefault(difficulty, []).append(stats)

    # Summary table
    print("\n\n=== Summary ===\n")
    print("| Difficulty | Solver | Avg time (s) | Avg nodes | Avg backtracks |")
    print("|---|---|---|---|---|")
    difficulties = ["easy", "medium", "hard", "expert", "17-clue"]
    for diff in difficulties:
        for solver_cls in SOLVERS:
            stats_list = [s for s in results[solver_cls.name].get(diff, [])
                         if not s["skipped"]]
            if not stats_list:
                print(f"| {diff} | {solver_cls.name} | skipped | - | - |")
                continue
            n = len(stats_list)
            avg_time = sum(s["time_seconds"] for s in stats_list) / n
            avg_nodes = sum(s["nodes_expanded"] for s in stats_list) / n
            avg_bt = sum(s["backtracks"] for s in stats_list) / n
            print(f"| {diff} | {solver_cls.name} | "
                  f"{avg_time:.4f} | {avg_nodes:.0f} | {avg_bt:.0f} |")


if __name__ == "__main__":
    main()
