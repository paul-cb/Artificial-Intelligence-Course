from bnet import *
import itertools

#Note: The tests here are NOT Comprehensive
#
#Helper function to reorder a factor's scope---produces a new factor.
#depends on the variables in the scope having names.
#Generates a new factor equivalent to the input factor f but with
#the scope ordered according to the list "scope_names" 
def reorder_factor_scope(f, scope_names):
    #get variables in order of scope_names
    d = dict()
    vdoms = []
    nscope = []
    for v in f.get_scope():
        d[v.name] = v
        vdoms.append(v.domain())
    for name in scope_names:
        nscope.append(d[name])
    nfactor = Factor(f.name, nscope)
    for t in itertools.product(*vdoms):
        for i, var in enumerate(f.get_scope()):
            var.set_assignment(t[i])
        nfactor.add_value_at_current_assignment(f.get_value_at_current_assignments())
    return nfactor

#Helper function to test the equality of two scopes given that the variables in the
#scope lists might be ordered differently.
def scopesEquiv(s1, s2):
    #s1 and s2 are lists of variables.
    return set(s1) == set(s2)
    
#maximum difference allowed between equivalent values
epsilon = 0.0001

#Helper function for testing.  Compares the probability table of a factor against expected results.
#Returns a two element list. Element 0 is the number of mismatches.  Element 1 is a string documenting the mismatches.

def comparetable(factor, values):

    outstring = ""
    counter = 0
    
    for i in range(0,len(values)):

        if(abs(factor.values[i] - values[i]) > epsilon):
            counter += 1
            outstring += derankmismatch(factor,i) + " : Expected Value={} Actual Value={}".format(values[i],factor.values[i]) + '\n'

    return [counter, outstring]

#Helper Function for testing.  Given a factor and an index with respect to the factor.values list, returns a string
#corresponding to the variable assignment associated with that index
def derankmismatch(factor, index):

    outstr = "P("
    
    value = index
    scope = factor.get_scope()

    variableindex = []
    
    for v in reversed(scope):
        
        variableindex.append(int(value % v.domain_size()))        
        value = int(value / v.domain_size())
       
    variableindex = list(reversed(variableindex))

    for i in range(0, len(scope)):    
        outstr += ("{} = {},".format(scope[i].name, scope[i].dom[variableindex[i]]))
    
    return outstr[:-1] + ")"


#Helper function for testing purposes.  Not necessary.
def scopefilter(scope):
    ret = []
    for i in scope:
        ret.append(repr(i))       
    return ret

#Factor Restriction Test Class
class RestrictionTest:

    #Factor is the factor to restrict such that variable = value
    def __init__(self, factor, variable, value, answer, points, name="factor restriction test"):
        self.name = name
        self.factor = factor
        self.variable = variable
        self.value = value
        self.answer = answer
        self.points = points


    def test(self):
        #answer[0] : the desired scope
        #answer[1] : the desired table values                

        print("\nRunning Test : {}".format(self.name))
        mark = 0
        result = restrict_factor(self.factor, self.variable, self.value)
        scopetest = scopesEquiv(self.answer[0],scopefilter(result.get_scope()))
        if(scopetest):
            print("\t[+] Scope of the resulting factor matches expected result")
        else:
            print("\t[!] Scope of the resulting factor does not match expected result : ")
            print("\t\tExpected: " + repr(self.answer[0]))            
            print("\t\tActual:  " + repr(scopefilter(result.get_scope())))
        if(scopetest):
            result = reorder_factor_scope(result, self.answer[0])
            tabletest = comparetable(result, self.answer[1])
            copytest = id(result) != id(self.factor)
            if(tabletest[0] == 0):
                print("\t[+] Factor values match the expected result in all cases")
                if copytest:
                    mark = self.points
                    print("\t[+] [{}/{}]".format(mark, self.points))
                else:
                    print("\t[+] input factor was changed")
            else:
                print("\t[!] Factor values mismatch the expected result in {} place{}:\n".format(tabletest[0], "" if (tabletest[0] == 1) else "s"))
                print(tabletest[1])        
        return mark, self.points
                
        
