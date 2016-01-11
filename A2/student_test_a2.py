from cspbase import *
import itertools
import traceback

import propagators as soln_propagators


########################################
##Necessary setup to generate problems

def queensCheck(qi, qj, i, j):
    '''Return true if i and j can be assigned to the queen in row qi and row qj 
       respectively. Used to find satisfying tuples.
    '''
    return i != j and abs(i-j) != abs(qi-qj)

def nQueens(n):
    '''Return an n-queens CSP'''
    i = 0
    dom = []
    for i in range(n):
        dom.append(i+1)

    vars = []
    for i in dom:
        vars.append(Variable('Q{}'.format(i), dom))

    cons = []    
    for qi in range(len(dom)):
        for qj in range(qi+1, len(dom)):
            con = Constraint("C(Q{},Q{})".format(qi+1,qj+1),[vars[qi], vars[qj]]) 
            sat_tuples = []
            for t in itertools.product(dom, dom):
                if queensCheck(qi, qj, t[0], t[1]):
                    sat_tuples.append(t)
            con.add_satisfying_tuples(sat_tuples)
            cons.append(con)
    
    csp = CSP("{}-Queens".format(n), vars)
    for c in cons:
        csp.add_constraint(c)
    return csp

############################################

#@max_grade(1)
##Tests FC after the first queen is placed in position 1.
def test_simple_FC(stu_propagators):
	score = 0

	print("---starting test_simple_FC---")
	did_fail = False
	try:
		queens = nQueens(8)
		curr_vars = queens.get_all_vars()
		curr_vars[0].assign(1)
		stu_propagators.prop_FC(queens,newVar=curr_vars[0])
		answer = [[1],[3, 4, 5, 6, 7, 8],[2, 4, 5, 6, 7, 8],[2, 3, 5, 6, 7, 8],[2, 3, 4, 6, 7, 8],[2, 3, 4, 5, 7, 8],[2, 3, 4, 5, 6, 8],[2, 3, 4, 5, 6, 7]]
		var_domain = [x.cur_domain() for x in curr_vars]
		for i in range(len(curr_vars)):
			if var_domain[i] != answer[i]:
				print("FAILED test_simple_FC\nExplanation:\nFC variable domains should be: %r\nFC variable domains are: %r" % (answer,var_domain))
				did_fail = True
				break
		if not did_fail:
			print("PASS")
			score = 2
	
	except Exception:
		print("Error occurred: %r" % traceback.print_exc())

	print("---finished test_simple_FC---\n")

	return score

#@max_grade(1)
##Tests GAC after the first queen is placed in position 1.
def test_simple_GAC(stu_propagators):
	score = 0
	print("---starting test_simple_GAC---")
	did_fail = False
	try:
		queens = nQueens(8)
		curr_vars = queens.get_all_vars()
		curr_vars[0].assign(1)
		stu_propagators.prop_GAC(queens,newVar=curr_vars[0])
		answer = [[1],[3, 4, 5, 6, 7, 8],[2, 4, 5, 6, 7, 8],[2, 3, 5, 6, 7, 8],[2, 3, 4, 6, 7, 8],[2, 3, 4, 5, 7, 8],[2, 3, 4, 5, 6, 8],[2, 3, 4, 5, 6, 7]]
		var_domain = [x.cur_domain() for x in curr_vars]
		for i in range(len(curr_vars)):
			if var_domain[i] != answer[i]:
				print("FAILED test_simple_GAC\nExplanation:\nGAC variable domains should be: %r\nGAC variable domains are: %r" % (answer,var_domain))
				did_fail = True
				break
		if not did_fail:
			print("PASS")
			score = 2

	except Exception:
		print("Error occurred: %r" % traceback.print_exc())

	print("---finished test_simple_GAC---\n")
	return score

#@max_grade(2)
##Simple example with 3 queens that results in different pruning for FC & GAC
##Q1 is placed in slot 2, q2 is placed in slot 4, and q8 is placed in slot 8.
##Checking GAC.
def three_queen_GAC(stu_propagators):
	score = 0
	print("---starting three_queen_GAC---")
	try:
		queens = nQueens(8)
		curr_vars = queens.get_all_vars()
		curr_vars[0].assign(4)
		curr_vars[2].assign(1)
		curr_vars[7].assign(5)
		stu_propagators.prop_GAC(queens)

		answer = [[4],[6, 7, 8],[1],[3, 8],[6, 7],[2, 8],[2, 3, 7, 8],[5]]
		var_vals = [x.cur_domain() for x in curr_vars]

		if var_vals != answer:
			print("FAILED\nExpected Output: %r\nOutput Received: %r" % (answer,var_vals))

		else:
			print("PASS")
			score = 3
	except Exception:
		print("Error occurred: %r" % traceback.print_exc())

	print("---finished three_queen_GAC---\n")
	return score

