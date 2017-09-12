from sys import argv
from csv import reader


class InvalidPuzzleError(Exception):
	def __init__(self, message:str):
		self.message = message


class IndeterminantPuzzleError(Exception):
	def __init__(self, message:str):
		self.message = message


def load_puzzle(filename:str) -> list:
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

def set_cell(x: int, y: int, new_val , puzzle: list):
	puzzle[x][y] = new_val
	print("Row " + str(x + 1) + ", Col " + str(y + 1) + " has been set to: " + str(new_val))

def get_row(row: int, puzzle: list):
	return puzzle[row]

def get_col(col: int, puzzle: list):
	return [row[col] for row in puzzle]

def get_box(box_x: int, box_y: int, puzzle: list): #: Indexing starts at 0!!
	x_init = 3 * box_x
	y_init = 3 * box_y
	x_bound = x_init + 3
	y_bound = y_init + 3

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


def Solver(filename: str):
	if filename[-4:] != ".csv":
		filename += ".csv"
	puzzle = load_puzzle(filename)
	print("Puzzle loaded from " + filename + " is: ")
	print_puzzle(puzzle)

	blanks = []
	for row_index, row in enumerate(puzzle):
		for column_index, value in enumerate(row):
			if value == 0:
				blanks.append([row_index, column_index])

	#: Main loop to solve puzzle:
	pass_number = 1
	while len(blanks) != 0:
		print("Pass number: " + str(pass_number))

		#: Find possible solutions.
		pencil = [[[0] for i in range(9)] for i in range(9)]
		for blank_index, blank in enumerate(blanks):
			row = get_row(blank[0], puzzle)
			col = get_col(blank[1], puzzle)
			box = get_box(blank[0] // 3, blank[1] // 3, puzzle)  #: 0, 2 => 0, 0/ 5, 5 => 1, 1

			for i in range(1,10):
				if i not in row and i not in col and i not in box:
					if pencil[blank[0]][blank[1]] == [0]:
						pencil[blank[0]][blank[1]] = []
					pencil[blank[0]][blank[1]].append(i)

		#: Remove Candidates from pencil using Block and column/Row Interactions


		#: Find cells with only one posibility
		for prow_index, pencilled_row in enumerate(pencil):
			for index, possibilities in enumerate(pencilled_row):
				if len(possibilities) == 1 and possibilities[0] != 0:
					set_cell(prow_index, index,possibilities[0], puzzle)
					print_puzzle(puzzle)

		#: Find rows with only one possiblity
		for prow_index, prow in enumerate(pencil):
			for i in range(1,10):
				count = 0
				col_index = 0
				for index, possibilities in enumerate(prow):
					if i in possibilities:
						count += 1
						col_index = index
				if count == 1:
					set_cell(prow_index, col_index, i, puzzle)
					print_puzzle(puzzle)

		#: Find cols with only one possibility
		for col in range(9):
			for i in range(1, 10):
				count = 0
				row_index = 0
				for index, possibilities in enumerate(get_col(col, pencil)):
					if i in possibilities:
						count += 1
						row_index = index

				if count == 1:
					set_cell(row_index, col, i, puzzle)
					print_puzzle(puzzle)

		#: Find boxes with only one possibility
		for i in range(1, 10):
			for box_row in range(3):
				for box_col in range(3):
					count = 0
					locn_box = [0, 0]
					for index, possibilities in enumerate(get_box(box_row, box_col, pencil)):
						if i in possibilities:
							count += 1
							locn_box[0] = (index // 3) + (3 * box_row)
							locn_box[1] = (index % 3) + (3 * box_col)
					if count == 1:
						set_cell(locn_box[0], locn_box[1], i, puzzle)
						print("Found by Box")
						print_puzzle(puzzle)

		#: Remove values that have been found this pass
		mark = []
		for blank in blanks:
			if get_cell(blank[0], blank[1], puzzle) != 0:
				mark.append(blank)

		if len(mark) != 0:
			for blank in mark:
				blanks.remove(blank)
		else:
			print("pencil: ")
			for item in pencil:
				print(str(item) + '\t')

			#print("blanks: ")
			#for item in blanks:
			#	print(item)

			msg = "This puzzle cannot be determined any further as ALL blank spaces now have more than 2 open options."
			raise IndeterminantPuzzleError(msg)

		pass_number += 1
	print("The puzzle has been sucessfully solved after " + str(pass_number - 1) + " passes.")

if __name__ == "__main__":
	Solver(argv[1])
