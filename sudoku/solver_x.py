from collections import defaultdict, namedtuple
import time

Piece = namedtuple("Piece", "name constraints")

class XSolver:
    name = "algorithm_x"

    def __init__(self):
        self.nodes_expanded = 0
        self.backtracks = 0

    def encode(self, board):
        self.piece_to_constraints = defaultdict(set)
        # (i,j) is targeted cell
        # creates full range of possible values for all cells
        for i in range(9):
            for j in range(9):
                for digit in range(1, 10):
                    self.piece_to_constraints[digit, i, j].add(("cell", i, j))
                    self.piece_to_constraints[digit, i, j].add(("row", i, digit))
                    self.piece_to_constraints[digit, i, j].add(("column", j, digit))
                    self.piece_to_constraints[digit, i, j].add(("area", i//3, j//3, digit))
        # convert dict
        self.constraint_to_pieces = defaultdict(set)
        for piece_name, constraints in self.piece_to_constraints.items():
            # piece_name will be the digit and coordinate, constraints are those that that digit selection fulfills
            piece = Piece(piece_name, tuple(constraints))
            for constraint in constraints:
                # each constraint represents one of the digits needed for each axis (area, row, column)
                self.constraint_to_pieces[constraint].add(piece)

        # encode existing cells
        solution = []
        for i in range(9):
            for j in range(9):
                if board[i][j] != "0":
                    digit = int(board[i][j])
                    self.select(self.piece_to_constraints[digit, i, j])
                    solution.append((digit, i, j))
        return solution


    def select(self, constraints):
        other_pieces = []
        for constraint in constraints:
            # this constraint is now fulfilled:
            # all pieces that have this constraint can be removed from the other constraints
            for piece in self.constraint_to_pieces[constraint]:
                # piece is one of the pieces that would've fulfilled the current constraint
                for other_constraint in piece.constraints:
                    # other_constraints are the other that the piece is also in
                    if other_constraint != constraint:
                        self.constraint_to_pieces[other_constraint].remove(piece)
            # remove the constraint and store it for backtracking
            other_pieces.append(self.constraint_to_pieces.pop(constraint))
        self.nodes_expanded += 1
        return other_pieces

    def deselect(self, constraints, other_pieces):
        for constraint in reversed(constraints):
            self.constraint_to_pieces[constraint] = other_pieces.pop()
            for other_piece in self.constraint_to_pieces[constraint]:
                for other_constraint in other_piece.constraints:
                    if other_constraint != constraint:
                        self.constraint_to_pieces[other_constraint].add(other_piece)
        self.backtracks += 1
        return other_pieces
    
    def solve_cell(self, solution=None):
        # solution should only be None on highest level run
        if solution is None:   
            solution = []

        # if solved from this placement, constraint_to_pieces should be empty
        if not self.constraint_to_pieces:
            return solution
        
        # failure is indicated if there is a constraint with no pieces being able to satisfy it
        for k, v in self.constraint_to_pieces.items():
            if len(v) == 0:
                return False

        # pulls the constraint with the smallest list of possible values to solve first
        constraint = min(self.constraint_to_pieces, key=lambda c: len(self.constraint_to_pieces[c]))

        # loop through those possible values
        for piece in list(self.constraint_to_pieces[constraint]):
            solution.append(piece.name)
            other_pieces = self.select(piece.constraints)
            # recursive solve
            cur_selection = self.solve_cell(solution)
            # final solve should return and cause cascade of solution returns
            if cur_selection:
                return solution
            # should only be reached if the cur_selection is empty (failure case)
            self.deselect(piece.constraints, other_pieces)
            solution.pop()

        # if all possible values are exhausted for current level, need to go back further
        return False
    
    def solve(self, board):
        start = time.perf_counter()
    
        pre_solutions = self.encode(board)
        solutions = self.solve_cell()
        solved_grid = [[0 for _ in range(9)] for _ in range(9)]
        if solutions:
            solved = True
            solutions = pre_solutions + solutions
            for digit, i, j in solutions:
                solved_grid[i][j] = digit
        else:
            solved_grid = None
            solved = False
        elapsed = time.perf_counter() - start
        stats = {
            "solver": self.name,
            "solved": solved,
            "time_seconds": elapsed,
            "nodes_expanded": self.nodes_expanded,
            "backtracks": self.backtracks,
        }
        return solved_grid, stats