#@max_grade(2)
##Simple example with 3 queens that results in different pruning for FC & GAC
##Q1 is placed in slot 2, q2 is placed in slot 4, and q8 is placed in slot 8.
##Checking FC.
def three_queen_FC(stu_propagators):
	score = 0
	print("---starting three_queen_FC---")
	try:
		queens = nQueens(8)
		curr_vars = queens.get_all_vars()
		curr_vars[0].assign(4)
		curr_vars[2].assign(1)
		curr_vars[7].assign(5)
		stu_propagators.prop_FC(queens)

		answer = [[4],[6, 7, 8],[1],[3, 6, 8],[6, 7],[2, 6, 8],[2, 3, 7, 8],[5]]
		var_vals = [x.cur_domain() for x in curr_vars]

		if var_vals != answer:
			print("FAILED\nExpected Output: %r\nOutput Received: %r" % (answer,var_vals))

		else:
			print("PASS")
			score = 3
	except Exception:
		print("Error occurred: %r" % traceback.print_exc())

	print("---finished three_queen_FC---\n")
	return score


#@max_grade(1)
##Checking that importing a sudoku board into model 1 works as expected.
##Passing this test is a prereq for passing check_model_1_constraints.
def model_1_import(stu_models):
	score = 0
	print("---starting model_1_import---")
	try:
		board = [[0,0,8,7,0,0,0,5,0],[0,3,0,0,1,0,0,9,0],[0,0,0,5,0,0,1,0,0],[4,0,3,0,0,7,0,0,0],[9,7,0,0,0,0,0,1,8],[0,0,0,8,0,0,3,0,9],[0,0,6,0,0,4,0,0,0],[0,9,0,0,8,0,0,2,0],[0,5,0,0,0,1,8,0,0]]

		answer = [[1, 2, 3, 4, 5, 6, 7, 8, 9], [1, 2, 3, 4, 5, 6, 7, 8, 9], [8], [7], [1, 2, 3, 4, 5, 6, 7, 8, 9], [1, 2, 3, 4, 5, 6, 7, 8, 9], [1, 2, 3, 4, 5, 6, 7, 8, 9], [5], [1, 2, 3, 4, 5, 6, 7, 8, 9], [1, 2, 3, 4, 5, 6, 7, 8, 9], [3], [1, 2, 3, 4, 5, 6, 7, 8, 9], [1, 2, 3, 4, 5, 6, 7, 8, 9], [1], [1, 2, 3, 4, 5, 6, 7, 8, 9], [1, 2, 3, 4, 5, 6, 7, 8, 9], [9], [1, 2, 3, 4, 5, 6, 7, 8, 9], [1, 2, 3, 4, 5, 6, 7, 8, 9], [1, 2, 3, 4, 5, 6, 7, 8, 9], [1, 2, 3, 4, 5, 6, 7, 8, 9], [5], [1, 2, 3, 4, 5, 6, 7, 8, 9], [1, 2, 3, 4, 5, 6, 7, 8, 9], [1], [1, 2, 3, 4, 5, 6, 7, 8, 9], [1, 2, 3, 4, 5, 6, 7, 8, 9], [4], [1, 2, 3, 4, 5, 6, 7, 8, 9], [3], [1, 2, 3, 4, 5, 6, 7, 8, 9], [1, 2, 3, 4, 5, 6, 7, 8, 9], [7], [1, 2, 3, 4, 5, 6, 7, 8, 9], [1, 2, 3, 4, 5, 6, 7, 8, 9], [1, 2, 3, 4, 5, 6, 7, 8, 9], [9], [7], [1, 2, 3, 4, 5, 6, 7, 8, 9], [1, 2, 3, 4, 5, 6, 7, 8, 9], [1, 2, 3, 4, 5, 6, 7, 8, 9], [1, 2, 3, 4, 5, 6, 7, 8, 9], [1, 2, 3, 4, 5, 6, 7, 8, 9], [1], [8], [1, 2, 3, 4, 5, 6, 7, 8, 9], [1, 2, 3, 4, 5, 6, 7, 8, 9], [1, 2, 3, 4, 5, 6, 7, 8, 9], [8], [1, 2, 3, 4, 5, 6, 7, 8, 9], [1, 2, 3, 4, 5, 6, 7, 8, 9], [3], [1, 2, 3, 4, 5, 6, 7, 8, 9], [9], [1, 2, 3, 4, 5, 6, 7, 8, 9], [1, 2, 3, 4, 5, 6, 7, 8, 9], [6], [1, 2, 3, 4, 5, 6, 7, 8, 9], [1, 2, 3, 4, 5, 6, 7, 8, 9], [4], [1, 2, 3, 4, 5, 6, 7, 8, 9], [1, 2, 3, 4, 5, 6, 7, 8, 9], [1, 2, 3, 4, 5, 6, 7, 8, 9], [1, 2, 3, 4, 5, 6, 7, 8, 9], [9], [1, 2, 3, 4, 5, 6, 7, 8, 9], [1, 2, 3, 4, 5, 6, 7, 8, 9], [8], [1, 2, 3, 4, 5, 6, 7, 8, 9], [1, 2, 3, 4, 5, 6, 7, 8, 9], [2], [1, 2, 3, 4, 5, 6, 7, 8, 9], [1, 2, 3, 4, 5, 6, 7, 8, 9], [5], [1, 2, 3, 4, 5, 6, 7, 8, 9], [1, 2, 3, 4, 5, 6, 7, 8, 9], [1, 2, 3, 4, 5, 6, 7, 8, 9], [1], [8], [1, 2, 3, 4, 5, 6, 7, 8, 9], [1, 2, 3, 4, 5, 6, 7, 8, 9]]
		
		csp, var_array = stu_models.sudoku_csp_model_1(board)
		lister = [] 
		
		for i in range(9):
			for j in range(9):
				lister.append(var_array[i][j].cur_domain())

		if lister != answer:
			print("FAILED\nExpected Output: %r\nOutput Received: %r" % (answer,lister))
		else:
			print("PASS")
			score = 1
	except Exception:
		print("Error occurred: %r" % traceback.print_exc())
	print("---finished model_1_import---\n")
	return score
	

