from collections import Iterable

from sudoku import Puzzle


class Pattern:

    # Constants for patterns
    UNSPECIFIED = 0
    MATCHING = 1
    NON_MATCHING = 2
    FILLED = 3
    UNFILLED = 4

    def __init__(self, pattern, resolution, candidate_reduction=False):
        """
        Args:
            pattern(list): A list of lists representing the
                           smallest possible grid the pattern
                           can fit in, with the pattern in it.
                           eg)
                                [[FILLED, UNSPECIFIED, MATCHING, NON_MATCHING],
                                 [MATCHING, UNSPECIFIED, UNSPECIFIED, UNFILLED]]

                           Represents a 4x2 pattern where the values at
                           (0,2) and (1,0) match, (0,3) matches neither of
                           those positions. Further, position (0,0) must have
                           a value, and position (1,3) must NOT have a value. Finally
                           (0,1), (1,1), (1,2) can have any value.

            resolution(list): A list of lists used to tell the pattern how it
                              should react to a match.

            candidate_reduction(bool): If True, then this pattern will
                                       alter the candidates, rather than
                                       the puzzle itself. If False, then
                                       this pattern applies to adding values
                                       directly into the puzzle.
        """

        self._pattern = pattern
        self.width = max([len(row) for row in pattern])
        self.height = len(pattern)
        self.candidate_reduction = candidate_reduction

    def apply_to(self, puzzle: Puzzle, candidates: dict):
        if self.candidate_reduction:
            self.apply_to_candidate_dict(candidates)
        else:
            self.apply_to_puzzle(puzzle)

    def apply_to_puzzle(self, puzzle: Puzzle):
        """ Apply the pattern to the puzzle, finding
            all matches, and returning a PatternResponse
            object to be used by the puzzle.
        """

        chunk_init_y = 0

        for chunk_y in range(self.height, 9):
            chunk_init_x = 0
            for chunk_x in range(self.width, 9):

                # Check if the pattern applies if all the "MATCHING" values
                # equal matching_with (ie, check each possible value, and
                # resolve on each match.
                for matching_with in range(1, 10):
                    chunk = puzzle.get_chunk(
                        (chunk_init_x, chunk_init_y), (chunk_x, chunk_y)
                    )

                    if self._does_match(chunk, matching_equals=matching_with):
                        pass  # somehow resolve this.

                chunk_init_x += 1
            chunk_init_y += 1

    def apply_to_candidate_dict(self, candidates: dict):
        """ Apply the pattern to the list of candidates,
            all matches, and returning a PatternResponse
            object to be used by the puzzle.
        """
        chunk_init_y = 0

        for chunk_final_y in range(self.height, 9):
            chunk_init_x = 0

            for chunk_final_x in range(self.width, 9):

                contained_positions = [
                    (x, y)
                    for x in range(chunk_init_x, chunk_final_x + 1)
                    for y in range(chunk_init_y, chunk_final_y + 1)
                ]
                chunk_flattened = [
                    candidates[position] for position in contained_positions
                ]

                # Break the flattened chunk into a 2D list based on the width of
                # the pattern.
                chunk = [
                    chunk_flattened[i : i + self.width]
                    for i in range(0, len(chunk_flattened), self.width)
                ]

                # Check if the pattern applies if all the "MATCHING" values
                # equal matching_with (ie, check each possible value, and
                # resolve on each match.
                for matching_with in range(1, 10):
                    if self._does_match(chunk, matching_with):
                        pass  # Somehow resolve this.

                chunk_init_x += 1
            chunk_init_y += 1

    def _does_match(self, chunk, matching_equals):
        """ Takes a 'chunk' of the puzzle of the same dimensions of
            the pattern, and checks to see if the pattern matches
            the chunk."""

        for y in range(0, self.height):
            for x in range(0, self.width):

                cell = chunk[y][x]
                if not isinstance(cell, Iterable):
                    cell = [cell]

                # Check to see if ANY of the cells don't match
                # the pattern. If any cell has any condition not
                # met, then return False.
                cell_filled = len(cell) == 1 and cell is not [0]
                cell_not_matching = matching_equals not in cell
                cell_matching = matching_equals in cell
                cell_not_filled = len(cell) != 0 or cell is [0]

                if self._pattern[y][x] is self.UNFILLED:
                    if cell_filled:
                        return False
                elif self._pattern[y][x] is self.MATCHING:
                    if cell_not_matching:
                        return False
                elif self._pattern[y][x] is self.NON_MATCHING:
                    if cell_matching:
                        return False
                elif self._pattern[y][x] is self.FILLED:
                    if cell_not_filled:
                        return False

        # If we have not returned False yet, then
        # the pattern should be an exact match, so
        # return True.
        return True


class PatternResponse:
    pass
