#
from SAT import *

# Solver object to preform operations on the SAT object
class Solver(object):
    '''
    '''
     
    # Constructor by using data file
    def __init__(self,dataFile):
        #
        self.SAT = SAT.initFromFile(dataFile)
        # Create SAT object from data file
        #self.SAT = .initFromFile(dataFile)
        # Assignment of truth values (0,1=True,False) for SAT object
        self.assignment = {}
        # Lambda function to map only ints in SAT.varDict to assignment 
        isInt = lambda x : x if isinstance(x,int) else False
        # Iterate over just the int keys from SAT.varDict
        for var in map(isInt,self.SAT.varDict.keys()):
            # Initiate each variable assignment with no assignment (None)
            self.assignment[var] = None

    # Assign assignment varaible a truth value
    #
    # Input: (int) var, (None,0,1) truthValue
    def assignVar(self,var,truthValue):
        self.assignment[var] = truthValue

    # Check if assignment has solved SAT object
    def isSolved(self):
        # Some variables are not yet assigned
        if None in self.assignment.values():
            return False
        # Check the all clauses to see if assignment is consistent
        for clause in self.SAT.clauses:
            # Return False if any clause is inconsistent with assignment
            if not self.isClauseConsistent(clause):
                return False
        # All clauses passed the check so SAT object is solved 
        return True 

    # Check that the clause is consistent with assignment
    def isClauseConsistent(self,clause):
        #
        isTrue = 0 # Only greater than 0 if at least a one literal is true
        for literal in clause:
            # Get variable from literal
            var = self.SAT.getVar(literal)
            # Assignment is None, 0 (False) or 1 (True)
            value = self.assignment[var]
            # Check that variable has been assigned
            if value == None:
            	return False
            # Add value assigned to testing sum (isTrue)
            else:
                # Negate value if literal in clause is negated
            	isTrue += value ^ self.SAT.isNeg(literal) #bitwise-XOR
        # Test if at least one literal evaluated is True (1)
        return True if (isTrue > 0) else False

    # Create a watchlist to make algorithms simple
    def createWatchlist(self):
        # Creat a 2*numOfVars sized watchlist of empty lists
        self.watchlist = [ [] for i in range(2*self.SAT.numOfVars) ]
        # Watch the first literal in each clause
        for clause in self.SAT.clauses:
            self.watchlist[ list(clause)[0] ].append(clause) #clause set to list

    # Updates the watchlist 
    def updateWatchlist(self,falseLiteral):
		# Loop until there's nothing in list of clauses watching this literal
        foundAlt = False
        while self.watchlist[falseLiteral]:
            clause = self.watchlist[falseLiteral][0] #get first watched clause
            # Default to say no alternative was found
            foundAlt = False
            # Look for alternative literal for the clause to watch           
            for alt in clause:
            	# Get the variable and negation piece of the literal in clause
                v = self.SAT.getVar(alt)
                a = self.SAT.isNeg(alt)
                # Get the current assignment of this variable
                varAssignment = self.assignment[v]
                # See that the newly watched literal has the correct property
                # The variable assignment is None or evaluates to True (1)
                if varAssignment is None or varAssignment == self.SAT.negate(a):
                    foundAlt = True
                    # Get rid of this clause since literal is now True
                    del self.watchlist[falseLiteral][0]
                    # Have this clause watch the alt literal now
                    self.watchlist[alt].append(clause)
                    break
            # No alternative has been found after looking through clause
            if not foundAlt:
                return False
        # Alternative is found (or loop condition fails?)
        return True


    # Basic SAT solver alogrithm that uses recursion
    def simpleSolve(self,var):
        # Check if this is the last assignment to end function call
        if var == self.SAT.numOfVars:
            return True #self.assignment
        
        # Check over all possible assignments
        for truthValue in [0,1]:
            self.assignment[var] = truthValue
            # Update the watchlist with the variable's literal with given value
            if self.updateWatchlist( var << 1 | truthValue ):
                # Check if the next variable is solved with all the assignments done
                if self.simpleSolve(var+1):
                    return True

        
        # Reset and return False since there was a conflict        
        self.assignment[var] = None
        return False
            

    # SAT solver to find all solutions that uses simpleSolver()
    def simpleSolveAll(self):
        # Once one solution is found, add the negative of this clause and find
        # the next solution. If no new solution can be found, stop and return
        # soltions in a list

        # List of solutions
        solutions = []

        # Search for all solutions until exhausted
        searching = True
        while True:
            # Reset the watchlist
            self.createWatchlist()

            # Will tell us if all solutions have been found
            searching = self.simpleSolve(0)

            # Break out since we found all solutions
            if not searching:
                return solutions

            # Solution dictionary as defined by the input CNF file
            solDict = {}
            for i in self.assignment:
                # Variable integer as defined by input file
                varInt = int(self.SAT.varDict[i])
                solDict[varInt] = self.assignment[i]

            # Save the resulting solution
            solutions.append(solDict.copy())

            # New clause of negated solution
            tempNegSol = set()
            for var in self.assignment:
                # Get if variable was negated and reverse it
                negTemp = self.assignment[var] #self.SAT.negate( self.assignment[var] )
                # Add the literal equivalent to the clause
                tempNegSol.add( var << 1 | negTemp )
            # Add new clause 
            self.SAT.clauses.append(tempNegSol)

            # Reset the assignments
            for key in self.assignment:
                self.assignment[key] = None


    # Iterative solving algorithm that uses backtracking
    def iterSolve(self, var):
        # Save solutions
        solutions = []
        # Set the list of states to untried for each variable
        # Possible states are 0-3:
        #   0 -> Nothing tried yet
        #   1 -> False tried, not True
        #   2 -> True tried, not False
        #   3 -> Tried both True and False
        state = [0] * self.SAT.numOfVars

        # Loop through all the possibilities
        while True:
            # If we went through all the variables
            if var == self.SAT.numOfVars:
                # Save solution
                solutions.append(self.assignment.copy())
                var -= 1
                continue
            # Attempt assigning var a truth value. Can be improved by deciding 
            # which value to attempt first
            tried = False
            for a in [0, 1]:
                # Only true when {a=0;s=0,2} and {a=1;s=1,2}
                if (state[var] >> a) & 1 == 0:
                    tried = True
                    # Set the bit indicating a has been tried for var
                    state[var] |= 1 << a
                    self.assignment[var] = a
                    if not self.updateWatchlist(var << 1 | a):
                        self.assignment[var] = None
                    else:
                        var += 1
                        break

            if not tried:
                # No more backtracking so return solutions found
                if var == 0:
                    return solutions
                # Backtrack for other solutions
                else:
                    self.assignment[var] = None
                    state[var] = 0
                    var -= 1

    
    # Find all solutions by iterative solver using iterSolve
    def iterSolveAll(self):
        # Create watchlist and return all the solutions of SAT object
        self.createWatchlist()
        return self.iterSolve(0)
        
