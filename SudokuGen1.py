"""
Generates Sudoku Puzzles on a 9x9 grid
Numbers 1-9 with no repeating numbers in rows, columns, or sub-grids of 3x3
Upon generating a complete solution, must delete numbers to create an unambiguous sodoku puzzle
"""

import sys
import random
from SudokuSolver import print_puzzle
from SudokuSolver import get_cell
from SudokuSolver import get_row
from SudokuSolver import get_col
from SudokuSolver import get_box
from SudokuSolver import set_cell

#: variables used in multiple functions
rows = 9
columns = 9
new_num = 0
grid = [[0 for i in range(columns)] for j in range(rows)]
flag = False

#: primary function where grid is generated
def generate_grid():	

	for row_index in range(len(grid)):
		for column_index in range(len(grid[row_index])):
			
			while True:

				new_num = random.randint(1,9)  #: starts with random number 1-9
				#: if first number in row, only check column
				if column_index == 0:
					if check_col(new_num, 0, columns, column_index):
						if check_group(row_index, column_index, new_num):
							grid[row_index][column_index] = new_num
							break

				#: checks both for row and column
				#: if number is already in row or column, restart loop with new random number
				elif new_num not in grid[row_index]:
					if check_col(new_num, 0, columns, column_index):
						if check_group(row_index, column_index, new_num):
							grid[row_index][column_index] = new_num
							print_puzzle(grid)
							break
	print_puzzle(grid)  #: prints grid (imported from SudokuSolver)

#: checks if new number is already in the column
#: returns false if number is already in column
def check_col(temp, s_cols, e_cols, column_index) -> bool:
	for row_index in range(len(grid)):
		if row_index == e_cols:
			break
		if temp == grid[row_index][column_index]:
			return False
	return True


#: checks 3x3 sub-grid for repeating numbers
def check_group(row_index, column_index, x) -> bool:

	#: start by grouping 3x3 sub-grids

	gr = 0  #: grid row
	gc = 0  #: grid column
	
	subgrid = [[0 for i in range(3)] for j in range(3)]  #: create for temporary testing use
	
	if row_index < 3:
		gr = 1
	elif row_index > 2 and row_index < 6:
		gr = 2
	elif row_index > 5:
		gr = 3		
	
	if column_index < 3:
		gc = 1
	elif column_index > 2 and column_index < 6:
		gc = 2
	elif column_index > 5:
		gc = 3

	#: fill in subgrid
	if gr == 1:

		if gc == 1:

			for r_i in range(3):
				for c_i in range(3):
					subgrid[r_i][c_i] = grid[r_i][c_i]
	
		if gc == 2:

			for r_i in range(3):
				for c_i in range(6):

					if c_i > 2:
						subgrid[r_i][c_i-3] = grid[r_i][c_i]
		
		if gc == 3:

			for r_i in range(3):
				for c_i in range(9):
				
					if c_i > 5:
						subgrid[r_i][c_i-6] = grid[r_i][c_i]
	if gr == 2:

		if gc == 1:

			for r_i in range(6):
				for c_i in range(3):

					if r_i > 2:
						subgrid[r_i-3][c_i] = grid[r_i][c_i]
	
		if gc == 2:

			for r_i in range(6):
				for c_i in range(6):

					if r_i > 2 and c_i > 2:
						subgrid[r_i-3][c_i-3] = grid[r_i][c_i]
		
		if gc == 3:

			for r_i in range(6):
				for c_i in range(9):
				
					if r_i > 2 and c_i > 5:
						subgrid[r_i-3][c_i-6] = grid[r_i][c_i]
	if gr == 3:

		if gc == 1:

			for r_i in range(9):
				for c_i in range(3):

					if r_i > 5:
						subgrid[r_i-6][c_i] = grid[r_i][c_i]
	
		if gc == 2:

			for r_i in range(9):
				for c_i in range(6):

					if r_i > 5 and c_i > 2:
						subgrid[r_i-6][c_i-3] = grid[r_i][c_i]
		
		if gc == 3:

			for r_i in range(9):
				for c_i in range(9):
				
					if r_i > 5 and c_i > 5:
						subgrid[r_i-6][c_i-6] = grid[r_i][c_i]

	#: check to see if number is already in subgrid
	for i in range(3):
		for j in range(3):
			if subgrid[i][j] == x:
				return False
	
	return True

if __name__ == "__main__":
	generate_grid()
