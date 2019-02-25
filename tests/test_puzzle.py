import pytest

from sudoku import Puzzle

from .test_utils import (
    generate_invalid_incomplete_puzzle_with_doubled_box,
    generate_invalid_incomplete_puzzle_with_doubled_column,
    generate_invalid_incomplete_puzzle_with_doubled_row,
    generate_valid_complete_puzzle,
    generate_valid_incomplete_puzzle,
)


@pytest.mark.parametrize(
    "puzzle_list",
    (
        [],
        [[]],
        [[[]]],
        [[], [], [], [], [], [], [], [], []],
        generate_invalid_incomplete_puzzle_with_doubled_column(),
        generate_invalid_incomplete_puzzle_with_doubled_row(),
        generate_invalid_incomplete_puzzle_with_doubled_box(),
    ),
)
def test_invalid_puzzle_raises_value_error(puzzle_list):

    with pytest.raises(ValueError):
        Puzzle(puzzle_list, validate=True)


@pytest.mark.parametrize(
    "puzzle_list",
    (
        generate_invalid_incomplete_puzzle_with_doubled_column(),
        generate_invalid_incomplete_puzzle_with_doubled_row(),
        generate_invalid_incomplete_puzzle_with_doubled_box(),
    ),
)
def test_check_valid_returns_false_for_invalid_puzzle(puzzle_list):
    puzzle = Puzzle(puzzle_list, validate=False)

    assert not puzzle.check_valid(raise_exception=False)


@pytest.mark.parametrize(
    "puzzle_list", ([], [[]], [[[]]], [[], [], [], [], [], [], [], [], []])
)
def test_check_valid_raises_value_error_if_all_tests_cannot_be_run(puzzle_list):
    puzzle = Puzzle(puzzle_list, validate=False)

    with pytest.raises(ValueError):
        puzzle.check_valid(raise_exception=False)


@pytest.mark.parametrize("col_num", (-1, 9))
def test_getting_invalid_column_number_raises_value_error(col_num):

    puzzle = Puzzle(generate_valid_complete_puzzle())

    with pytest.raises(ValueError):
        puzzle.get_column(col_num)


@pytest.mark.parametrize("row_num", (-1, 9))
def test_getting_invalid_row_number_raises_value_error(row_num):
    puzzle = Puzzle(generate_valid_complete_puzzle())

    with pytest.raises(ValueError):
        puzzle.get_row(row_num)


@pytest.mark.parametrize("invalid_pos", ((-1, -1), (-1, 3), (3, 3), (3, -1)))
def test_getting_invalid_box_position_raises_value_error(invalid_pos):
    puzzle = Puzzle(generate_valid_complete_puzzle())

    with pytest.raises(ValueError):
        puzzle.get_box(invalid_pos)


@pytest.mark.parametrize("invalid_pos", ((-1, -1), (-1, 9), (9, 9), (9, -1)))
def test_getting_invalid_cell_position_raises_value_error(invalid_pos):
    puzzle = Puzzle(generate_valid_complete_puzzle())

    with pytest.raises(ValueError):
        puzzle.get_cell(invalid_pos)


@pytest.mark.parametrize("invalid_pos", ((-1, -1), (-1, 9), (9, 9), (9, -1)))
def test_getting_box_of_invalid_cell_position_raises_value_error(invalid_pos):
    puzzle = Puzzle(generate_valid_complete_puzzle())

    with pytest.raises(ValueError):
        puzzle.get_box_from_cell(invalid_pos)


@pytest.mark.parametrize("invalid_pos", ((-1, -1), (-1, 9), (9, 9), (9, -1)))
def test_setting_invalid_cell_position_raises_value_error(invalid_pos):
    puzzle = Puzzle(generate_valid_complete_puzzle())

    with pytest.raises(ValueError):
        puzzle.set_cell(invalid_pos, 0)


@pytest.mark.parametrize("invalid_pos", ((-1, -1), (-1, 3), (3, 3), (3, -1)))
def test_getting_invalid_cell_from_box_raises_value_error(invalid_pos):
    puzzle = Puzzle(generate_valid_complete_puzzle())

    with pytest.raises(ValueError):
        puzzle.get_cell_from_box(invalid_pos, (0, 0))


