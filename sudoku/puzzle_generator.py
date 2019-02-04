
"""
Generates Sudoku Puzzles on a 9x9 grid
Numbers 1-9 with no repeating numbers in rows, columns, or sub-grids of 3x3
Upon generating a complete solution, must delete numbers to create an unambiguous sodoku puzzle
"""

import sys
import random
from time import time
from .puzzle_solver import print_puzzle, get_cell, get_row, get_col, get_box, set_cell


#: primary function where grid is generated
def generate_grid():	
    t1 = time()  #: starts timer to measure program speed
    rows = 9
    columns = 9
    new_num = 0  #: number to be added to the grid

    #: create a zero matrix as an empty grid
    #: imported print_puzzle function will display zeroes as blank space
    grid = [[0 for i in range(columns)] for j in range(rows)]

    is_stuck = False

    #: start infinite loop to repeatedly attempt to generate a complete sudoku grid
    #: breaks when complete grid is generated
    while True:

        #: traverse the grid left to right, top to bottom
        #: adds random number 1-9 at each location
        for row_index in range(len(grid)):
            for column_index in range(len(grid[row_index])):

                #: create loop to repeatedly attempt to place new number
                #: checks repetition rules before placing, if repetition -> try again
                #: limit 999 added in case generator reaches logical stalemate -> try again
                for i in range(999):

                    #: set flag before reaching end of loop to break all loops and try again
                    if i == 998:
                        is_stuck = True

                    new_num = random.randint(1,9)  #: starts with random number 1-9

                    #: if first number in row, only check column
                    if column_index == 0:
                        if check_col(grid, new_num, 0, columns, column_index):
                            if check_group(grid, row_index, column_index, new_num):
                                grid[row_index][column_index] = new_num
                                break

                    #: checks both for row and column
                    #: if number is already in row or column, restart loop with new random number
                    elif new_num not in grid[row_index]:
                        if check_col(grid, new_num, 0, columns, column_index):
                            if check_group(grid, row_index, column_index, new_num):
                                grid[row_index][column_index] = new_num
                                break
                if is_stuck == True:
                    break
            if is_stuck == True:
                is_stuck = False
                break

        #: check for complete grid
        #: if grid has been completely filled out: print time and puzzle, break loop, end program
        if check_zero(grid):
            t2 = time()
            print(str(t2 - t1) + " seconds")
            print_puzzle(grid)
            break

        #: if program reaches this point, puzzle generation was unsuccessful
        #: reset grid and try again
        grid = [[0 for i in range(columns)] for j in range(rows)]


#: checks if new number is already in the column
#: returns false if number is already in column
def check_col(grid, temp, s_cols, e_cols, column_index) -> bool:
    for row_index in range(len(grid)):
        if row_index == e_cols:
            break
        if temp == grid[row_index][column_index]:
            return False
    return True


#: checks 3x3 sub-grid for repeating numbers
def check_group(grid, row_index, column_index, x) -> bool:

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
    for r_i in range(9):
        for c_i in range(9):

            if r_i > gr*3-3 and r_i < gr*3:  #: row index must be between start of subgrid and end of subgrid
                if c_i > gc*3-3 and c_i < gc*3:  #: column index must also be between start and end of subgrid
                    subgrid[r_i-(gr*3-3)][c_i-(gc*3-3)] = grid[r_i][c_i]

    #: check to see if number is already in subgrid
    for i in range(3):
        for j in range(3):
            if subgrid[i][j] == x:
                return False

    return True


def check_zero(grid) -> bool:

    for row_index in range(len(grid)):
        for column_index in range(len(grid[row_index])):
            if grid[row_index][column_index] == 0:
                return False
    return True

if __name__ == "__main__":
    generate_grid()
