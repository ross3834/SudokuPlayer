from sudoku import Puzzle


class Pattern:

    UNSPECIFIED = 0
    MATCHING = 1
    NONMATCH = 2
    FILLED = 3
    UNFILLED = 4

    def __init__(self, pattern, candidate_reduction=False):
        """
        Args:
            pattern(list): A list of lists representing the
                           smallest possible grid the pattern
                           can fit in, with the pattern in it.
                           eg)
                                [[FILLED, UNSPECIFIED, MATCHING, NONMATCHING],
                                 [MATCHING, UNSPECIFIED, UNSPECIFIED, UNFILLED]]

                           Represents a 4x2 pattern where the values at
                           (0,2) and (1,0) match, (0,3) matches neither of
                           those positions. Further, position (0,0) must have
                           a value, and position (1,3) must NOT have a value. Finally
                           (0,1), (1,1), (1,2) can have any value.

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

    def apply_to(self, puzzle: Puzzle):
        """ Apply the pattern to the puzzle, finding
            all matches, and returning a PatternResponse
            object, to be used by the puzzle.
        """
        pass

    def _does_match(self, chunk):
        """ Takes a 'chunk' of the puzzle of the same dimensions of
            the pattern, and checks to see if the pattern matches
            the chunk."""

        pass
