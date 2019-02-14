from sudoku import Puzzle, PuzzleGenerator, PuzzleSolver
from tests.test_utils import generate_valid_incomplete_puzzle

if __name__ == "__main__":

    p = Puzzle(generate_valid_incomplete_puzzle())

    ps = PuzzleSolver(p)
    pg = PuzzleGenerator()

    ps.solve_puzzle(verbose=True)
