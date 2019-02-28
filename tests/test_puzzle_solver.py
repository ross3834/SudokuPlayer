from unittest.mock import MagicMock, Mock, patch

from sudoku import Puzzle, PuzzleSolver
from tests.test_utils import (
    generate_valid_complete_puzzle,
    generate_valid_incomplete_puzzle,
)


def test_initialize_puzzle_solver():
    ps = PuzzleSolver(Puzzle(generate_valid_incomplete_puzzle()))

    assert isinstance(ps, PuzzleSolver)


@patch("sudoku.puzzle.Puzzle.set_cell")
def test_fill_trivial_cells_finds_and_fills_correct_cells(set_cell_mock):

    ps = PuzzleSolver(Puzzle(generate_valid_complete_puzzle()))
    ps._missing_values = {(0, 0): [1]}

    ps._fill_trivial_cells()
    assert ps._missing_values[(0, 0)] == []
    set_cell_mock.assert_called_once_with(cell_position=(0, 0), new_val=1)


def test_apply_patterns_applies_all_patterns():

    ps = PuzzleSolver(Puzzle(generate_valid_complete_puzzle()))

    pattern_mock = MagicMock()
    ps.register_pattern(pattern_mock)

    ps._apply_patterns()

    assert pattern_mock.apply_to.called


def test_is_puzzle_solved_returns_true_for_solved_puzzles():

    ps = PuzzleSolver(Puzzle(generate_valid_complete_puzzle()))

    assert ps._is_puzzle_solved()


def test_is_puzzle_solved_returns_false_for_unsolved_puzzles():

    ps = PuzzleSolver(Puzzle(generate_valid_incomplete_puzzle()))

    assert not ps._is_puzzle_solved()


def test_register_pattern_adds_the_pattern_to_the_list():

    ps = PuzzleSolver(Puzzle(generate_valid_complete_puzzle()))
    pattern = Mock()

    ps.register_pattern(pattern)

    assert pattern in ps._patterns
