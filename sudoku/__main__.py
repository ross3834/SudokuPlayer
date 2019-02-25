import logging

from sudoku import Puzzle, PuzzleGenerator, PuzzleSolver
from tests.test_utils import generate_valid_incomplete_puzzle

if __name__ == "__main__":
    logging_format = "logging.%(levelname)s:\n%(message)s"
    logging.basicConfig(format=logging_format)
    logging.getLogger().setLevel(logging.INFO)

    p = Puzzle(generate_valid_incomplete_puzzle())

    ps = PuzzleSolver(p)
    pg = PuzzleGenerator()

    ps.solve_puzzle(verbose=True)
