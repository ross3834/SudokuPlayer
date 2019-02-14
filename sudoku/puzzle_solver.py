class PuzzleSolver:
    def __init__(self, puzzle):

        self._puzzle = puzzle
        self._missing_values = {}
        self._patterns = []

        self._find_missing_values()

    def _find_missing_values(self):
        """ Generate and return a dictionary of all the possibilities
            for each cell without a value (ie a 0 value.)
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
            pass

    def _is_puzzle_solved(self):
        for possibilities in self._missing_values.values():
            if len(possibilities) != 0:
                return False

        return True

    def register_pattern(self, pattern):
        self._patterns.append(pattern)

    def solve_puzzle(self, verbose=False):

        past_puzzle = None

        while not self._is_puzzle_solved():

            if verbose:
                print(self._puzzle)

            self._find_missing_values()
            self._fill_trivial_cells()
            self._apply_patterns()

            if past_puzzle == self._puzzle:
                print("Puzzle can't be solved currently")
                break
            else:
                past_puzzle = self._puzzle

        if verbose:
            print(self._puzzle)
