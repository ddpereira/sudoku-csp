Sudoku Solver via Constraint Satisfaction
-----------------------------------------------------------------

This sudoku solver expresses the puzzle as a constraint satisfaction 
problem. Thus, a solution is found by satisfying a set of contraints
that essentially define a Sudoku puzzle.

AUTHOR
-----------------------------------------------------------------
D. Pereira

MODEL 1 
-----------------------------------------------------------------
	
Creates a variable for each cell of the board, with domain equal 
to {1-9} if the board has a 0 at that position, and domain equal 
{i} if the board has a fixed number i at that cell. 
      
Model 1 creates BINARY CONSTRAINTS OF NOT-EQUAL between all
relevant variables (e.g., all pairs of variables in the same
row), then invokes enforce_gac on those constraints. All of the
constraints of Model_1 are binary constraints (i.e.,
constraints whose scope includes two and only two variables).
       
The ouput has the same layout as the input: a list of
nine lists each representing a row of the board. However, the
numbers in the positions of the input list are replaced by
lists which are the corresponding cell's pruned domain (current
domain) after GAC* has been performed.
	   
MODEL 2
-----------------------------------------------------------------
The variables of model 2 are the same as for model 1: a variable
for each cell of the board, with domain equal to {1-9} if the
board has a 0 at that position, and domain equal {i} if the board
has a fixed number i at that cell.

However, model 2 has different constraints. In particular, instead
of binary non-equals constaints model 2 has 27 ALL-DIFFERENT
constraints: all-different constraints for the variables in each
of the 9 rows, 9 columns, and 9 sub-squares. Each of these
constraints is over 9-variables (some of these variables have
a single value in their domain). Model 2  creates these
all-different constraints between the relevant variables, then
invoke enforce_gac* on those constraints.
	

*GAC: A variable x is generalized arc consistent (GAC) with a 
constraint if every value of the variable can be extended to 
all the other variables of the constraint in such a way the 
constraint is satisfied





