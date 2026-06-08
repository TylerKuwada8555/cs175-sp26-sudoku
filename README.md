# cs175-sp26-sudoku

Comparative study of classical algorithms for solving sudoku.
CS 175, Spring 2026, Prof. Kask.

**Team:** Mathieu Khalaf (mathieuk), Tyler Kuwada (tkuwada).

## Solvers

- **Solver 1: Plain Backtracking** (baseline) — `sudoku/solver_backtracking.py` (done)
- **Solver 2: Backtracking + AC-3 + MRV/LCV** — `sudoku/solver_csp.py` (done)
- **Solver 3: Dancing Links / Algorithm X** — `sudoku/solver_x.py` (done)

## How to run

### Locally (Python 3.11+)

```bash
pip install -r requirements.txt
python -m pytest tests/ -v          # run tests
python benchmarks/run_benchmark.py   # run benchmarks
```

### With Docker

```bash
docker build -t sudoku .
docker run -it -v ${PWD}:/workspace sudoku
# then inside the container:
python -m pytest tests/ -v
python benchmarks/run_benchmark.py
```

## Layout

```
sudoku/             Solver code
  io.py             Parse/print puzzles
  verify.py         Check whether a solved grid is valid
  solver_backtracking.py   Solver 1
  solver_csp.py            Solver 2
  solver_x.py              Solver 3
puzzles/
  bank.py           Puzzles by difficulty tier (easy/medium/hard/expert/17-clue)
  puzzle_bank/
    easy.txt
    medium.txt
    hard.txt
    expert.txt
    17.txt
tests/
  test_solvers.py   Pytest unit tests
benchmarks/
  run_benchmark.py  Run all solvers on the puzzle bank, print a table
```

## Current results

CSP solver is currently between ~100x and ~22,000x faster than plain backtracking
depending on difficulty, and solves expert / 17-clue puzzles that plain backtracking
times out on. Numbers in the progress report.

Algorithm X solver is slightly slower than CSP for easy to medium problems but highly 
outperforms on hard to expert problems.