##This function verifies that a given solution to a sudoku puzzle is a valid solution.

from cspbase import *

##Takes in a sudoku_variable_array, as specified in sudoku_csp
##variable_array[i][j] is the Variable (object) that represents the value to be placed in cell i,j of the sudoku board
##It is assumed that every variable in this array has been assigned
##a value.
##Returns True if the variable values are a valid solution; 
##Returns False otherwise
def check_solution(sudoku_variable_array):
	##check the rows
	for i in range(9):
		row_sol = [] 
		for j in range(9):
			row_sol.append(sudoku_variable_array[i][j].get_assigned_value())
		if not check_list(row_sol):
			return False	
	for j in range(9):
		col_sol = []
		for i in range(9):
			col_sol.append(sudoku_variable_array[i][j].get_assigned_value())
		if not check_list(col_sol):
			return False
	block_starting_indices = [ [0,0], [0,3],[0,6],[3,0],[3,3],[3,6],[6,0],[6,3],[6,6]]

	for start in block_starting_indices:
		block_list = [] 
		for add_i in range(3):
			for add_j in range(3):
				i = start[0] + add_i
				j = start[1] + add_j
				block_list.append(sudoku_variable_array[i][j].get_assigned_value())
		if not check_list(block_list):
			return False
	return True
	
##Helper function that checks if a given list is valid
def check_list(solution_list):
	solution_list.sort()
	return solution_list == list(range(1,10))
