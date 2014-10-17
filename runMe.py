# Import the Solver class
from Solver import *

# Ask for file path
satFile = raw_input("Enter path to CNF file: ")


# Create a SAT problem to solve
x = Solver(satFile)

# Now solve the SAT problem (finding all solutions)
solutions = x.simpleSolveAll()

# Print out all solutions
print "Solutions:\n", solutions
