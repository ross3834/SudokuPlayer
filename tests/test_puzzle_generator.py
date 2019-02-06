from sudoku import PuzzleGenerator


def test_initialize_puzzle_generator():
    pg = PuzzleGenerator()

    assert isinstance(pg, PuzzleGenerator)