#Factor Variable Sum Out Test Class
class SummationTest:
    #factor is the factor to sum over, variable is the variable to sum out
    def __init__(self, factor, variable, answer, points, name="sum out variable test"):
        #answer[0] : the desired scope
        #answer[1] : the desired table values                
        self.name = name
        self.factor = factor
        self.variable = variable
        self.answer = answer
        self.points = points

    def test(self):
        print("\nRunning Test : {}".format(self.name))
        result = sum_out_variable(self.factor, self.variable)
        scopetest = scopesEquiv(self.answer[0],scopefilter(result.get_scope()))
        mark = 0
        if(scopetest):
            print("\t[+] Scope of the resulting factor matches expected result")
        else:
            print("\t[!] Scope of the resulting factor does not match expected result : ")
            print("\t\tExpected: " + repr(self.answer[0]))            
            print("\t\tActual:  " + repr(scopefilter(result.get_scope())))
                        
        if(scopetest):
            result = reorder_factor_scope(result, self.answer[0])
            tabletest = comparetable(result, self.answer[1])
            copytest = id(result) != id(self.factor)
            if(tabletest[0] == 0):
                print("\t[+] Factor values match the expected result in all cases")
                if(copytest):
                    mark = self.points
                    print("\t[+] [{}/{}]".format(mark, self.points))
                else:
                    print("\t[+] input factor was changed")
            else:
                print("\t[!] Factor values mismatch the expected result in {} place{}:\n".format(tabletest[0], "" if (tabletest[0] == 1) else "s"))
                print(tabletest[1])        
            
        return mark, self.points
                
#Factor Multiplication Test Class
class MultiplyTest:
    #factors is a list of factors to multiply
    def __init__(self, factors, answer,points, name="factor multiplication test"):
        self.name = name
        self.factors = factors
        self.answer = answer
        self.points = points
                 
                 
    def test(self):
        #answer[0] : the desired scope
        #answer[1] : the desired table values                
        print("\nRunning Test : {}".format(self.name))
        mark = 0
        result = multiply_factors(self.factors)                        
        scopetest = scopesEquiv(self.answer[0],scopefilter(result.get_scope()))
        if(scopetest):
            print("\t[+] Scope of the resulting factor matches expected result")
        else:
            print("\t[!] Scope of the resulting factor does not match expected result : ")
            print("\t\tExpected: " + repr(self.answer[0]))            
            print("\t\tActual:  " + repr(scopefilter(result.get_scope())))

        if(scopetest):
            result = reorder_factor_scope(result, self.answer[0])
            tabletest = comparetable(result, self.answer[1])
            if(tabletest[0] == 0):
                print("\t[+] Factor values match the expected result in all cases")
                copytest = id(result) != id(self.factors)
                if(copytest):
                    mark = self.points
                    print("\t[+] [{}/{}]".format(mark, self.points))
                else:
                    print("\t[+] input factor was changed")
            else: 
                print("\t[!] Factor values mismatch the expected result in {} place{}:\n".format(tabletest[0], "" if (tabletest[0] == 1) else "s"))
                print(tabletest[1])        
            
        return mark, self.points

#Variable Elimination Test Class    
class VETest:


    #net is the bayes net, evidence is a list of pairs of the form [variable, value]
    def __init__(self, net, evidence, queryVariable, answer, points, name="variable elimination test"):
        self.name = name
        self.net = net
        self.evidence = evidence
        self.queryVariable = queryVariable
        self.answer = answer
        self.points = points

        self.evidenceVars = []
        
        for i in self.evidence:
            i[0].set_evidence(i[1])
            self.evidenceVars.append(i[0])
                         
    def test(self):
        #answer[0] : a list of probabilities for the values for queryVariable
        mark = 0
        for i in self.evidence:
            i[0].set_evidence(i[1])
        result = VE(self.net, self.queryVariable, self.evidenceVars)                 

        querytest = True 

        for i in range(0,len(self.answer[0])):
            if( abs(self.answer[0][i] - result[i]) > epsilon):
                querytest = False        

        print("\nRunning Test : {}".format(self.name))

        
        
        if(querytest):
            print("\t[+] Probability distribution of the query variable matches the expected results")
            mark = self.points
            print("\t[+] [{}/{}]".format(mark, self.points))
        else:
            print("\t[!] Probability distribution of the query variable does not match the expected results : ")
            print("\t\tExpected: " + repr(self.answer[0]))            
            print("\t\tActual:  " + repr(result))

        return mark, self.points


    #Test functions for extracting the answer
    #def getanswer(self):
    #    for i in self.evidence:
    #        i[0].set_evidence(i[1])
    #    result = VE(self.net, self.queryVariable, self.evidenceVars)                 

    #    self.answer = [result]
                
    #def printanswer(self):
    #    outstr = repr(self.answer)         
    #    print(outstr)
        
