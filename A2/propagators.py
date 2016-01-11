  '''This file will contain different constraint propagators to be used within 
   bt_search.

   propagator == a function with the following template
      propagator(csp, newly_instantiated_variable=None)
           ==> returns (True/False, [(Variable, Value), (Variable, Value) ...]

      csp is a CSP object---the propagator can use this to get access
      to the variables and constraints of the problem. The assigned variables
      can be accessed via methods, the values assigned can also be accessed.

      newly_instaniated_variable is an optional argument.
      if newly_instantiated_variable is not None:
          then newly_instantiated_variable is the most
           recently assigned variable of the search.
      else:
          progator is called before any assignments are made
          in which case it must decide what processing to do
           prior to any variables being assigned. SEE BELOW

       The propagator returns True/False and a list of (Variable, Value) pairs.
       Return is False if a deadend has been detected by the propagator.
       in this case bt_search will backtrack
       return is true if we can continue.

      The list of variable values pairs are all of the values
      the propagator pruned (using the variable's prune_value method). 
      bt_search NEEDS to know this in order to correctly restore these 
      values when it undoes a variable assignment.

      NOTE propagator SHOULD NOT prune a value that has already been 
      pruned! Nor should it prune a value twice

      PROPAGATOR called with newly_instantiated_variable = None
      PROCESSING REQUIRED:
        for plain backtracking (where we only check fully instantiated constraints)
        we do nothing...return true, []

        for forward checking (where we only check constraints with one remaining variable)
        we look for unary constraints of the csp (constraints whose scope contains
        only one variable) and we forward_check these constraints.

        for gac we establish initial GAC by initializing the GAC queue
        with all constaints of the csp


      PROPAGATOR called with newly_instantiated_variable = a variable V
      PROCESSING REQUIRED:
         for plain backtracking we check all constraints with V (see csp method
         get_cons_with_var) that are fully assigned.

         for forward checking we forward check all constraints with V
         that have one unassigned variable left

         for gac we initialize the GAC queue with all constraints containing V.
         
   '''

def prop_BT(csp, newVar=None):
    '''Do plain backtracking propagation. That is, do no 
    propagation at all. Just check fully instantiated constraints'''
    
    if not newVar:
        return True, []
    for c in csp.get_cons_with_var(newVar):
        if c.get_n_unasgn() == 0:
            vals = []
            vars = c.get_scope()
            for var in vars:
                vals.append(var.get_assigned_value())
            if not c.check(vals):
                return False, []
    return True, []

def prop_FC(csp, newVar=None):
    '''Do forward checking. That is check constraints with 
       only one uninstantiated variable. Remember to keep 
       track of all pruned variable,value pairs and return '''
    
#IMPLEMENT
    if not newVar:
        pruned_final_list = []
        for c in csp.get_all_cons():
            if c.get_n_unasgn() == 1:
                unassigned_var = c.get_unasgn_vars()
                pruned_var_value_pairs = forward_check(c, unassigned_var[0])
                pruned_final_list.extend(pruned_var_value_pairs[1])
                if pruned_var_value_pairs[0] == False:
                    return False, pruned_final_list
        return True, pruned_final_list

    else:
        pruned_final_list = []
        for c in csp.get_cons_with_var(newVar):
            if c.get_n_unasgn() == 1:
                unassigned_var = c.get_unasgn_vars()
                pruned_var_value_pairs = forward_check(c, unassigned_var[0])
                pruned_final_list.extend(pruned_var_value_pairs[1])
                if pruned_var_value_pairs[0] == False:
                    return False, pruned_final_list
        return True, pruned_final_list
      
def forward_check(c, x):
    '''C is a constraint with all it's variables already assigned
       except for variable x.'''
    
    pruned_values = list()
    for value in x.cur_domain():
        vals = []
        vars = c.get_scope()
        #index_of_x = vars.index(x)
        for var in vars:
            if var == x:
                vals.append(value)
            else:
                vals.append(var.get_assigned_value())
        if c.check(vals) == False:
            pruned_values.append((x, value))
            x.prune_value(value)
        if x.cur_domain() == []:
            return False, pruned_values

    return True, pruned_values


def prop_GAC(csp, newVar=None):
    '''Do GAC propagation. If newVar is None we do initial GAC enforce 
       processing all constraints. Otherwise we do GAC enforce with
       constraints containing newVar on GAC Queue'''

    if not newVar:
        queue = list()
        pruned_final_list = list()
        for c in csp.get_all_cons():
            queue.insert(0, c)
        pruned_var_value_pairs = enforce_gac(queue, csp)
        pruned_final_list.extend(pruned_var_value_pairs[1])
        if pruned_var_value_pairs[0] == False:
            return False, pruned_final_list
        else:
            return True, pruned_final_list
    else:
        queue = list()
        pruned_final_list = list()
        for c in csp.get_cons_with_var(newVar):
            queue.insert(0, c)
        pruned_var_value_pairs = enforce_gac(queue, csp)
        pruned_final_list.extend(pruned_var_value_pairs[1])
        if pruned_var_value_pairs[0] == False:
            return False, pruned_final_list
        else:
            return True, pruned_final_list

def enforce_gac(queue, csp):

    pruned_pairs = list()
    while queue != []:
        c = queue.pop()
        vars = c.get_scope()
        for var in vars:
            for value in var.cur_domain():
                if (c.has_support(var, value) == False):
                    pruned_pairs.append((var, value))
                    var.prune_value(value)
                    if var.cur_domain() == []:
                        return False, pruned_pairs
                    else:
                        for cons in csp.get_cons_with_var(var):
                            if cons not in queue:
                                queue.insert(0, cons)
    return True, pruned_pairs

    