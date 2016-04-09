'''
Construct and return sudoku CSP models.
'''

from cspbase import *
import itertools

def sudoku_csp_model_1(initial_sudoku_board):
    '''Return a CSP object representing a sudoku CSP problem along 
       with an array of variables for the problem. That is return

       sudoku_csp, variable_array

       where sudoku_csp is a csp representing sudoku using model_1
       and variable_array is a list of lists

       [ [  ]
         [  ]
         .
         .
         .
         [  ] ]

       such that variable_array[i][j] is the Variable (object) that
       you built to represent the value to be placed in cell i,j of
       the sudokup board (indexed from (0,0) to (8,8))

       
       
       The input board is specified as a list of 9 lists. Each of the
       9 lists represents a row of the board. If a 0 is in the list it
       represents an empty cell. Otherwise if a number between 1--9 is
       in the list then this represents a pre-set board
       position. E.g., the board
    
       -------------------  
       | | |2| |9| | |6| |
       | |4| | | |1| | |8|
       | |7| |4|2| | | |3|
       |5| | | | | |3| | |
       | | |1| |6| |5| | |
       | | |3| | | | | |6|
       |1| | | |5|7| |4| |
       |6| | |9| | | |2| |
       | |2| | |8| |1| | |
       -------------------
       would be represented by the list of lists
       
       [[0,0,2,0,9,0,0,6,0],
       [0,4,0,0,0,1,0,0,8],
       [0,7,0,4,2,0,0,0,3],
       [5,0,0,0,0,0,3,0,0],
       [0,0,1,0,6,0,5,0,0],
       [0,0,3,0,0,0,0,0,6],
       [1,0,0,0,5,7,0,4,0],
       [6,0,0,9,0,0,0,2,0],
       [0,2,0,0,8,0,1,0,0]]
       
       
       This routine returns Model_1 which consists of a variable for
       each cell of the board, with domain equal to {1-9} if the board
       has a 0 at that position, and domain equal {i} if the board has
       a fixed number i at that cell.
       
       Model_1 also contains BINARY CONSTRAINTS OF NOT-EQUAL between
       all relevant variables (e.g., all pairs of variables in the
       same row, etc.), then invoke enforce_gac on those
       constraints. All of the constraints of Model_1 MUST BE binary
       constraints (i.e., constraints whose scope includes two and
       only two variables).
    '''
    
    csp_variables = create_variable_objects(initial_sudoku_board)
    constraints = create_not_equal_constraints(csp_variables)
    
    csp_name = "sudoku board"
    csp_obj = CSP(csp_name)
    for i in csp_variables:
        for j in i:
            csp_obj.add_var(j)

    for c in constraints:
        csp_obj.add_constraint(c)
    
    return csp_obj, csp_variables


def create_variable_objects(board):

    list_variables = list()

    for row in board:
        variables_row_lst = list()
        for col_num in range(0,9):
            if row[col_num] != 0:
                # create variable object
                row_num = board.index(row)
                # naming - Row # Col # is Z.
                name = str(row_num) + str(col_num)
                domain = [row[col_num]]
                var = Variable(name, domain)
                variables_row_lst.append(var)
                # append to a list X 
            else:
                # create variable object
                name = "e"
                domain = [1,2,3,4,5,6,7,8,9]
                var = Variable(name, domain)
                variables_row_lst.append(var)
                # append to a list X
        if len(variables_row_lst) == 9:
            list_variables.append(variables_row_lst)
    return list_variables

def create_not_equal_constraints(variables):
    constraints = []

    ## Row constraints 
    for i in range(0,9):
        row = variables[i]
        for f1 in range(0,9):
            # get next Variable after Variable f
            for f2 in range(f1+1, 9):
                var1 = row[f1]
                var2 = row[f2]
                name = var1.name + var2.name
                new_constraint = Constraint(name, [var1, var2])
                tuples = []
                for x in var1.cur_domain():
                    for y in var2.cur_domain():
                        if x != y:
                            tuples.append((x,y))
                tuples = tuple(tuples)
                new_constraint.add_satisfying_tuples(tuples)
                constraints.append(new_constraint)
    
    ## Column constraints
    for i in range(0,9):
        column = get_column(variables, i)
        for f1 in range(0,9):
            # get next Variable after Variable f
            for f2 in range(f1+1, 9):
                var1 = column[f1]
                var2 = column[f2]
                name = var1.name + var2.name
                new_constraint = Constraint(name, [var1, var2])
                tuples = []
                for x in var1.cur_domain():
                    for y in var2.cur_domain():
                        if x != y:
                            tuples.append((x,y))
                tuples = tuple(tuples)
                new_constraint.add_satisfying_tuples(tuples)
                constraints.append(new_constraint)

    # 3 by 3 square constraints
    for i in range(0,9):
        square = get_square(variables, i)
        for f1 in range(0,9):
            # get next Variable after Variable f
            for f2 in range(f1+1, 9):
                var1 = square[f1]
                var2 = square[f2]
                name = var1.name + var2.name
                new_constraint = Constraint(name, [var1, var2])
                tuples = []
                for x in var1.cur_domain():
                    for y in var2.cur_domain():
                        if x != y:
                            tuples.append((x,y))
                tuples = tuple(tuples)
                new_constraint.add_satisfying_tuples(tuples)
                
                constraints.append(new_constraint)
    return constraints