if __name__ == '__main__':
    

    #Example Bayes Net
    VisitAsia = Variable('Visit_To_Asia', ['visit', 'no-visit'])
    F1 = Factor("F1", [VisitAsia])
    F1.add_values([['visit', 0.01], ['no-visit', 0.99]])
    
    Smoking = Variable('Smoking', ['smoker', 'non-smoker'])
    F2 = Factor("F2", [Smoking])
    F2.add_values([['smoker', 0.5], ['non-smoker', 0.5]])

    Tuberculosis = Variable('Tuberculosis', ['present', 'absent'])
    F3 = Factor("F3", [Tuberculosis, VisitAsia])
    F3.add_values([['present', 'visit', 0.05],
                   ['present', 'no-visit', 0.01],
                   ['absent', 'visit', 0.95],
                   ['absent', 'no-visit', 0.99]])

    Cancer = Variable('Lung Cancer', ['present', 'absent'])
    F4 = Factor("F4", [Cancer, Smoking])
    F4.add_values([['present', 'smoker', 0.10],
                   ['present', 'non-smoker', 0.01],
                   ['absent', 'smoker', 0.90],
                   ['absent', 'non-smoker', 0.99]])

    Bronchitis = Variable('Bronchitis', ['present', 'absent'])
    F5 = Factor("F5", [Bronchitis, Smoking])
    F5.add_values([['present', 'smoker', 0.60],
                   ['present', 'non-smoker', 0.30],
                   ['absent', 'smoker', 0.40],
                   ['absent', 'non-smoker', 0.70]])

    TBorCA = Variable('Tuberculosis or Lung Cancer', ['true', 'false'])
    F6 = Factor("F6", [TBorCA, Tuberculosis, Cancer])
    F6.add_values([['true', 'present', 'present', 1.0],
                   ['true', 'present', 'absent', 1.0],
                   ['true', 'absent', 'present', 1.0],
                   ['true', 'absent', 'absent', 0],
                   ['false', 'present', 'present', 0],
                   ['false', 'present', 'absent', 0],
                   ['false', 'absent', 'present', 0],
                   ['false', 'absent', 'absent', 1]])


    Dyspnea = Variable('Dyspnea', ['present', 'absent'])
    F7 = Factor("F7", [Dyspnea, TBorCA, Bronchitis])
    F7.add_values([['present', 'true', 'present', 0.9],
                   ['present', 'true', 'absent', 0.7],
                   ['present', 'false', 'present', 0.8],
                   ['present', 'false', 'absent', 0.1],
                   ['absent', 'true', 'present', 0.1],
                   ['absent', 'true', 'absent', 0.3],
                   ['absent', 'false', 'present', 0.2],
                   ['absent', 'false', 'absent', 0.9]])


    Xray = Variable('XRay Result', ['abnormal', 'normal'])
    F8 = Factor("F8", [Xray, TBorCA])
    F8.add_values([['abnormal', 'true', 0.98],
                   ['abnormal', 'false', 0.05],
                   ['normal', 'true', 0.02],
                   ['normal', 'false', 0.95]])

    Asia = BN("Asia", [VisitAsia, Smoking, Tuberculosis, Cancer,
                       Bronchitis, TBorCA, Dyspnea, Xray],
              [F1, F2, F3, F4, F5, F6, F7, F8])


    #This factor is for testing purposes only
    V1 = Variable('Colour', ['Red','Blue'])
    V2 = Variable('Distance', ['Close','Far'])
    V3 = Variable('Temperature', ['Cold','Hot'])
    F9 = Factor("F9", [V1,V2,V3])
    F9.add_values([['Red', 'Close', 'Cold', 0.3],
                   ['Red', 'Close', 'Hot', 0.05],
                   ['Red', 'Far', 'Cold', 0],
                   ['Red', 'Far', 'Hot', 0.2],
                   ['Blue', 'Close', 'Cold', 0.1],
                   ['Blue', 'Close', 'Hot', 0.15],
                   ['Blue', 'Far', 'Cold', 0.05],
                   ['Blue', 'Far', 'Hot',0.05]])


    #Based on the example from Russel and Norvig, Artificial Intelligence: A Modern Approach, 3rd Edition, Figure 14.2, Pg 512
    Burglary = Variable('Burglary', [True, False])
    Earthquake = Variable('Earthquake', [True, False])
    Alarm = Variable('Alarm', [True, False])
    John = Variable('John Calls', [True, False])
    Mary = Variable('Mary Calls', [True, False])

    F10 = Factor("F10", [Burglary])
    F10.add_values([[True,  0.001],
                    [False, 0.999]])

    F11 = Factor("F11", [Earthquake])
    F11.add_values([[True,  0.002],
                    [False, 0.998]])


    
    F12 = Factor("F12", [Burglary, Earthquake, Alarm])
    F12.add_values([[True, True, True, .95],
                    [True, True, False, .05],
                    [True, False, True, .94],
                    [True, False, False, .06],
                    [False, True, True, .29],
                    [False, True, False, .71],
                    [False, False, True, .001],
                    [False, False, False, .999]])


    F13 = Factor("F13", [Alarm, John])
    F13.add_values([[True, True, .90],
                    [True, False, .10],
                    [False, True, .05],
                    [False, False, .95]])


    F14 = Factor("F14", [Alarm, Mary])
    F14.add_values([[True, True, .70],
                    [True, False, .30],
                    [False, True, .01],
                    [False, False, .99]])

    AlarmNet = BN("Home Alarm", [Burglary, Earthquake, Alarm, John, Mary], [F10, F11, F12, F13, F14])


    #The current list of tests
    t1 = RestrictionTest(F8, TBorCA, 'false', [['XRay Result',],[0.05,0.95]], 3, "Factor Restriction Test 1")
    t2 = RestrictionTest(F9, V1, 'Blue', [['Distance','Temperature',],[0.1, 0.15, 0.05, 0.05]], 3, "Factor Restriction Test 2")
    t3 = RestrictionTest(F9, V2, 'Close', [['Colour','Temperature',],[0.3, 0.05, 0.1, 0.15]], 2, "Factor Restriction Test 3")
    #    t4 = RestrictionTest(F9, V3, 'Cold', [['Colour','Distance',],[0.3, 0, 0.1, 0.05]], 3, "Factor Restriction Test 4")

    t5 = SummationTest(F6,Cancer,[['Tuberculosis or Lung Cancer','Tuberculosis',],[2.0, 1.0, 0, 1]], 4, "Factor Sum Out Test 1")
    t6 = SummationTest(F9,V1,[['Distance','Temperature',],[0.4, 0.2, 0.05, 0.25]], 4, "Factor Sum Out Test 2")
    t7 = SummationTest(F9,V2,[['Colour','Temperature',],[0.3, 0.25, 0.15000000000000002, 0.2]], 4, "Factor Sum Out Test 3")
    #    t8 = SummationTest(F9,V3,[['Colour','Distance',],[0.35, 0.2, 0.25, 0.1]], 4, "Factor Sum Out Test 4")


    t9 = MultiplyTest([F4,F5,F7],[['Lung Cancer','Smoking','Bronchitis','Dyspnea','Tuberculosis or Lung Cancer',],[0.054, 0.048, 0.006, 0.012, 0.028000000000000004, 0.004000000000000001, 0.012000000000000002, 0.03600000000000001, 0.0027, 0.0024000000000000002, 0.00030000000000000003, 0.0006000000000000001, 0.004899999999999999, 0.0007, 0.0021, 0.006299999999999999, 0.48600000000000004, 0.43200000000000005, 0.054000000000000006, 0.10800000000000001, 0.252, 0.036000000000000004, 0.10800000000000001, 0.32400000000000007, 0.2673, 0.2376, 0.0297, 0.0594, 0.4850999999999999, 0.0693, 0.20789999999999997, 0.6236999999999999]], 5, "Factor Multiplication Test 1")
    t10 = MultiplyTest([F2,F5,F7],[['Smoking','Bronchitis','Dyspnea','Tuberculosis or Lung Cancer',],[0.27, 0.24, 0.03, 0.06, 0.13999999999999999, 0.020000000000000004, 0.06, 0.18000000000000002, 0.135, 0.12, 0.015, 0.03, 0.24499999999999997, 0.034999999999999996, 0.105, 0.315]], 5, "Factor Multiplication Test 2")
    t11 = MultiplyTest([F6,F7,F8],[['Tuberculosis or Lung Cancer','Tuberculosis','Lung Cancer','Dyspnea','Bronchitis','XRay Result',],[0.882, 0.018000000000000002, 0.6859999999999999, 0.013999999999999999, 0.098, 0.002, 0.294, 0.006, 0.882, 0.018000000000000002, 0.6859999999999999, 0.013999999999999999, 0.098, 0.002, 0.294, 0.006, 0.882, 0.018000000000000002, 0.6859999999999999, 0.013999999999999999, 0.098, 0.002, 0.294, 0.006, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.04000000000000001, 0.76, 0.005000000000000001, 0.095, 0.010000000000000002, 0.19, 0.045000000000000005, 0.855]], 5, "Factor Multiplication Test 3")
    #    t12 = MultiplyTest([F2,F4,F5],[['Smoking','Lung Cancer','Bronchitis',],[0.03, 0.020000000000000004, 0.27, 0.18000000000000002, 0.0015, 0.0034999999999999996, 0.1485, 0.3465]], 5, "Factor Multiplication Test 4")

    t13= VETest(Asia,[[Smoking,'smoker'], [Dyspnea,'present'], [Xray,'abnormal']],Cancer,[[0.7237140153108922, 0.27628598468910776]], 5, "Variable Elimination Test 1")
    t14 = VETest(Asia,[[VisitAsia,'visit'], [TBorCA,'true'], [Xray,'abnormal']],Cancer,[[0.5378973105134475, 0.4621026894865526]], 5, "Variable Elimination Test 2")
    t15 = VETest(AlarmNet,[[John, True], [Mary, False]],Earthquake,[[0.0045386400007529125, 0.9954613599992471]], 5, "Variable Elimination Test 3")
    #t16 = VETest(AlarmNet,[[John, False], [Mary, False], [Earthquake, True]],Alarm,[[0.012901897594550255, 0.9870981024054498]], 5, "Variable Elimination Test 4")
    #t17 = VETest(AlarmNet,[[Burglary, False], [Mary, True], [Earthquake, False]],John,[[0.10565949485500468, 0.8943405051449953]], 5, "Variable Elimination Test 5")

    
    mark = 0
    outof = 0

    m,o = t1.test()
    mark += m
    outof += o

    m,o = t2.test()
    mark += m
    outof += o

    m,o = t3.test()
    mark += m
    outof += o

    #m,o = t4.test()
    #mark += m
    #outof += o

    m,o = t5.test()
    mark += m
    outof += o

    m,o = t6.test()
    mark += m
    outof += o

    m,o = t7.test()
    mark += m
    outof += o

    #m,o = t8.test()
    #mark += m
    #outof += o

    m,o = t9.test()
    mark += m
    outof += o

    m,o = t10.test()
    mark += m
    outof += o

    m,o = t11.test()
    mark += m
    outof += o

    #m,o = t12.test()
    #mark += m
    #outof += o

    m,o = t13.test()
    mark += m
    outof += o

    m,o = t14.test()
    mark += m
    outof += o

    m,o = t15.test()
    mark += m
    outof += o

    #m,o = t16.test()
    #mark += m
    #outof += o

    #m,o = t17.test()
    #mark += m
    #outof += o

    print("Mark on student tests = {}/{}".format(mark, outof))
    