#@max_grade(1)
##Checking that importing a sudoku board into model 2 works as expected.
##Passing this test is a prereq for passing check_model_2_constraints.
def model_2_import(stu_models):

	score = 0
	print("---starting model_2_import---")
	try:
		board = [[0,0,8,7,0,0,0,5,0],[0,3,0,0,1,0,0,9,0],[0,0,0,5,0,0,1,0,0],[4,0,3,0,0,7,0,0,0],[9,7,0,0,0,0,0,1,8],[0,0,0,8,0,0,3,0,9],[0,0,6,0,0,4,0,0,0],[0,9,0,0,8,0,0,2,0],[0,5,0,0,0,1,8,0,0]]

		answer = [[1, 2, 3, 4, 5, 6, 7, 8, 9], [1, 2, 3, 4, 5, 6, 7, 8, 9], [8], [7], [1, 2, 3, 4, 5, 6, 7, 8, 9], [1, 2, 3, 4, 5, 6, 7, 8, 9], [1, 2, 3, 4, 5, 6, 7, 8, 9], [5], [1, 2, 3, 4, 5, 6, 7, 8, 9], [1, 2, 3, 4, 5, 6, 7, 8, 9], [3], [1, 2, 3, 4, 5, 6, 7, 8, 9], [1, 2, 3, 4, 5, 6, 7, 8, 9], [1], [1, 2, 3, 4, 5, 6, 7, 8, 9], [1, 2, 3, 4, 5, 6, 7, 8, 9], [9], [1, 2, 3, 4, 5, 6, 7, 8, 9], [1, 2, 3, 4, 5, 6, 7, 8, 9], [1, 2, 3, 4, 5, 6, 7, 8, 9], [1, 2, 3, 4, 5, 6, 7, 8, 9], [5], [1, 2, 3, 4, 5, 6, 7, 8, 9], [1, 2, 3, 4, 5, 6, 7, 8, 9], [1], [1, 2, 3, 4, 5, 6, 7, 8, 9], [1, 2, 3, 4, 5, 6, 7, 8, 9], [4], [1, 2, 3, 4, 5, 6, 7, 8, 9], [3], [1, 2, 3, 4, 5, 6, 7, 8, 9], [1, 2, 3, 4, 5, 6, 7, 8, 9], [7], [1, 2, 3, 4, 5, 6, 7, 8, 9], [1, 2, 3, 4, 5, 6, 7, 8, 9], [1, 2, 3, 4, 5, 6, 7, 8, 9], [9], [7], [1, 2, 3, 4, 5, 6, 7, 8, 9], [1, 2, 3, 4, 5, 6, 7, 8, 9], [1, 2, 3, 4, 5, 6, 7, 8, 9], [1, 2, 3, 4, 5, 6, 7, 8, 9], [1, 2, 3, 4, 5, 6, 7, 8, 9], [1], [8], [1, 2, 3, 4, 5, 6, 7, 8, 9], [1, 2, 3, 4, 5, 6, 7, 8, 9], [1, 2, 3, 4, 5, 6, 7, 8, 9], [8], [1, 2, 3, 4, 5, 6, 7, 8, 9], [1, 2, 3, 4, 5, 6, 7, 8, 9], [3], [1, 2, 3, 4, 5, 6, 7, 8, 9], [9], [1, 2, 3, 4, 5, 6, 7, 8, 9], [1, 2, 3, 4, 5, 6, 7, 8, 9], [6], [1, 2, 3, 4, 5, 6, 7, 8, 9], [1, 2, 3, 4, 5, 6, 7, 8, 9], [4], [1, 2, 3, 4, 5, 6, 7, 8, 9], [1, 2, 3, 4, 5, 6, 7, 8, 9], [1, 2, 3, 4, 5, 6, 7, 8, 9], [1, 2, 3, 4, 5, 6, 7, 8, 9], [9], [1, 2, 3, 4, 5, 6, 7, 8, 9], [1, 2, 3, 4, 5, 6, 7, 8, 9], [8], [1, 2, 3, 4, 5, 6, 7, 8, 9], [1, 2, 3, 4, 5, 6, 7, 8, 9], [2], [1, 2, 3, 4, 5, 6, 7, 8, 9], [1, 2, 3, 4, 5, 6, 7, 8, 9], [5], [1, 2, 3, 4, 5, 6, 7, 8, 9], [1, 2, 3, 4, 5, 6, 7, 8, 9], [1, 2, 3, 4, 5, 6, 7, 8, 9], [1], [8], [1, 2, 3, 4, 5, 6, 7, 8, 9], [1, 2, 3, 4, 5, 6, 7, 8, 9]]
		
		csp, var_array = stu_models.sudoku_csp_model_2(board)
		lister = [] 
		
		for i in range(9):
			for j in range(9):
				lister.append(var_array[i][j].cur_domain())

		if lister != answer:
			print("FAILED\nExpected Output: %r\nOutput Received: %r" % (answer,lister))
		else:
			print("PASS")
			score = 1
	except Exception:
		print("Error occurred: %r" % traceback.print_exc())
	print("---finished model_2_import---\n")
	return score

	
