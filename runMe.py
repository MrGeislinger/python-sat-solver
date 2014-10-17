# Import the Solver class
from Solver import *

# Create a SAT problem to solve
x = Solver('data/ex1.cnf')

# Now solve the SAT problem (finding all solutions)
solutions = x.simpleSolveAll()

# Print out all solutions
print "Solutions:\n", solutions
