"""'

Author: Ross Alexandra
Most recent update: December 19th, 2017
Most recent changes:
		- Updated documentation to allow for future updates to be completed
		with less downtime when attempting to add addtional features.

		- Removed some code that was not used.

		- Added this header for more up-to-date information on the current
		standings of this file.

Note:
	This program is as of current incomplete and highly experimental. As such,
	much of this code is not in a form that does not reflect an ideal state (
	ie uncommented, unoptimized, etc.) As I have more time to work on this overall
	project I will make the code more readable as a first priority before attempting
	to add new features.
"""

from csv import reader #: Used to read puzzles loaded from text files.
import argparse #: Used for reading command line arguments

class InvalidPuzzleError(Exception):
	"""'
	An exception to be thrown incase of an invalid puzzle being passed to
	into the solver.

	In otherwords, this error will be thrown if a puzzle either
		1) Not matching the correct csv format or,
		2) A puzzle that has an incorrect setup (example an
		   incorrect number of rows or columns.

	This error will NOT be thrown if the puzzle cannot be solved, only
	if the puzzle itself is invalid.

	"""

	def __init__(self, message:str):
		self.message = message


class IndeterminantPuzzleError(Exception):
	"""'
	This exception will be thrown if a puzzle is
	determined to be unsolvable is passed.

	NOTE:
		As the current version of this program cannot solve all puzzles,
		and as this is the mechanism by which a puzzle is determined to
		be solvable, this exception will occasionally be thrown in error.

	"""
	def __init__(self, message:str):
		self.message = message

def PuzzleSolver(filename: str, verbose = False) -> (list, int):
	"""'
	The function used to solve the actual puzzle. This method does the task of
	filling in missing cells, and removing candidates that are not currently valid.

	Args:
		filename (str): The name of the file from which to read the puzzle from.
		verbose (boolean): If true the program will output each step of its process.
				   Useful for debugging or for someone who wants to see the
				   exact steps the program uses to solve each puzzle.

	"""

	if filename[-4:] != ".csv": #: Assume that all files passed are of the csv format.
		filename += ".csv"

	puzzle = load_puzzle(filename) #: Load the puzzle from the given file.

	if verbose:
		#: Print the read puzzle to the screen.
		print("Puzzle loaded from " + filename + " is: ")
		print_puzzle(puzzle)

	#: Create and populate a list containing the row and columns pairs of all cells that
	#: do not contain a number.
	blanks = []
	for row_index, row in enumerate(puzzle):
		for column_index, value in enumerate(row):
			if value == 0: #: If the value at this row is 0
				blanks.append([row_index, column_index]) #: Append its row and column to the list.

	pass_number = 1 #: Tracks how many full passes of the puzzle have currently happened.
	past_pencil = [] #: Keeps track of the possiblities that were found on the last pass.

	#: Generate the pencil. The pencil is a list containing the list of possible
	#: values for each cell within the puzzle.
	#: Read this line as:
	#:	For each row and column (ie for each cell), append a list containing the values
	#:	1 to 9 to this new list being created.
	pencil = [[[i for i in range(1, 10)] for i in range(9)] for i in range(9)]


	while len(blanks) != 0: #: While there are still blank tiles within the puzzle
		if verbose:
			print("Pass number: " + str(pass_number))

		#: Copy the contents of the current pencil into this variable
		#: for use after pencil has been changed.
		past_pencil = list(pencil)


		#: If a cell is not empty, remove all possibilities from this cell.
		for r_index, row in enumerate(puzzle):
			for c_index, cell in enumerate(row):
				if cell != 0:
					pencil[r_index][c_index] = [0]

		#: Remove candidates if a number has been entered into a cell by row, col, and box:
		c_remove_by_exclusion(puzzle, pencil)

		#: Remove Candidates from pencil with Block and column/Row Interaction
		#: If within a box, there are two+ numbers than exist in a line (row or col)
		#: AND they dont exist anywhere else IN the box; nowehere else in that line (row col)
		#: can those numbers exist!
		c_remove_by_block_colrow(pencil, verbose)

		#: Remove candidates using naked sets
		c_remove_by_naked_set(pencil, verbose)
