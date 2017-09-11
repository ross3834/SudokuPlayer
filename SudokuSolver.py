from sys import argv
from csv import reader


class InvalidPuzzleError(Exception):
	def __init__(self, message:str):
		self.message = message


class IndeterminantPuzzleError(Exception):
	def __init__(self, message:str):
		self.message = message


def load_puzzle(filename:str):
	sudoku_puzzle = []
	if filename[-4:] != ".csv":
		filename += ".csv"
	try:
		with open(filename, 'rt') as sfile:
			puzzle = reader(sfile, delimiter=',')
			for row in puzzle:
				sudoku_puzzle.append([])
				for box in row:
					sudoku_puzzle[-1].append(int(box.strip()))
	except FileNotFoundError:
		print("\"" + filename + "\" Could not be found.")

	if len(sudoku_puzzle) != 9:
		msg = str(len(sudoku_puzzle)) + " Is an invalid number of rows." \
		      " A sudoku puzzle must have 9 rows."
		raise InvalidPuzzleError(msg)

	for index, row in enumerate(sudoku_puzzle):
		if len(row) != 9:
			msg = str(len(sudoku_puzzle)) + "Is an invalid number of" \
			      " boxes in a row. Row " + str(index) + " must have 9 boxes."
			raise InvalidPuzzleError(msg)

	for i in range(1, 10):
		box_row = 0
		for y in range(9):
			row = get_row(y, sudoku_puzzle)
			col = get_col(y, sudoku_puzzle)

			if y % 3 == 0 and y != 0:
				box_row += 1
			box_col = y - 3 * (box_row)
			box = get_box(box_row, box_col, sudoku_puzzle)

			if row.count(i) > 1:
				msg = str(i) + " appears more than once in row " + str(y + 1)
				raise InvalidPuzzleError(msg)
			elif col.count(i) > 1:
				msg = str(i) + " appears more than once in column " + str(y + 1)
				raise InvalidPuzzleError(msg)
			elif box.count(i) > 1:
				msg = str(i) + " appears more than once in box " + str(box_row + 1) + \
					", " + str(box_col + 1)

	return sudoku_puzzle

def get_cell(x: int, y: int, puzzle: list):
	return puzzle[x][y]

def get_row(row: int, puzzle: list):
	return puzzle[row]

def get_col(col: int, puzzle: list):
	return [row[col] for row in puzzle]

def get_box(box_x: int, box_y: int, puzzle: list):
	x_bound = 3 * box_x
	y_bound = 3 * box_y
	x_init = x_bound - 3
	y_init= y_bound - 3

	box  = []
	for x in range(x_init, x_bound):
		for y in range(y_init, y_bound):
			box.append(get_cell(x, y, puzzle))

	return box

def print_puzzle(puzzle: list):
	for count, row in enumerate(puzzle):
		if count != len(puzzle) - 1 and count % 3 == 0 and count != 0:
			print('\n=========================')
		else:
			pass
			print()

		for index, value in enumerate(row):
			if index % 3 == 0:
				print('| ', end='')

			if value != 0:
				print(value,end=' ')
			else:
				print(' ', end=' ')

		print('|', end='')
	print()
	print()



if __name__ == "__main__":
	puzzle = load_puzzle(argv[1])
	print_puzzle(puzzle)
