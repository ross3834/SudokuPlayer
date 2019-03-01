from unittest.mock import MagicMock, Mock, patch

import pytest

from sudoku import Puzzle
from sudoku.pattern import Pattern


def test_width_correctly_set_on_initialization():
    pattern_list = [[0, 0, 0], [0, 0, 0, 0]]

    p = Pattern(pattern=pattern_list, resolution=pattern_list)

    assert p.width == 4


def test_height_correctly_set_on_initialization():
    pattern_list = [[0, 0, 0], [0, 0, 0], [0, 0, 0]]

    p = Pattern(pattern=pattern_list, resolution=pattern_list)

    assert p.height == 3


@patch("sudoku.pattern.Pattern.apply_to_candidate_dict")
@patch("sudoku.pattern.Pattern.apply_to_puzzle")
def test_apply_to_calls_correct_apply_method(apply_to_puzzle, apply_to_candidate_dict):
    pattern_list = [[0, 0]]

    p = Pattern(
        pattern=pattern_list, resolution=pattern_list, candidate_reduction=False
    )

    p.apply_to(Mock(), Mock())

    assert apply_to_puzzle.called
    assert not apply_to_candidate_dict.called

    p = Pattern(pattern_list, pattern_list, True)

    p.apply_to(Mock(), Mock())

    assert apply_to_candidate_dict.called


def test_apply_to_puzzle_returns_correct_response():
    puzzle_list = [
        [5, 5, 5, 1, 2, 3, 4, 5, 6],
        [5, 0, 5, 1, 2, 3, 4, 5, 6],
        [5, 5, 5, 1, 2, 3, 4, 5, 6],
        [1, 2, 3, 4, 5, 6, 7, 8, 9],
        [1, 2, 3, 4, 5, 6, 7, 8, 9],
        [1, 2, 3, 4, 5, 6, 7, 8, 9],
        [1, 2, 3, 4, 5, 6, 7, 8, 9],
        [1, 2, 3, 4, 5, 6, 7, 8, 9],
        [1, 2, 3, 4, 5, 6, 7, 8, 9],
    ]

    matching = Pattern.MATCHING
    unspecified = Pattern.UNSPECIFIED

    # Pattern that will match to the puzzle.
    pattern_list = [
        [matching, matching, matching],
        [matching, unspecified, matching],
        [matching, matching, matching],
    ]

    resolution = [[False, False, False], [False, True, False], [False, False, False]]

    puzzle = Puzzle(puzzle=puzzle_list, validate=False)
    pattern = Pattern(
        pattern=pattern_list, resolution=resolution, candidate_reduction=False
    )

    response = pattern.apply_to_puzzle(puzzle)

    responses = response.get_responses()

    assert len(responses) == 1
    assert responses[0] == ((1, 1), 5, False)


def test_apply_to_candidate_dict_returns_correct_response():

    candidate_dict = {(x, y): [x] for x in range(9) for y in range(9)}
    candidate_dict.update(
        {
            (0, 0): [5, 2],
            (0, 1): [5, 3],
            (0, 2): [5, 2],
            (1, 0): [5, 3],
            (1, 1): [1, 2, 3, 4, 6, 7, 8, 9],
            (1, 2): [5, 2],
            (2, 0): [5, 1],
            (2, 1): [5, 2],
            (2, 2): [5, 1],
        }
    )

    matching = Pattern.MATCHING
    unspecified = Pattern.UNSPECIFIED

    pattern_list = [
        [matching, matching, matching],
        [matching, unspecified, matching],
        [matching, matching, matching],
    ]

    resolution = [[False, False, False], [False, True, False], [False, False, False]]

    pattern = Pattern(
        pattern=pattern_list, resolution=resolution, candidate_reduction=True
    )

    response = pattern.apply_to_candidate_dict(candidate_dict)
    responses = response.get_responses()

    assert len(responses) == 1
    assert responses[0] == ((1, 1), 5, True)


@pytest.mark.parametrize(
    "chunk, pattern, match",
    [
        (
            [[1, 1, 1]],
            [[Pattern.MATCHING, Pattern.MATCHING, Pattern.NON_MATCHING]],
            False,
        ),
        ([[1, 1, 1]], [[Pattern.MATCHING, Pattern.MATCHING, Pattern.MATCHING]], True),
        (
            [[1, 1, 1]],
            [[Pattern.MATCHING, Pattern.MATCHING, Pattern.UNSPECIFIED]],
            True,
        ),
        ([[1, 1, 1]], [[Pattern.MATCHING, Pattern.MATCHING, Pattern.FILLED]], True),
        ([[1, 1, 1]], [[Pattern.MATCHING, Pattern.MATCHING, Pattern.UNFILLED]], False),
        (
            [[1, 1, [1, 2, 3]]],
            [[Pattern.MATCHING, Pattern.MATCHING, Pattern.NON_MATCHING]],
            False,
        ),
        (
            [[1, 1, [1, 2, 3]]],
            [[Pattern.MATCHING, Pattern.MATCHING, Pattern.MATCHING]],
            True,
        ),
        (
            [[1, 1, [1, 2, 3]]],
            [[Pattern.MATCHING, Pattern.MATCHING, Pattern.UNSPECIFIED]],
            True,
        ),
        (
            [[1, 1, [1, 2, 3]]],
            [[Pattern.MATCHING, Pattern.MATCHING, Pattern.FILLED]],
            False,
        ),
        (
            [[1, 1, [1, 2, 3]]],
            [[Pattern.MATCHING, Pattern.MATCHING, Pattern.UNFILLED]],
            True,
        ),
    ],
)
def test_does_match_correctly_matches_patterns(chunk, pattern, match):
    pattern = Pattern(pattern=pattern, resolution=[])

    assert match == pattern._does_match(chunk, 1)
