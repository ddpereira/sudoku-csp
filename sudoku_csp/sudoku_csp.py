'''	Author: D. Pereira
'''

from cspbase import *
import itertools 


def enforce_gac(constraint_list):
    '''Input a list of constraint objects, each representing a constraint, then 
       enforce GAC on them pruning values from the variables in the scope of
       these constraints. Return False if a DWO is detected. Otherwise, return True. 
       The pruned values will be reflected in the variable object cur_domain (i.e.,
       enforce_gac will modify the variable objects that are in the scope of
       the constraints passed to it.'''
    
    Q = []
    
    #initially, queue contains all the constraints
    for n in constraint_list: 
        Q.append(n)
    
    while len(Q) > 0:
        #consider the first constraint on the queue
        C = Q.pop(0)
                            
        for V in C.scope:
            for d in V.cur_domain():
                
                #if d in fixed:
                if not C.has_support(V, d):
                    #prune this domain value of the variable,
                    #since it cannot lead to a solution
                    V.prune_value(d)
                    
                    if V.cur_domain() == []:
                        #domain wipe out
                        return False
                    else:
                        #enqueue relevant constraints
                        Q = GAC_enq(constraint_list, Q, V)                        
                
    return True
     
#GAC enforce helper method           
def GAC_enq(cList, Q, V):
    '''Given cList (the list of all constraints), Q (a queue of constraints,
    a subset of cList), and a variable V, enqueue every contraint containing 
    variable V into Q'''
    
    for C in cList:
        if (V in C.scope) and (not(C in Q)):
            Q.append(C)
            
    return Q