@pytest.mark.parametrize("invalid_pos", ((-1, -1), (-1, 3), (3, 3), (3, -1)))
def test_getting_invalid_box_from_puzzle_when_getting_cell_raises_value_error(
    invalid_pos
):
    puzzle = Puzzle(generate_valid_complete_puzzle())

    with pytest.raises(ValueError):
        puzzle.get_cell_from_box((0, 0), invalid_pos)


@pytest.mark.parametrize(
    "initial_position, final_position",
    [((-1, -1), (2, 2)), ((2, 2), (9, 9)), ((5, 5), (2, 2))],
)
def test_getting_invalid_chunk_from_puzzle_raises_valid_error(
    initial_position, final_position
):
    puzzle = Puzzle(generate_valid_complete_puzzle())

    with pytest.raises(ValueError):
        puzzle.get_chunk(initial_position, final_position)


def test_getting_box_returns_correct_box():
    puzzle = Puzzle(generate_valid_complete_puzzle())

    box = puzzle.get_box((0, 0))

    assert box == [[1, 2, 3], [4, 5, 6], [7, 8, 9]]


def test_getting_column_returns_correct_column():
    puzzle = Puzzle(generate_valid_complete_puzzle())

    col = puzzle.get_column(0)

    assert col == [1, 4, 7, 2, 5, 8, 3, 6, 9]


def test_getting_row_returns_correct_row():
    puzzle = Puzzle(generate_valid_complete_puzzle())

    row = puzzle.get_row(0)

    assert row == [1, 2, 3, 4, 5, 6, 7, 8, 9]


def test_get_cell_from_box_returns_correct_cell():
    puzzle = Puzzle(generate_valid_complete_puzzle())

    cell = puzzle.get_cell_from_box((0, 0), (0, 0))

    assert cell == 1


def test_get_box_from_cell_returns_correct_box():
    puzzle = Puzzle(generate_valid_complete_puzzle())

    box = puzzle.get_box_from_cell((0, 0))

    assert box == puzzle.get_box((0, 0))


def test_get_cell_returns_correct_value():
    puzzle = Puzzle(generate_valid_complete_puzzle())

    cell = puzzle.get_cell((0, 0))

    assert cell == 1


def test_get_chunk_returns_the_correct_chunk():
    puzzle = Puzzle(generate_valid_complete_puzzle())

    chunk = puzzle.get_chunk((0, 0), (2, 2))

    assert chunk == puzzle.get_box((0, 0))


def test_set_cell_sets_cell():
    puzzle = Puzzle(generate_valid_incomplete_puzzle())

    puzzle.set_cell((0, 0), new_val=1)


# The generated puzzle has only one non invalid value, 1.
@pytest.mark.parametrize("invalid_val", (-1, 2, 3, 4, 5, 6, 7, 8, 9, 10))
def test_set_cell_setting_invalid_cell_raises_value_error_on_validate_puzzle(
    invalid_val
):
    validate_puzzle = Puzzle(generate_valid_incomplete_puzzle(), validate=True)

    with pytest.raises(ValueError):
        validate_puzzle.set_cell((0, 0), invalid_val)


# The generated puzzle has only one non invalid value, 1.
@pytest.mark.parametrize("invalid_val", (-1, 2, 3, 4, 5, 6, 7, 8, 9, 10))
def test_set_cell_setting_invalid_cell_undoes_move(invalid_val):
    valid_puzzle = generate_valid_complete_puzzle()

    puzzle = Puzzle(generate_valid_complete_puzzle(), validate=True)

    puzzle.set_cell((0, 0), invalid_val, undo_move=True)

    assert puzzle._puzzle == valid_puzzle


def test_str_returns_a_string():
    puzzle = Puzzle(generate_valid_incomplete_puzzle())

    assert isinstance(str(puzzle), str)


def test_is_equal_returns_true_for_equal_puzzles():
    puzzle1 = Puzzle(generate_valid_incomplete_puzzle())

    assert puzzle1.is_equal(puzzle1)


def test_is_equal_returns_false_for_unequal_puzzles():
    puzzle1 = Puzzle(generate_valid_incomplete_puzzle())
    puzzle2 = Puzzle(generate_valid_complete_puzzle())

    assert not puzzle1.is_equal(puzzle2)
