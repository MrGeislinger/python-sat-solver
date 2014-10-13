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

	# Create a watch list to make algoriths simple
	def createWatchlist(self):
        # Create a 2*numOfVars sized watchlist of empty lists
		self.watchlist = [ [] for i in range(2*self.SAT.numOfVars) ]
		# Watch the first literal in each clause
		for clause in self.SAT.clauses
			# Convert clause within watchlist to be a list
    		self.watchlist[ list(clause)[0] ].append(clause)
    
    # Updates the watchlist for 
    def updateWatchlist(self,falseLiteral):
		#
        while watchlist[falseLiteral]:
            clause = watchlist[falseLiteral][0] #get first watched clause
            foundAlt = False
            #            
            for alt in clause:
                v = self.SAT.getVar(alt)
                a = self.SAT.isNeg(alt)
            #
            if self.assignment[v] is None or 
               self.assignment[v] == self.SAT.negate(a):
                foundAlt = True
                # Get rid of this clause since literal is now True
                del self.watchlist[falseLiteral][0]
                self.watchlist[alt].append(clause)
                break
            #
            if not foundAlt:
                return False
            #
            return True


    # Basic SAT solver alogrithm that uses recursion
    def simpleSolve(self,var):
        # Check if this is the last assignment to end function call
        if var == self.numOfVars:
            yield self.assignment
            return 

        #
        for truthValue in [0,1]:
            self.assignment[var] = truthValue
            #
            if self.updateWatchlist( self.SAT.getLit(var) ):
                #
                for truthValue in self.simpleSolve(var+1):
                    #
                    yield truthValue

        #
        self.assignment[var] = None