def sudoku_enforce_gac_model_1(initial_sudoku_board):
    '''The input board is specified as a list of 9 lists. Each of the
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
       
       
       In model_1, create a variable for each cell of the
       board, with domain equal to {1-9} if the board has a 0 at that
       position, and domain equal {i} if the board has a fixed number i
       at that cell. 
       
       Model_1 creates BINARY CONSTRAINTS OF NOT-EQUAL between all
       relevant variables (e.g., all pairs of variables in the same
       row), then invokes enforce_gac on those constraints. All of the
       constraints of Model_1 are binary constraints (i.e.,
       constraints whose scope includes two and only two variables).
       
       The ouput has the same layout as the input: a list of
       nine lists each representing a row of the board. However, the
       numbers in the positions of the input list are replaced by
       lists which are the corresponding cell's pruned domain (current
       domain) after gac has been performed.
       
       For example, if GAC failed to prune any values the output from
       the above input would result in an output would be: NOTE python 
	   could not output this list of lists in the intended padded format...
       
       
       [[[1,2,3,4,5,6,7,8,9],[1,2,3,4,5,6,7,8,9],[                2],[1,2,3,4,5,6,7,8,9],[                9],[1,2,3,4,5,6,7,8,9],[1,2,3,4,5,6,7,8,9],[                6],[1,2,3,4,5,6,7,8,9]],
       [[1,2,3,4,5,6,7,8,9],[                4],[1,2,3,4,5,6,7,8,9],[1,2,3,4,5,6,7,8,9],[1,2,3,4,5,6,7,8,9],[                1],[1,2,3,4,5,6,7,8,9],[1,2,3,4,5,6,7,8,9],[                8]],
       [[1,2,3,4,5,6,7,8,9],[                7],[1,2,3,4,5,6,7,8,9],[                4],[                2],[1,2,3,4,5,6,7,8,9],[1,2,3,4,5,6,7,8,9],[1,2,3,4,5,6,7,8,9],[                3]],
       [[                5],[1,2,3,4,5,6,7,8,9],[1,2,3,4,5,6,7,8,9],[1,2,3,4,5,6,7,8,9],[1,2,3,4,5,6,7,8,9],[1,2,3,4,5,6,7,8,9],[                3],[1,2,3,4,5,6,7,8,9],[1,2,3,4,5,6,7,8,9]],
       [[1,2,3,4,5,6,7,8,9],[1,2,3,4,5,6,7,8,9],[                1],[1,2,3,4,5,6,7,8,9],[                6],[1,2,3,4,5,6,7,8,9],[                5],[1,2,3,4,5,6,7,8,9],[1,2,3,4,5,6,7,8,9]],
       [[1,2,3,4,5,6,7,8,9],[1,2,3,4,5,6,7,8,9],[                3],[1,2,3,4,5,6,7,8,9],[1,2,3,4,5,6,7,8,9],[1,2,3,4,5,6,7,8,9],[1,2,3,4,5,6,7,8,9],[1,2,3,4,5,6,7,8,9],[                6]],
       [[                1],[1,2,3,4,5,6,7,8,9],[1,2,3,4,5,6,7,8,9],[1,2,3,4,5,6,7,8,9],[                5],[                7],[1,2,3,4,5,6,7,8,9],[                4],[1,2,3,4,5,6,7,8,9]],
       [[                6],[1,2,3,4,5,6,7,8,9],[1,2,3,4,5,6,7,8,9],[                9],[1,2,3,4,5,6,7,8,9],[1,2,3,4,5,6,7,8,9],[1,2,3,4,5,6,7,8,9],[                2],[1,2,3,4,5,6,7,8,9]],
       [[1,2,3,4,5,6,7,8,9],[                2],[1,2,3,4,5,6,7,8,9],[1,2,3,4,5,6,7,8,9],[                8],[1,2,3,4,5,6,7,8,9],[                1],[1,2,3,4,5,6,7,8,9],[1,2,3,4,5,6,7,8,9]]]
       
       Of course, GAC would prune some variable domains so this would
       not be the outputted list.
       
       '''
    #generate all 81 variables for each cell on the board
    variables = make_variables(initial_sudoku_board)       
    
    #first, create lists of variables for the variables in the same column 
    #and box, for easier simplification
    boxes = group_boxes(variables)
    cols = group_cols(variables)

    #GENERATE THE CONSTRAINTS:
  
    constraints = []
    checker = [] #will help ignore redundant constraints
                     #eg. if a row constraint exists between (v1, v2),
                     #then we don't need a col/box constraint for them as well
             
    #binary row constraints
    for r in variables:
        for c1 in r:
            for c2 in r[r.index(c1) + 1:]:
                #no need for checker here, because there are no constraints yet
                cons = Constraint("BIN-ROW: (R" + str(variables.index(r)) + \
                                  ", C" + str(r.index(c1)) +") and (R" + str(variables.index(r)) + \
                                  ", C" + str(r.index(c2)) + ")", [c1, c2])
                    
                cons.add_satisfying_tuples(binary_permutations(c1, c2))
                constraints.append(cons)
                checker.append((c1, c2))
    
    #binary col constraints
    for r in cols:
        for c1 in r:
            for c2 in r[r.index(c1) + 1:]:
                if (c1, c2) not in checker:
                    cons = Constraint("BIN-COL: (R" + str(cols.index(r)) + \
                                  ", C" + str(r.index(c1)) +") and (R" + str(cols.index(r)) + \
                                  ", C" + str(r.index(c2)) + ")", [c1, c2]) 
                    cons.add_satisfying_tuples(binary_permutations(c1, c2))
                    constraints.append(cons)
                    checker.append((c1, c2))
                                        
    #binary box constraints
    for r in boxes:
        for c1 in r:
            for c2 in r[r.index(c1) + 1:]:
                if (c1, c2) not in checker:
                    cons = Constraint("BIN-BOX: (R" + str(boxes.index(r)) + \
                                  ", C" + str(r.index(c1)) +") and (R" + str(boxes.index(r)) + \
                                  ", C" + str(r.index(c2)) + ")", [c1, c2]) 
                    cons.add_satisfying_tuples(binary_permutations(c1, c2))
                    constraints.append(cons)
                    checker.append((c1, c2))                       
                
                
    #ENFORCE GAC on these contraints:
    result_list = [[], [], [], [], [], [], [], [], []]
    
    e = enforce_gac(constraints)
    
    #results_list will contain the updated domain values (in the case of a DWO,
    #some variable domains will be empty
    for r in variables:
        for c in r:
            result_list[variables.index(r)].append(c.cur_domain())
        
    return result_list       

##############################