def get_column(board, i):
    L = []
    for j in range(0,9):
        L.append(board[j][i])
    return L

def get_square(board, i):
    row_one = (i // 3) * 3
    col_one = (i % 3) * 3
    square = [None] * 9 
    for k in range(0,9):
        sub1 = k // 3 
        sub2 = k % 3
        square[k] = board[row_one + sub1][col_one + sub2]
    return square

##############################

def sudoku_csp_model_2(initial_sudoku_board):
    '''Return a CSP object representing a sudoku CSP problem along 
       with an array of variables for the problem. That is return

       sudoku_csp, variable_array

       where sudoku_csp is a csp representing sudoku using model_1
       and variable_array is a list of lists

       [ [  ]
         [  ]
         .
         .
         .
         [  ] ]

       such that variable_array[i][j] is the Variable (object) that
       you built to represent the value to be placed in cell i,j of
       the sudokup board (indexed from (0,0) to (8,8))

    The input board takes the same input format (a list of 9 lists
    specifying the board as sudoku_csp_model_1.
    
    The variables of model_2 are the same as for model_1: a variable
    for each cell of the board, with domain equal to {1-9} if the
    board has a 0 at that position, and domain equal {i} if the board
    has a fixed number i at that cell.

    However, model_2 has different constraints. In particular, instead
    of binary non-equals constaints model_2 has 27 all-different
    constraints: all-different constraints for the variables in each
    of the 9 rows, 9 columns, and 9 sub-squares. Each of these
    constraints is over 9-variables (some of these variables will have
    a single value in their domain). model_2 should create these
    all-different constraints between the relevant variables, then
    invoke enforce_gac on those constraints.
    '''


    csp_variables = create_variable_objects(initial_sudoku_board)
    constraints = create_all_diff_constraints(csp_variables)

    csp_name = "sudoku board"
    csp_obj = CSP(csp_name)
    for i in csp_variables:
        for j in i:
            csp_obj.add_var(j)

    for c in constraints:
        csp_obj.add_constraint(c)
    
    return csp_obj, csp_variables

def create_all_diff_constraints(variables):

    constraints = []

    ## Row constraints
    for n in range(0, 9):
        lst = []
        for k in range(0, 9):
            lst.append(variables[n][k])
        name = 'All-DIFF Row' + str(n)
        new_constraint = Constraint(name, lst)
        new_constraint.add_satisfying_tuples(helper_all_diff(lst))
        constraints.append(new_constraint)

    ## Column constraints
    for n in range(0, 9):
        lst = []
        for k in range(0, 9):
            lst.append(variables[k][n])
        name = 'All-DIFF Column' + str(n)
        new_constraint = Constraint(name, lst)
        new_constraint.add_satisfying_tuples(helper_all_diff(lst))
        constraints.append(new_constraint)

    ## Sub square constraints

    for n in range(0, 9):
        lst = []
        x = int(n/3) * 3
        y = int(n/3) * 3 + 3
        for cur_row in range(x, y):
            x1 = int(n % 3) * 3 
            y1 = int(n % 3) * 3 + 3
            for cur_col in range(x1, y1):
                lst.append(variables[cur_row][cur_col])
        name = 'All-DIFF Sub Square' + str(n + 1)
        new_constraint = Constraint(name, lst)
        new_constraint.add_satisfying_tuples(helper_all_diff(lst))
        constraints.append(new_constraint)

    return constraints

def helper_all_diff(bound):
    final_lst = []
    for i in range(0,1):
        final_lst.append([])
    for var in bound:
        lst = []
        while len(final_lst) > 0:
            temp = final_lst.pop(0)
            for value in var.cur_domain():
                if value not in temp:
                    t = temp[:]
                    t.append(value)
                    lst.append(t)
        final_lst = lst
    return final_lst

