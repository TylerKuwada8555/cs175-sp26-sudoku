"""
Check whether a solved sudoku is actually correct.
"""


def is_solved(grid):
    """Returns True if grid is a complete and valid sudoku solution."""
    expected = set(range(1, 10))

    # check rows
    for r in range(9):
        if set(grid[r]) != expected:
            return False

    # check columns
    for c in range(9):
        if set(grid[r][c] for r in range(9)) != expected:
            return False

    # check 3x3 boxes
    for box_r in range(3):
        for box_c in range(3):
            cells = set()
            for dr in range(3):
                for dc in range(3):
                    cells.add(grid[box_r*3+dr][box_c*3+dc])
            if cells != expected:
                return False

    return True


def matches_clues(original, solution):
    """Check that the solution agrees with all the given clues
    from the original puzzle (i.e. we didn't overwrite anything)."""
    for r in range(9):
        for c in range(9):
            if original[r][c] != 0 and original[r][c] != solution[r][c]:
                return False
    return True