#@max_grade(2)
##Checks that model 1 constraints pass when all different, and fail when not all different
def check_model_1_constraints_enum(stu_models):
	score = 2
	print("---starting check_model_1_constraints_enum---")
	try: 		
		board = [[0,0,8,7,0,0,0,5,0],[0,3,0,0,1,0,0,9,0],[0,0,0,5,0,0,1,0,0],[4,0,3,0,0,7,0,0,0],[9,7,0,0,0,0,0,1,8],[0,0,0,8,0,0,3,0,9],[0,0,6,0,0,4,0,0,0],[0,9,0,0,8,0,0,2,0],[0,5,0,0,0,1,8,0,0]]

		csp, var_array = stu_models.sudoku_csp_model_1(board)

		for cons in csp.get_all_cons():
			all_vars = cons.get_scope()
			taken = [] 
			domain_list = [] 
			should_pass = []
			should_fail = [] 
			for va in all_vars:
				domain_list.append(va.cur_domain())
				if len(va.cur_domain()) == 1:
					taken.append(va.cur_domain()[0])
			for i in range(len(all_vars)):
				va = all_vars[i]
				domain = domain_list[i] 
				if len(domain) == 1:
					should_pass.append(domain[0])
					should_fail.append(domain[0])
				else:
					for i in range(1,10):
						if i in domain and i in taken:
							should_fail.append(i)
							break
					for i in range(1,10):
						if i in domain and i not in taken:
							should_pass.append(i)
							taken.append(i)
							break
			if cons.check(should_fail) != cons.check(should_pass):
				if cons.check(should_fail) or not cons.check(should_pass):
					if not cons.check(should_fail):
						print("FAILED\nConstraint %s should be falsified by %r" % (str(cons),should_fail))
						print("var domains:")
						for va in all_vars:
							print(va.cur_domain())
					if cons.check(should_pass):
						print("FAILED\nConstraint %s should be satisfied by %r" % (str(cons),should_pass))
						print("var domains:")
						for va in all_vars:
							print(va.cur_domain())
					print("---finished check_model_1_constraints_enum---\n")
					return 0

	except Exception:
		print("Error occurred: %r" % traceback.print_exc())
		print("---finished check_model_1_constraints_enum---\n")
		return 0
	
	print("PASS")
	print("---finished check_model_1_constraints_enum---\n")
	return score



