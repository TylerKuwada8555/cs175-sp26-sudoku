"""
Solver 1: Plain Backtracking.

No constraint propagation, no heuristics. Just try values 1-9 in order
for the first empty cell, recurse, backtrack on conflict. This is the
baseline that the other solvers get compared against.
"""

import time


class SolverTimeout(Exception):
    pass


class PlainBacktrackingSolver:
    name = "plain_backtracking"

    def __init__(self):
        self.nodes_expanded = 0
        self.backtracks = 0
        self.deadline = None

    def solve(self, grid, timeout_seconds=None):
        """Solve the puzzle in place. Returns (solved_grid, stats_dict)."""
        # work on a copy so we don't mutate the original
        board = [row[:] for row in grid]
        self.nodes_expanded = 0
        self.backtracks = 0

        start = time.perf_counter()
        self.deadline = (
            start + timeout_seconds
            if timeout_seconds is not None
            else None
        )

        try:
            ok = self._backtrack(board)
            elapsed = time.perf_counter() - start

            stats = {
                "solver": self.name,
                "solved": ok,
                "time_seconds": elapsed,
                "nodes_expanded": self.nodes_expanded,
                "backtracks": self.backtracks,
            }
            return (board if ok else None), stats

        except SolverTimeout:
            elapsed = time.perf_counter() - start

            stats = {
                "solver": self.name,
                "solved": False,
                "time_seconds": elapsed,
                "nodes_expanded": self.nodes_expanded,
                "backtracks": self.backtracks,
                "timeout": True,
            }
            return None, stats

    def _check_timeout(self):
        if self.deadline is not None and time.perf_counter() > self.deadline:
            raise SolverTimeout()

    def _find_empty(self, board):
        """Find the next empty cell (left to right, top to bottom)."""
        for r in range(9):
            for c in range(9):
                if board[r][c] == 0:
                    return (r, c)
        return None

    def _is_valid(self, board, r, c, val):
        """Check if placing val at (r,c) breaks any constraint."""
        # row
        for cc in range(9):
            if board[r][cc] == val:
                return False
        # column
        for rr in range(9):
            if board[rr][c] == val:
                return False
        # 3x3 box
        box_r, box_c = (r // 3) * 3, (c // 3) * 3
        for dr in range(3):
            for dc in range(3):
                if board[box_r+dr][box_c+dc] == val:
                    return False
        return True

    def _backtrack(self, board):
        self._check_timeout()

        self.nodes_expanded += 1
        empty = self._find_empty(board)
        if empty is None:
            return True  # solved

        r, c = empty
        for val in range(1, 10):
            self._check_timeout()

            if self._is_valid(board, r, c, val):
                board[r][c] = val
                if self._backtrack(board):
                    return True
                board[r][c] = 0
                self.backtracks += 1
        return False