def sudoku_enforce_gac_model_2(initial_sudoku_board):
    '''This function takes the same input format (a list of 9 lists
    specifying the board, and generates the same format output as
    sudoku_enforce_gac_model_1.
    
    The variables of model_2 are the same as for model_1: a variable
    for each cell of the board, with domain equal to {1-9} if the
    board has a 0 at that position, and domain equal {i} if the board
    has a fixed number i at that cell.

    However, model_2 has different constraints. In particular, instead
    of binary non-equals constaints model_2 has 27 all-different
    constraints: all-different constraints for the variables in each
    of the 9 rows, 9 columns, and 9 sub-squares. Each of these
    constraints is over 9-variables (some of these variables have
    a single value in their domain). model_2 should create these
    all-different constraints between the relevant variables, then
    invoke enforce_gac on those constraints.
    '''
    variables = make_variables(initial_sudoku_board)       
    
    #first, create lists of variables for variables in the same column 
    #and box, for easier accessing
    boxes = group_boxes(variables)
    cols = group_cols(variables)    
       
    #GENERATE THE CONSTRAINTS: 
  
    constraints = []
    perms = list(itertools.permutations(range(10)[1:])) #all permutations of satisfying
                                                        #tuples for 9 variables
             
    #all-diff row constraints
    for r in variables:
        cons = Constraint("ALLDIFF-ROW: R" + str(variables.index(r)), r)                    
        cons.add_satisfying_tuples(alldif_permutations(r, perms))
        constraints.append(cons)
    
    #all-diff col constraints
    for c in cols:
        cons = Constraint("ALLDIFF-COL: C" + str(cols.index(c)), c) 
        cons.add_satisfying_tuples(alldif_permutations(c, perms))
        constraints.append(cons)
                                        
    #all-diff box constraints
    for b in boxes:
        cons = Constraint("ALLDIFF-BOX: B" + str(boxes.index(b)), b) 
        cons.add_satisfying_tuples(alldif_permutations(b, perms))
        constraints.append(cons)
                                                  
                
    #ENFORCE GAC on the constraints:
    result_list = [[], [], [], [], [], [], [], [], []]
    
    e = enforce_gac(constraints)
    
    #results_list will contain the updated domain values (in the case of a DWO,
    #some variable domains will be empty
    for r in variables:
        for c in r:
            result_list[variables.index(r)].append(c.cur_domain())
        
    return result_list       

##############################

#Helper functions

def group_cols(variables):
    '''Given the sudoku board representation, group the variables that belong 
     to the same column'''
    temp = range(9)
    
    cols = [[], [], [], [], [], [], [], [], []]
    
    for i in temp:
        for j in temp:
            cols[i].append(variables[j][i])
            
    return cols
         
def group_boxes(variables):
    '''Given the sudoku board representation, group the variables that belong 
    to the same box'''
    temp = range(9)
            
    boxes = [[], [], [], [], [], [], [], [], []]
              
    for h in temp[0:3]:
        for i1 in temp[0:3]:
            boxes[0].append(variables[h][i1])
        for j1 in temp[3:6]:
            boxes[1].append(variables[h][j1])
        for k1 in temp[6:9]:
            boxes[2].append(variables[h][k1])
        
        for i2 in temp[0:3]:
            boxes[3].append(variables[h+3][i2])
        for j2 in temp[3:6]:
            boxes[4].append(variables[h+3][j2])
        for k2 in temp[6:9]:
            boxes[5].append(variables[h+3][k2])
    
        for i3 in temp[0:3]:
            boxes[6].append(variables[h+6][i3])
        for j3 in temp[3:6]:
            boxes[7].append(variables[h+6][j3])
        for k3 in temp[6:9]:
            boxes[8].append(variables[h+6][k3])
            
    return boxes
                  
def make_variables(board):
    '''Given a list of lists representing each cell in a sudoku board, generate 
    variables for each cell of the board'''
    
    variables = []
    for i in range(9): variables.append([])
    
    #set up 81 variables, one for each cell on the board
    for row in board:
        for col in row:
            V = Variable("CELL(" + str(board.index(row)) + ", " + str(col) + ")")
                                    
            if col == 0:
                V.add_domain_values(range(10)[1:])
            else:
                V.add_domain_values([col])
            
            variables[board.index(row)].append(V)
        
    return variables

def binary_permutations(V1, V2):
    '''Given two variables, compute the satisfying tuples for the two variables 
    that satisfy a binary not-equals constraint (ie. all combinations (n, m) of 
    values in the domains of the V1 and V2 such that n != m)'''
    L = []
    for n in V1.domain():
        for m in V2.domain():
            if n != m:
                L.append([n, m])
    
    return L

def alldif_permutations(V, perms):
    '''Given a list of (9) variables, and all permutations of their satisfying tuples,
    compute the satisfying tuples for the variables such that they satisfy an 
    all-diff constraint'''
    
    fixed = [] #will keep track of all variables with a single domain value
    L = []
    
    for v in V:
        if len(v.cur_domain()) == 1:
            fixed.append((V.index(v), v.cur_domain()[0]))
            #append (index, value)
            
    #after the following loop, L will contain all permutations of satisfying 
    #tuples where the fixed values match up (ie. ignores all others)
    for p in perms:
        test = True
        for f in fixed:
            if p[f[0]] != f[1]:
                test = False
                break
        
        #if the permutation contains the correct fixed values, take it
        if (test): L.append(p)
        
    return L