#@max_grade(2)
##Checks that model 1 constraints are implemented as expected.
##Both model_1_import must pass and prop_GAC must be implemented correctly for this test to behave as intended.
def check_model_1_constraints(stu_model):
	score = 0
	print("---starting check_model_1_constraints---")
	try: 		
		board = [[0,0,8,7,0,0,0,5,0],[0,3,0,0,1,0,0,9,0],[0,0,0,5,0,0,1,0,0],[4,0,3,0,0,7,0,0,0],[9,7,0,0,0,0,0,1,8],[0,0,0,8,0,0,3,0,9],[0,0,6,0,0,4,0,0,0],[0,9,0,0,8,0,0,2,0],[0,5,0,0,0,1,8,0,0]]
		answer = [[1, 2, 6], [1, 2, 4, 6], [8], [7], [2, 3, 4, 6, 9], [2, 3, 6, 9], [2, 4, 6], [5], [2, 3, 4, 6], [2, 5, 6, 7], [3], [2, 4, 5, 7], [2, 4, 6], [1], [2, 6, 8], [2, 4, 6, 7], [9], [2, 4, 6, 7], [2, 6, 7], [2, 4, 6], [2, 4, 7, 9], [5], [2, 3, 4, 6, 9], [2, 3, 6, 8, 9], [1], [3, 4, 7, 8], [2, 3, 4, 6, 7], [4], [1, 2, 8], [3], [1, 2, 9], [2, 5, 9], [7], [2, 5], [6], [2, 5], [9], [7], [2, 5], [2, 3, 4, 6], [2, 3, 4, 5, 6], [2, 3, 5, 6], [2, 4, 5], [1], [8], [1, 2, 5, 6], [1, 2, 6], [1, 2, 5], [8], [2, 4, 5, 6], [2, 5, 6], [3], [4, 7], [9], [1, 2, 3, 7, 8], [1, 2, 8], [6], [2, 3, 9], [2, 3, 5, 7, 9], [4], [5, 7, 9], [3, 7], [1, 3, 5, 7], [1, 3, 7], [9], [1, 4, 7], [3, 6], [8], [3, 5, 6], [4, 5, 6, 7], [2], [1, 3, 4, 5, 6, 7], [2, 3, 7], [5], [2, 4, 7], [2, 3, 6, 9], [2, 3, 6, 7, 9], [1], [8], [3, 4, 7], [3, 4, 6, 7]]

		csp, var_array = stu_model.sudoku_csp_model_1(board)
		lister = [] 		
		soln_propagators.prop_GAC(csp)
		for i in range(9):
			for j in range(9):
				lister.append(var_array[i][j].cur_domain())

		if lister != answer:
			print("FAILED\nExpected Output: %r\nOutput Received: %r" % (answer,lister))
		else:
			print("PASS")
			score = 2
	except Exception:
		print("Error occurred: %r" % traceback.print_exc())
	print("---finished check_model_1_constraints---\n")
	return score
	
