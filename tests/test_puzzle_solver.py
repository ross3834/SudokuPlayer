from sudoku import Puzzle, PuzzleSolver
from tests.test_utils import generate_valid_incomplete_puzzle


def test_initialize_puzzle_solver():
    ps = PuzzleSolver(Puzzle(generate_valid_incomplete_puzzle()))

    assert isinstance(ps, PuzzleSolver)
