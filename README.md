# cs175-sp26-sudoku

Comparative study of classical algorithms for solving sudoku.
CS 175, Spring 2026, Prof. Kask.

**Team:** Mathieu Khalaf (mathieuk), Tyler Kuwada (tkuwada).

## Solvers

- **Solver 1: Plain Backtracking** (baseline) — `sudoku/solver_backtracking.py` (done)
- **Solver 2: Backtracking + AC-3 + MRV/LCV** — `sudoku/solver_csp.py` (done)
- **Solver 3: Dancing Links / Algorithm X** — TODO
- **Stretch: Preemptive sets (Crook)** — TODO
- **Stretch: Simulated annealing (Chi & Lange)** — TODO

## How to run

### Locally (Python 3.11+)

```bash
pip install -r requirements.txt
pytest tests/ -v          # run tests
python benchmarks/run_benchmark.py   # run benchmarks
```

### With Docker

```bash
docker build -t sudoku .
docker run -it -v ${PWD}:/workspace sudoku
# then inside the container:
pytest tests/ -v
python benchmarks/run_benchmark.py
```

## Layout

```
sudoku/             Solver code
  io.py             Parse/print puzzles
  verify.py         Check whether a solved grid is valid
  solver_backtracking.py   Solver 1
  solver_csp.py            Solver 2
puzzles/
  bank.py           Puzzles by difficulty tier (easy/medium/hard/expert/17-clue)
tests/
  test_solvers.py   Pytest unit tests
benchmarks/
  run_benchmark.py  Run all solvers on the puzzle bank, print a table
```

## Current results

CSP solver is currently between ~100x and ~22,000x faster than plain backtracking
depending on difficulty, and solves expert / 17-clue puzzles that plain backtracking
times out on. Numbers in the progress report.
