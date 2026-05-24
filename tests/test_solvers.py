"""
Run with: pytest tests/

Tests cover I/O round-tripping, the solution verifier, and both solvers
running on a known puzzle.
"""

import pytest
from sudoku import (
    parse_string, to_string, is_solved, matches_clues,
    PlainBacktrackingSolver, CSPSolver, XSolver
)


EASY_PUZZLE = "530070000600195000098000060800060003400803001700020006060000280000419005000080079"
EASY_SOLUTION = "534678912672195348198342567859761423426853791713924856961537284287419635345286179"


def test_parse_and_dump():
    grid = parse_string(EASY_PUZZLE)
    assert len(grid) == 9
    assert all(len(row) == 9 for row in grid)
    assert to_string(grid) == EASY_PUZZLE


def test_parse_with_dots():
    s = EASY_PUZZLE.replace("0", ".")
    grid = parse_string(s)
    assert to_string(grid) == EASY_PUZZLE


def test_is_solved_true():
    grid = parse_string(EASY_SOLUTION)
    assert is_solved(grid)


def test_is_solved_false_incomplete():
    grid = parse_string(EASY_PUZZLE)
    assert not is_solved(grid)


def test_is_solved_false_wrong():
    grid = parse_string(EASY_SOLUTION)
    grid[0][0] = grid[0][1]  # duplicate in row 0
    assert not is_solved(grid)


def test_matches_clues():
    original = parse_string(EASY_PUZZLE)
    solution = parse_string(EASY_SOLUTION)
    assert matches_clues(original, solution)


def test_plain_backtracking_solves_easy():
    solver = PlainBacktrackingSolver()
    grid = parse_string(EASY_PUZZLE)
    solved, stats = solver.solve(grid)
    assert solved is not None
    assert is_solved(solved)
    assert matches_clues(grid, solved)
    assert stats["solved"] is True
    print(f"plain bt: {stats['time_seconds']:.4f}s, "
          f"{stats['nodes_expanded']} nodes, {stats['backtracks']} backtracks")

def test_csp_solves_easy():
    solver = CSPSolver()
    grid = parse_string(EASY_PUZZLE)
    solved, stats = solver.solve(grid)
    assert solved is not None
    assert is_solved(solved)
    assert matches_clues(grid, solved)
    assert stats["solved"] is True
    print(f"csp: {stats['time_seconds']:.4f}s, "
          f"{stats['nodes_expanded']} nodes, {stats['backtracks']} backtracks")
    
def test_x_solves_easy():
    solver = XSolver()
    grid = parse_string(EASY_PUZZLE)
    solved, stats = solver.solve(grid)
    assert solved is not None
    assert is_solved(solved)
    assert matches_clues(grid, solved)
    assert stats["solved"] is True
    print(f"x: {stats['time_seconds']:.4f}s, "
          f"{stats['nodes_expanded']} nodes, {stats['backtracks']} backtracks")

def test_solvers_agree():
    """Solvers should produce the same correct solution."""
    s1 = PlainBacktrackingSolver()
    s2 = CSPSolver()
    s3 = XSolver()
    grid = parse_string(EASY_PUZZLE)
    sol1, _ = s1.solve(grid)
    sol2, _ = s2.solve(grid)
    sol3, _ = s3.solve(grid)
    assert to_string(sol1) == to_string(sol2) and to_string(sol2) == to_string(sol3)