#------------------------------------------------- CODE BELOW THIS LINE IS USED TO FILL CELLS. CODE ABODE IS TO REMOVE CANDIDATED.-------------------------------------------------------------#

		#: Find cells with only one posibility
		for prow_index, pencilled_row in enumerate(pencil):
			for index, possibilities in enumerate(pencilled_row):

				#: For each cell in the puzzle, if the pencil only has one value for that cell, then
				#: That value must be the correct value for that cell.
				if len(possibilities) == 1 and possibilities[0] != 0:
					if get_cell(prow_index, index, puzzle) == 0:
						#: Set the cell with only one possibility to that possibility
						set_cell(prow_index, index,possibilities[0], puzzle, verbose=verbose)
						if verbose:
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
					if get_cell(prow_index, col_index, puzzle) == 0:
						set_cell(prow_index, col_index, i, puzzle, verbose=verbose)
						if verbose:
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
					if get_cell(prow_index, col, puzzle) == 0:
						set_cell(row_index, col, i, puzzle, verbose=verbose)
						if verbose:
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
						if get_cell(locn_box[0], locn_box[1], puzzle) == 0:
							set_cell(locn_box[0], locn_box[1], i, puzzle, verbose=verbose)
							if verbose:
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
			if verbose:
				print("pencil: ")
				print_puzzle(pencil)
			empty_pencil = True
			for row in pencil:
				for item in row:
					if item != [0]:
						empty_pencil = False

			if empty_pencil:
				msg = "This puzzle cannot be determined any futher as there are no more valid moves."
			else:
				msg = "This puzzle cannot be determined any further as ALL blank spaces now have more than 2 open options."
			raise IndeterminantPuzzleError(msg)

		pass_number += 1
	return (puzzle, pass_number - 1)


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

def set_cell(x: int, y: int, new_val , puzzle: list, verbose: bool = True):
	puzzle[x][y] = new_val
	if verbose:
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

def set_box(box_x: int, box_y: int, new_box, puzzle: list):
	x_init = 3 * box_x
	y_init = 3 * box_y
	x_bound = x_init + 3
	y_bound = y_init + 3

	for x in range(x_init, x_bound):
		for y in range(y_init, y_bound):
			for new_value in new_box:
				set_cell(x, y, new_value, puzzle, verbose=False)

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