#@max_grade(2)
##Checks that model 1 constraints pass when all different, and fail when not all different
def check_model_2_constraints_enum(stu_models):
	score = 2
	print("---starting check_model_2_constraints_enum---")
	try: 		
		board = [[0,0,8,7,0,0,0,5,0],[0,3,0,0,1,0,0,9,0],[0,0,0,5,0,0,1,0,0],[4,0,3,0,0,7,0,0,0],[9,7,0,0,0,0,0,1,8],[0,0,0,8,0,0,3,0,9],[0,0,6,0,0,4,0,0,0],[0,9,0,0,8,0,0,2,0],[0,5,0,0,0,1,8,0,0]]

		csp, var_array = stu_models.sudoku_csp_model_2(board)

		for cons in csp.get_all_cons():
			all_vars = cons.get_scope()
			taken = [] 
			domain_list = [] 
			should_pass = []
			should_fail = [] 
			for va in all_vars:
				domain_list.append(va.cur_domain())
				if len(va.cur_domain()) == 1:
					taken.append(va.cur_domain()[0])
			for i in range(len(all_vars)):
				va = all_vars[i]
				domain = domain_list[i] 
				if len(domain) == 1:
					should_pass.append(domain[0])
					should_fail.append(domain[0])
				else:
					for i in range(1,10):
						if i in domain and i in taken:
							should_fail.append(i)
							break
					for i in range(1,10):
						if i in domain and i not in taken:
							should_pass.append(i)
							taken.append(i)
							break
			if cons.check(should_fail) != cons.check(should_pass):
				if cons.check(should_fail) or not cons.check(should_pass):
					if not cons.check(should_fail):
						print("FAILED\nConstraint %s should be falsified by %r" % (str(cons),should_fail))
						print("var domains:")
						for va in all_vars:
							print(va.cur_domain())
					if cons.check(should_pass):
						print("FAILED\nConstraint %s should be satisfied by %r" % (str(cons),should_pass))
						print("var domains:")
						for va in all_vars:
							print(va.cur_domain())
					print("---finished check_model_2_constraints_enum---\n")
					return 0

	except Exception:
		print("Error occurred: %r" % traceback.print_exc())
		print("---finished check_model_2_constraints_enum---\n")
		return 0
	
	print("PASS")
	print("---finished check_model_2_constraints_enum---\n")
	return score

#@max_grade(2)
##Checks that model 2 constraints are implemented as expected.
##Both model_2_import must pass and prop_GAC must be implemented correctly for this test to behave as intended.
def check_model_2_constraints(stu_model):
	score = 0
	print("---starting check_model_2_constraints---")
			
	try: 		
		board = [[0,0,8,7,0,0,0,5,0],[0,3,0,0,1,0,0,9,0],[0,0,0,5,0,0,1,0,0],[4,0,3,0,0,7,0,0,0],[9,7,0,0,0,0,0,1,8],[0,0,0,8,0,0,3,0,9],[0,0,6,0,0,4,0,0,0],[0,9,0,0,8,0,0,2,0],[0,5,0,0,0,1,8,0,0]]
		answer = [[1], [4], [8], [7], [2], [9], [6], [5], [3], [6], [3], [5], [4], [1], [8], [2], [9], [7], [7], [2], [9], [5], [6], [3], [1], [8], [4], [4], [8], [3], [1], [9], [7], [5], [6], [2], [9], [7], [2], [3], [5], [6], [4], [1], [8], [5], [6], [1], [8], [4], [2], [3], [7], [9], [8], [1], [6], [2], [7], [4], [9], [3], [5], [3], [9], [4], [6], [8], [5], [7], [2], [1], [2], [5], [7], [9], [3], [1], [8], [4], [6]]

		csp, var_array = stu_model.sudoku_csp_model_2(board)
		lister = [] 		
		soln_propagators.prop_GAC(csp)
		for i in range(9):
			for j in range(9):
				lister.append(var_array[i][j].cur_domain())

		if lister != answer:
			print("FAILED\nExpected Output: %r\nOutput Received: %r" % (answer,lister))
		else:
			print("PASS")
			score = 2
	except Exception:
		print("Error occurred: %r" % traceback.print_exc())
	print("---finished check_model_2_constraints---\n")
	return score

def main(stu_propagators=None, stu_models=None):
	TOTAL_POINTS = 20
	total_score = 0

	import propagators as propagators_soln

	if stu_propagators == None:
		import propagators as stu_propagators
	else:
		import stu_propagators
	if stu_models ==None:
		import sudoku_csp as stu_models
	else:
		import stu_models
	

	total_score += test_simple_FC(stu_propagators)
	total_score += test_simple_GAC(stu_propagators)
	total_score += three_queen_FC(stu_propagators)
	total_score += three_queen_GAC(stu_propagators)
	total_score += model_1_import(stu_models)
	total_score += model_2_import(stu_models)
	total_score += check_model_1_constraints(stu_models)
	total_score += check_model_2_constraints(stu_models)
	total_score += check_model_1_constraints_enum(stu_models)
	total_score += check_model_2_constraints_enum(stu_models)

	if total_score == TOTAL_POINTS:
		print("Score: %d/%d; Passed all tests; Will pass assignment with >= 50pct mark" % (total_score,TOTAL_POINTS))
	else:
		print("Score: %d/%d; Did not pass all tests." % (total_score,TOTAL_POINTS))


if __name__=="__main__":
	main()
