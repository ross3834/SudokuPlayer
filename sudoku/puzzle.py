class Puzzle:
    def __init__(self, puzzle: list, validate=True):
        """ Create an object that represents a Sudoku puzzle.

            Args:
                puzzle(list): A 2D list representing a puzzle. Note, a 0 is considered
                              an empty cell.
                validate(bool): Whether or the initialization should validate whether the
                                puzzle is valid or not.
                """

        self.validate = validate
        self._puzzle = puzzle

        if validate:
            self.check_valid()

    def get_column(self, col_index: int):
        """ Get the column of the puzzle at the passed index."""

        if self.validate and not 0 <= col_index <= 8:
            raise ValueError(
                f"Column index: {col_index} is not a valid column index. Must be between 0 and 8."
            )

        column = [row[col_index] for row in self._puzzle]

        return column

    def get_row(self, row_index: int):
        """ Get the row of the puzzle at the passed index."""

        if self.validate and not 0 <= row_index <= 8:
            raise ValueError(
                f"Row index: {row_index} is not a valid row index. Must be between 0 and 8."
            )

        row = self._puzzle[row_index]

        return row

    def get_box(self, box_position: tuple, flatten=False):
        """ Get a list representing the contents of the box at the passed position tuple.
            This can be from (0, 0) to (2, 2)."""

        if self.validate and not (
            0 <= box_position[0] <= 2 and 0 <= box_position[1] <= 2
        ):
            raise ValueError(
                f"box position: {box_position} is not a valid box position. Must be between"
                f" (0,0) and (2,2)"
            )
        box_x = box_position[0] * 3
        box_y = box_position[1] * 3

        if flatten:
            box = (
                self._puzzle[box_y][box_x : box_x + 3]
                + self._puzzle[box_y + 1][box_x : box_x + 3]
                + self._puzzle[box_y + 2][box_x : box_x + 3]
            )
        else:
            box = [
                self._puzzle[box_y][box_x : box_x + 3],
                self._puzzle[box_y + 1][box_x : box_x + 3],
                self._puzzle[box_y + 2][box_x : box_x + 3],
            ]

        return box

    def get_cell(self, cell_position: tuple):
        """ Get the value of the cell back from the passed position"""
        if self.validate and not (
            0 <= cell_position[0] <= 8 and 0 <= cell_position[1] <= 8
        ):
            raise ValueError(
                f"box position: {cell_position} is not a valid box position. Must be between"
                f" (0,0) and (8,8)"
            )

        return self._puzzle[cell_position[1]][cell_position[0]]

    def get_cell_from_box(self, box_position: tuple, cell_position: tuple):
        """ Returns the absolute position of a cell given its relative position
            in the passed box."""

        if self.validate and not (
            0 <= cell_position[0] <= 2 and 0 <= cell_position[1] <= 2
        ):
            raise ValueError(
                f"cell position: {cell_position} is not a valid cell position from within a box. Must be between"
                f" (0, 0) and (2, 2) for the relative position in the box."
            )

        box = self.get_box(box_position)
        return box[cell_position[1]][cell_position[0]]

    def get_box_from_cell(self, cell_position: tuple, flatten=False):
        """ Returns the box that the cell is in.
        """

        if self.validate and not (
            0 <= cell_position[0] <= 8 and 0 <= cell_position[1] <= 8
        ):
            raise ValueError(
                f"cell position: {cell_position} is not a valid cell position. Must be between"
                f" (0, 0) and (8, 8)"
            )

        box_x = cell_position[0] // 3
        box_y = cell_position[1] // 3

        return self.get_box((box_x, box_y), flatten=flatten)

    def get_chunk(self, initial_position, final_position):

        if self.validate and (
            not 0 <= initial_position[0] <= final_position[0] < 9
            or not 0 <= initial_position[1] <= final_position[1] < 9
        ):
            raise ValueError(
                f"Chunk position: {initial_position} "
                f"-> {final_position} is invalid.\n"
                f"Final must be greater or equal to intial.\n"
                f"All values must be within 0 to 8."
            )

        chunk = []
        for cell_y in range(initial_position[1], final_position[1] + 1):
            inner_chunk = []
            for cell_x in range(initial_position[0], final_position[0] + 1):
                inner_chunk.append(self.get_cell((cell_x, cell_y)))

            chunk.append(inner_chunk)

        return chunk

    def is_equal(self, puzzle):
        """ Don't implement __eq__ as we don't want to implement __hash__.
            For more information see: https://docs.python.org/3.6/reference/datamodel.html#object.__hash__
        """
        if puzzle is None:
            return False

        return puzzle._puzzle == self._puzzle

    def __str__(self):
        """
        Returns a string representing the puzzle.
        Ie, a returned string may look like:
            | 1  2  3 | 4  5  6 | 7  8  9
            | 4  5  6 | 7  8  9 | 1     3
            | 7  8  9 | 1  2  3 | 4  5  6
            -----------------------------
            | 2  3  1 | 5  6  4 | 8  9  7
            | 5     4 | 8  9  7 | 2  3  1
            | 8  9  7 | 2  3  1 | 5  6  4
            -----------------------------
            | 3  1  2 | 6  4  5 | 9  7  8
            | 6  4  5 | 9  7  8 | 3  1  2
            | 9  7  8 | 3  1  2 | 6  4  5
        """

        puzzle_string = ""

        for cell_y in range(9):
            puzzle_string += "|"
            for cell_x in range(9):
                cell_value = self.get_cell((cell_x, cell_y))

                if cell_value == 0:
                    puzzle_string += "   "
                else:
                    puzzle_string += f" {cell_value} "

                if cell_x == 2 or cell_x == 5:
                    puzzle_string += "|"
            if cell_y == 2 or cell_y == 5:
                puzzle_string += "\n-----------------------------\n"
            else:
                puzzle_string += "\n"

        return puzzle_string

    def check_valid(self, raise_exception=True):
        """ Checks that both the puzzle object is of the valid form, and that the puzzle does
            not appear to break any rules (2 numbers in the same row, column, or box"""

        def contains_duplicate(l: list):

            l = [item for item in l if item != 0]
            length = len(l)

            if len(set(l)) == length:
                return False
            else:
                return True

        error_messages = []

        try:
            if len(self._puzzle) != 9:
                error_messages.append(
                    "A sudoku puzzle must be 9x9. This puzzle does not have 9 rows."
                )

            if not all([len(row) == 9 for row in self._puzzle]):
                error_messages.append(
                    "A suduko puzzle must be 9x9. This puzzle has at least"
                    "one row not of length 9."
                )

            if not all([0 <= cell <= 9 for row in self._puzzle for cell in row]):
                error_messages.append(
                    "A suduko puzzle can only have values 0 to 9. 0 represents"
                    "an unknown, and the rest represent their actual numbers."
                )

            if any([contains_duplicate(row) for row in self._puzzle]):
                error_messages.append("A duplicate value was found in one of the rows")

            if any([contains_duplicate(self.get_column(i)) for i in range(9)]):
                error_messages.append(
                    "A duplicate value was found in one of the columns"
                )

            for box_x in range(3):
                for box_y in range(3):
                    if contains_duplicate(
                        [item for row in self.get_box((box_x, box_y)) for item in row]
                    ):
                        error_messages.append(
                            f"Duplicates found in box {(box_x, box_y)}."
                        )
        except:
            # Some of these tests assume that the previous check passed.
            # In other words, if a test fails, other specific tests may
            # throw IndexErrors because the puzzle is so invalid. In this case
            # report that the state of the puzzle caused some tests to be
            # un-runnable, and report the known errors.
            raise ValueError(
                f"Due to the state of the puzzle, some tests became un-runnable.\n"
                f"There were {len(error_messages)} errors found before an un-runnable"
                f" test was reached. They are: {error_messages}"
            )

        if error_messages and raise_exception:
            raise ValueError(
                f"{len(error_messages)} types of errors found in puzzle. "
                f"They are: {error_messages}"
            )
        elif error_messages and not raise_exception:
            return False

        return True

    def set_cell(self, cell_position: tuple, new_val: int, undo_move=False):
        """ Set the cell at the passed position."""

        if self.validate and not (
            0 <= cell_position[0] <= 8 and 0 <= cell_position[1] <= 8
        ):
            raise ValueError(
                f"cell position: {cell_position} is not a valid cell position. Must be between"
                f" (0, 0) and (8, 8)"
            )

        previous_value = self._puzzle[cell_position[1]][cell_position[0]]
        self._puzzle[cell_position[1]][cell_position[0]] = new_val

        if self.validate:
            is_valid = self.check_valid(raise_exception=(not undo_move))

            if undo_move and not is_valid:
                self._puzzle[cell_position[1]][cell_position[0]] = previous_value
