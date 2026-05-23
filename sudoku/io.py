"""
Parse and write sudoku puzzles in different formats.

Supports:
- 81-char string (digits 1-9, 0 or . for empty)
- 9x9 list of lists
- Plain text file with one row per line
"""


def parse_string(s):
    """Take an 81-char string and return a 9x9 list of lists.
    0 and . both mean empty (we store empty as 0)."""
    s = s.strip().replace(".", "0")
    if len(s) != 81:
        raise ValueError(f"expected 81 chars, got {len(s)}")
    grid = []
    for r in range(9):
        row = [int(c) for c in s[r*9:(r+1)*9]]
        grid.append(row)
    return grid


def to_string(grid):
    """Take a 9x9 grid and return the 81-char string version."""
    return "".join(str(grid[r][c]) for r in range(9) for c in range(9))


def parse_text_file(path):
    """Read a text file with one row of 9 digits per line."""
    with open(path) as f:
        lines = [line.strip() for line in f if line.strip()]
    if len(lines) != 9:
        raise ValueError(f"expected 9 lines, got {len(lines)}")
    grid = []
    for line in lines:
        # strip spaces in case the file is formatted like "5 3 0 0 7 0 0 0 0"
        digits = [c for c in line if c.isdigit() or c == "."]
        if len(digits) != 9:
            raise ValueError(f"expected 9 digits per row, got {len(digits)}")
        grid.append([0 if c == "." else int(c) for c in digits])
    return grid


def pretty_print(grid):
    """Print the grid in a nicer format with separator lines."""
    out = []
    for r in range(9):
        if r % 3 == 0 and r != 0:
            out.append("- - - + - - - + - - -")
        row = []
        for c in range(9):
            if c % 3 == 0 and c != 0:
                row.append("|")
            row.append(str(grid[r][c]) if grid[r][c] != 0 else ".")
        out.append(" ".join(row))
    return "\n".join(out)
