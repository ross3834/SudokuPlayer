import logging


class PuzzleSolver:
    def __init__(self, puzzle):

        self._puzzle = puzzle
        self._missing_values = {}
        self._patterns = []

        self._find_missing_values()

    def _find_missing_values(self):
        """ Generate a dictionary of all the possibilities
            for each cell without a value (ie a 0 value.) and
            set _missing_values to it.
        """
        missing_values = {}
        for cell_x in range(9):
            for cell_y in range(9):

                if self._puzzle.get_cell((cell_x, cell_y)) != 0:
                    missing_values[(cell_x, cell_y)] = []
                else:
                    missing = {_ for _ in range(1, 10)}

                    missing -= set(self._puzzle.get_column(cell_x))
                    missing -= set(self._puzzle.get_row(cell_y))
                    missing -= set(
                        self._puzzle.get_box_from_cell((cell_x, cell_y), flatten=True)
                    )

                    missing_values[(cell_x, cell_y)] = list(missing)

        self._missing_values = missing_values

    def _fill_trivial_cells(self):
        """ For any entry in the puzzle that has only one possibility
            fill that value in with that one possibility, and return the puzzle.
        """

        for position, possibilities in self._missing_values.items():
            if len(possibilities) == 1:
                self._puzzle.set_cell(cell_position=position, new_val=possibilities[0])

                self._missing_values[position] = []

    def _apply_patterns(self):
        for pattern in self._patterns:
            pattern.apply_to(self._puzzle, self._missing_values)

    def _is_puzzle_solved(self):
        for position, possibilities in self._missing_values.items():
            if len(possibilities) != 0 or self._puzzle.get_cell(position) == 0:
                return False

        return self._puzzle.check_valid(raise_exception=False)

    def register_pattern(self, pattern):
        self._patterns.append(pattern)

    def solve_puzzle(self, verbose=False):

        past_puzzle = None
        past_possibilities = None

        while not self._is_puzzle_solved():

            if verbose:
                logging.info(str(self._puzzle))

            self._find_missing_values()
            self._fill_trivial_cells()
            self._apply_patterns()

            if (
                past_puzzle == self._puzzle
                and past_possibilities == self._missing_values
            ) or not self._puzzle.check_valid(raise_exception=False):
                raise self.UnsolvablePuzzleException(
                    "Puzzle passed to the solver is either unsolvable or cannot be"
                    "solved using the methods this solver knows."
                )
            else:
                past_puzzle = self._puzzle
                past_possibilities = self._missing_values

        if verbose:
            logging.info(str(self._puzzle))

    class UnsolvablePuzzleException(ValueError):
        pass
