from sudoku import PuzzleSolver


def test_initialize_puzzle_solver():
    ps = PuzzleSolver()

    assert isinstance(ps, PuzzleSolver)
