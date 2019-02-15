""" This test file will run the solver through multiple puzzles
    with different tricks to ensure that the solver can solve
    puzzles with those tricks.

    the name of each of these tests is read:
        "test_trivial_puzzle" -> test_puzzle_solver_can_solve_trivial_puzzle

    Because of the nature of solving puzzles, it is possible that these
    tests may take a while to run, thus they will all be marked with
    pytest.mark.slow.
"""

from unittest.mock import patch

import pytest

from sudoku import Puzzle, PuzzleSolver
from tests.test_utils import (
    generate_invalid_incomplete_puzzle_with_doubled_box,
    generate_invalid_incomplete_puzzle_with_doubled_column,
    generate_invalid_incomplete_puzzle_with_doubled_row,
    generate_valid_incomplete_puzzle,
)


@pytest.mark.slow
def test_trivial_puzzle():
    ps = PuzzleSolver(Puzzle(generate_valid_incomplete_puzzle()))

    ps.solve_puzzle()

    assert ps._is_puzzle_solved()


@patch("sudoku.puzzle_solver.logging")
def test_solving_with_verbose_true_prints(logging_mock):
    ps = PuzzleSolver(Puzzle(generate_valid_incomplete_puzzle()))

    ps.solve_puzzle(True)

    assert logging_mock.info.called


@pytest.mark.parametrize(
    "puzzle_list",
    [
        generate_invalid_incomplete_puzzle_with_doubled_row(),
        generate_invalid_incomplete_puzzle_with_doubled_column(),
        generate_invalid_incomplete_puzzle_with_doubled_box(),
    ],
)
def test_unsolvable_puzzle_raises_value_error(puzzle_list):

    ps = PuzzleSolver(Puzzle(puzzle_list, validate=False))

    with pytest.raises(PuzzleSolver.UnsolvablePuzzleException):
        ps.solve_puzzle()
