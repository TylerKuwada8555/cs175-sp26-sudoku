"""
Solver 2: Backtracking with AC-3 constraint propagation and MRV/LCV heuristics.

This is the "smart" CSP solver. The improvements over Solver 1:
  1. Each cell tracks a domain of possible values (not just one trial value).
  2. AC-3 propagates constraints after every assignment, shrinking domains.
  3. MRV picks the most constrained variable next (smallest domain).
  4. LCV tries values that leave the most options open for neighbors.

Reference: Russell & Norvig AIMA, ch. 6 (CSP).
Original AC-3: Mackworth 1977.
"""

import time
from collections import deque


def get_peers(r, c):
    """Return the set of (r,c) cells that share a row, column, or box
    with (r,c), excluding (r,c) itself."""
    peers = set()
    for cc in range(9):
        if cc != c:
            peers.add((r, cc))
    for rr in range(9):
        if rr != r:
            peers.add((rr, c))
    box_r, box_c = (r // 3) * 3, (c // 3) * 3
    for dr in range(3):
        for dc in range(3):
            rr, cc = box_r + dr, box_c + dc
            if (rr, cc) != (r, c):
                peers.add((rr, cc))
    return peers


# Precompute peers once, since they never change
PEERS = {(r, c): get_peers(r, c) for r in range(9) for c in range(9)}


class CSPSolver:
    name = "backtracking_ac3_mrv_lcv"

    def __init__(self):
        self.nodes_expanded = 0
        self.backtracks = 0

    def solve(self, grid):
        # build initial domains: singleton for clues, {1..9} otherwise
        domains = {}
        for r in range(9):
            for c in range(9):
                if grid[r][c] != 0:
                    domains[(r, c)] = {grid[r][c]}
                else:
                    domains[(r, c)] = set(range(1, 10))

        self.nodes_expanded = 0
        self.backtracks = 0
        start = time.perf_counter()

        # run AC-3 once at the start to prune obvious values
        if not self._ac3(domains):
            elapsed = time.perf_counter() - start
            return None, self._stats(False, elapsed)

        result = self._backtrack(domains)
        elapsed = time.perf_counter() - start

        if result is None:
            return None, self._stats(False, elapsed)

        # extract solution into a 9x9 grid
        solved = [[0]*9 for _ in range(9)]
        for (r, c), vals in result.items():
            solved[r][c] = next(iter(vals))
        return solved, self._stats(True, elapsed)

    def _stats(self, solved, elapsed):
        return {
            "solver": self.name,
            "solved": solved,
            "time_seconds": elapsed,
            "nodes_expanded": self.nodes_expanded,
            "backtracks": self.backtracks,
        }

    def _ac3(self, domains):
        """Standard AC-3. Returns False if a domain wipes out."""
        queue = deque()
        for cell in domains:
            for peer in PEERS[cell]:
                queue.append((cell, peer))

        while queue:
            xi, xj = queue.popleft()
            if self._revise(domains, xi, xj):
                if not domains[xi]:
                    return False
                for xk in PEERS[xi]:
                    if xk != xj:
                        queue.append((xk, xi))
        return True

    def _revise(self, domains, xi, xj):
        """Remove values from D[xi] that have no consistent partner in D[xj]."""
        revised = False
        # For AllDifferent: if xj has a singleton value v, then xi can't be v.
        if len(domains[xj]) == 1:
            v = next(iter(domains[xj]))
            if v in domains[xi]:
                domains[xi] = domains[xi] - {v}
                revised = True
        return revised

    def _select_unassigned(self, domains):
        """MRV: pick the unassigned cell with the smallest domain.
        Tie-break by degree (number of unassigned peers)."""
        unassigned = [(cell, d) for cell, d in domains.items() if len(d) > 1]
        if not unassigned:
            return None
        # min by (domain size, -degree)
        def key(item):
            cell, d = item
            degree = sum(1 for p in PEERS[cell] if len(domains[p]) > 1)
            return (len(d), -degree)
        return min(unassigned, key=key)[0]

    def _order_values(self, cell, domains):
        """LCV: try values that rule out the fewest options for peers first."""
        def count_conflicts(v):
            return sum(1 for p in PEERS[cell] if v in domains[p])
        return sorted(domains[cell], key=count_conflicts)

    def _backtrack(self, domains):
        self.nodes_expanded += 1

        cell = self._select_unassigned(domains)
        if cell is None:
            return domains  # all singletons, done

        for v in self._order_values(cell, domains):
            # save current state for restoration
            saved = {c: set(d) for c, d in domains.items()}

            # assign v
            domains[cell] = {v}

            # propagate
            if self._ac3(domains):
                result = self._backtrack(domains)
                if result is not None:
                    return result

            # restore on failure
            domains.clear()
            domains.update(saved)
            self.backtracks += 1

        return None