def c_remove_by_exclusion(puzzle:str, pencil: str):
	for subset in range(9):
		s_row = get_row(subset, puzzle)
		s_col = get_col(subset, puzzle)
		s_box = get_box(subset // 3, subset % 3, puzzle)

		for i in range(1, 10):
			if i in s_row:
				p_row = get_row(subset, pencil)
				for p_cell in p_row:
					if i in p_cell:
						p_cell.remove(i)
			if i in s_col:
				p_col = get_col(subset, pencil)
				for p_cell in p_col:
					if i in p_cell:
						p_cell.remove(i)
			if i in s_box:
				p_box = get_box(subset // 3, subset % 3, pencil)
				for p_cell in p_box:
					if i in p_cell:
						p_cell.remove(i)

def c_remove_by_block_colrow(pencil: str, verbose: bool=False):
	for box_row in range(3):
		for box_col in range(3):
			#: For each set of possibilities
			box = get_box(box_row, box_col, pencil)
			#: Remove candidates from rows
			for inner_row in range(3):
				row_within_box = box[inner_row * 3: (inner_row * 3) + 3]
				for i in range(1, 10):
					count = 0
					double_count = 0
					for index, spos in enumerate(row_within_box):
						if i in spos:
							count += 1
					for spos in box:
						if i in spos:
							double_count += 1
					if count > 1 and double_count == count:
						row = get_row((inner_row + ((box_row) * 3)), pencil)
						for removal_index, removal_spos in enumerate(row):
							if removal_index not in range(box_col * 3, (box_col * 3) + 3):
								if i in removal_spos:
									removal_spos.remove(i)
									if verbose:
										print("Removed " + str(i) + " as a possibility from row " + str((inner_row + ((box_row) * 3) + 1)) +
										" and col " + str(removal_index + 1))

			#: Remove candidates from columns
			for inner_col in range(3):
				col_within_box = box[inner_col::3]
				for i in range(1, 10):
					count = 0
					double_count = 0
					for index, spos in enumerate(col_within_box):
						if i in spos:
							count += 1
					for spos in box:
						if i in spos:
							double_count += 1
					if count > 1 and double_count == count:
						col = get_col((inner_col + ((box_col) * 3)), pencil)
						for removal_index, removal_spos in enumerate(col):
							if removal_index not in range(box_row * 3, (box_row * 3) + 3):
								if i in removal_spos:
									removal_spos.remove(i)
									if verbose:
										print("Removed " + str(i) + " as a possibility from row " + str(removal_index + 1) +
										" and col " + str(inner_col + ((box_col) * 3)))
def c_remove_by_naked_set(pencil: str, verbose: bool=False):
	for subset in range(9):
		p_row = get_row(subset, pencil)
		p_col = get_col(subset, pencil)
		p_box = get_box(subset // 3, subset % 3, pencil)

		#: Find naked sets within Rows
		for c_set in p_row:
			type = len(c_set)
			in_naked = []
			if type >= 2:
				for index, comparison in enumerate(p_row):
					#: If comparison is not the set, and comparison is a subset of set

					if set(comparison) <= set(c_set) and len(comparison) >= 2:
						in_naked.append(index)

				if len(in_naked) >= type and len(in_naked) != len([x for x in p_row if x != [0]]):
					for extranious in [value for value in range(9) if value not in in_naked]:
						#: Generate a new list without the values in c_set that are being removed.
						new_set = [new_set for new_set in p_row[extranious] if new_set not in c_set]

						if new_set != p_row[extranious]:
							#p_row[extranious] = new_set
							set_cell(subset, extranious, new_set, pencil, verbose=False)
							if verbose:
								print("Removed " + str(c_set) + " from (" + str(subset) + ", " + str(extranious) + ") Using naked subsets from rows")

		#: Find naked sets within Cols
		for c_set in p_col:
			type = len(c_set)
			in_naked = []
			if type >= 2:
				for index, comparison in enumerate(p_col):
					#: If comparison is not the set, and comparison is a subset of set

					if set(comparison) <= set(c_set) and len(comparison) >= 2:
						in_naked.append(index)

				if len(in_naked) >= type and len(in_naked) != len([x for x in p_col if x != [0]]):
					for extranious in [value for value in range(9) if value not in in_naked]:
						#: Generate a new list without the values in c_set that are being removed.
						new_set = [new_set for new_set in p_col[extranious] if new_set not in c_set]

						if new_set != p_col[extranious]:
							#p_col[extranious] = new_set
							set_cell(extranious, subset, new_set, pencil, verbose=False)
							if verbose:
								print("Removed " + str(c_set) + " from (" + str(extranious) + ", " + str(subset) + ") Using naked subsets from cols")

		#: Find naked sets within Boxes
		for c_set in p_box:
			type = len(c_set)
			in_naked = []
			if type >= 2:
				for index, comparison in enumerate(p_box):
					#: If comparison is not the set, and comparison is a subset of set

					if set(comparison) <= set(c_set) and len(comparison) >= 2:
						in_naked.append(index)

				if len(in_naked) >= type and len(in_naked) != len([x for x in p_box if x != [0]]):
					for extranious in [value for value in range(9) if value not in in_naked]:
						#: Generate a new list without the values in c_set that are being removed.
						new_set = [new_set for new_set in p_box[extranious] if new_set not in c_set]

						if new_set != p_box[extranious]:
							box_x = subset // 3
							box_y = subset % 3
							cell_within_x = extranious // 3
							cell_within_y = extranious % 3
							cell_x = (box_x * 3) + cell_within_x
							cell_y = (box_y * 3) + cell_within_y

							set_cell(cell_x, cell_y, new_set, pencil, verbose=False)
							if verbose:
								print("Removed " + str(c_set) + " from (" + str(cell_x) + ", " + str(cell_y) + ") Using naked subsets from boxes")


if __name__ == "__main__":

	#: Create an arugment parser to be used when this is called from the command line.
	parser = argparse.ArgumentParser(description="Command line Sudoku puzzle solver.")

        #: Create the equation argument.
	parser.add_argument("FileName", type=str, help="The file to load the puzzle from.")

        #: Create the verbose argument.
	parser.add_argument('-v', "--verbose", action="store_true",
				help="Output at each step for the solution.")

        #: Parse the arguments.
	args = parser.parse_args()

        #: Print the result of the passed equation. If the verbose argument was given,
        #: output each step of the computing process.
	soln = Solver(args.FileName, args.verbose)

	if not args.verbose:
		print_puzzle(soln[0])
	print("The puzzle has been sucessfully solved after " + str(soln[1]) + " passes.")
