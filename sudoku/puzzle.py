import logging


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

        if not 0 <= col_index <= 8:
            raise ValueError(
                f"Column index: {col_index} is not a valid column index. Must be between 0 and 8."
            )

        return [row[col_index] for row in self._puzzle]

    def get_row(self, row_index: int):
        """ Get the row of the puzzle at the passed index."""

        if not 0 <= row_index <= 8:
            raise ValueError(
                f"Row index: {row_index} is not a valid row index. Must be between 0 and 8."
            )

        return self._puzzle[row_index]

    def get_box(self, box_position: tuple):
        """ Get a list representing the contents of the box at the passed position tuple.
            This can be from (0, 0) to (2, 2)."""

        if not (0 <= box_position[0] <= 2 and 0 <= box_position[1] <= 2):
            raise ValueError(
                f"box position: {box_position} is not a valid box position. Must be between"
                f" (0,0) and (2,2)"
            )
        box_x = box_position[0] * 3
        box_y = box_position[1] * 3

        return [
            self._puzzle[box_y][box_x : box_x + 3],
            self._puzzle[box_y + 1][box_x : box_x + 3],
            self._puzzle[box_y + 2][box_x : box_x + 3],
        ]

    def get_cell(self, cell_position: tuple):
        """ Get the value of the cell back from the passed position"""
        if not (0 <= cell_position[0] <= 8 and 0 <= cell_position[1] <= 8):
            raise ValueError(
                f"box position: {cell_position} is not a valid box position. Must be between"
                f" (0,0) and (8,8)"
            )

        return self._puzzle[cell_position[1]][cell_position[0]]

    def get_cell_from_box(self, box_position: tuple, cell_position: tuple):
        """ Returns the absolute position of a cell given its relative position
            in the passed box."""
        if not (0 <= box_position[0] <= 2 and 0 <= box_position[1] <= 2):
            raise ValueError(
                f"box position: {box_position} is not a valid box position. Must be between"
                f" (0,0) and (2,2)"
            )

        if not (0 <= cell_position[0] <= 2 and 0 <= cell_position[1] <= 2):
            raise ValueError(
                f"cell position: {cell_position} is not a valid cell position. Must be between"
                f" (0, 0) and (2, 2)"
            )

        box = self.get_box(box_position)
        return box[cell_position[1]][cell_position[0]]

    def check_valid(self):
        """ Checks that both the puzzle object is of the valid form, and that the puzzle does
            not appear to break any rules (2 numbers in the same row, column, or box"""

        def contains_duplicate(l: list):
            print("--------------", l, "--------------", sep="\n")

            l = [item for item in l if item != 0]
            length = len(l)

            if len(set(l)) == length:
                return False
            else:
                return True

        if len(self._puzzle) != 9:
            raise ValueError(
                "A sudoku puzzle must be 9x9. This puzzle does not have" "9 rows."
            )

        if not all([len(row) == 9 for row in self._puzzle]):
            raise ValueError(
                "A suduko puzzle must be 9x9. This puzzle has at least"
                "one row not of length 9."
            )

        if not all([0 <= cell <= 9 for row in self._puzzle for cell in row]):
            raise ValueError(
                "A suduko puzzle can only have values 0 to 9. 0 represents"
                "an unknown, and the rest represent their actual numbers."
            )

        if any([contains_duplicate(row) for row in self._puzzle]):
            raise ValueError("A duplicate value was found in one of the rows")

        if any([contains_duplicate(self.get_column(i)) for i in range(9)]):
            raise ValueError("A duplicate value was found in one of the columns")

        for box_x in range(3):
            for box_y in range(3):
                if contains_duplicate(
                    [item for row in self.get_box((box_x, box_y)) for item in row]
                ):
                    raise ValueError(f"Duplicates found in box {(box_x, box_y)}.")

    def set_cell(self, cell_position: tuple, new_val: int):
        """ Set the cell at the passed position."""

        if not (0 <= cell_position[0] <= 8 and 0 <= cell_position[1] <= 8):
            raise ValueError(
                f"cell position: {cell_position} is not a valid cell position. Must be between"
                f" (0, 0) and (8, 8)"
            )

        self._puzzle[cell_position[1]][cell_position[0]] = new_val

        if self.validate:
            self.check_valid()
