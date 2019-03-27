from unittest.mock import MagicMock, Mock, patch

from sudoku.pattern import PatternResponse


def test_pattern_response_returns_all_responses():

    pr = PatternResponse()
    responses = (((0, 0), 5, True), ((1, 1), 5, False), ((6, 6), 5, True))

    pr.add_response(*responses[0])
    pr.add_response(*responses[1])
    pr.add_response(*responses[2])

    assert all([response in responses for response in pr.get_responses()])
