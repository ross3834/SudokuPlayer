def generate_valid_complete_puzzle():
    return [
        [1, 2, 3, 4, 5, 6, 7, 8, 9],
        [4, 5, 6, 7, 8, 9, 1, 2, 3],
        [7, 8, 9, 1, 2, 3, 4, 5, 6],
        [2, 3, 1, 5, 6, 4, 8, 9, 7],
        [5, 6, 4, 8, 9, 7, 2, 3, 1],
        [8, 9, 7, 2, 3, 1, 5, 6, 4],
        [3, 1, 2, 6, 4, 5, 9, 7, 8],
        [6, 4, 5, 9, 7, 8, 3, 1, 2],
        [9, 7, 8, 3, 1, 2, 6, 4, 5],
    ]


def generate_valid_incomplete_puzzle():
    return [
        [0, 2, 3, 4, 5, 6, 7, 8, 9],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [7, 8, 0, 1, 2, 3, 4, 5, 6],
        [2, 3, 1, 0, 6, 4, 8, 9, 7],
        [5, 6, 4, 8, 0, 7, 2, 3, 1],
        [8, 9, 7, 2, 3, 0, 5, 6, 4],
        [3, 1, 2, 6, 4, 5, 0, 7, 8],
        [6, 4, 5, 9, 7, 8, 3, 0, 2],
        [9, 7, 8, 3, 1, 2, 6, 4, 0],
    ]


def generate_invalid_incomplete_puzzle_with_doubled_column():
    puzzle = generate_valid_incomplete_puzzle()

    # Create a columns with two of the same number, but valid
    # seeming boxes and rows.
    puzzle[1][1] = 2

    return puzzle


def generate_invalid_incomplete_puzzle_with_doubled_row():
    puzzle = generate_valid_incomplete_puzzle()

    # Create a row with two of the same number, but valid
    # seeming boxes and columns
    puzzle[0][0] = 4

    return puzzle


def generate_invalid_incomplete_puzzle_with_doubled_box():
    puzzle = generate_valid_incomplete_puzzle()

    # Create a box with two of the same number, but valid
    # seeming rows and columns.
    puzzle[1][3] = 5

    return puzzle
