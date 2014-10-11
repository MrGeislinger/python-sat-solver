#
from SAT import *
# Solver object to preform operations on the SAT object
class Solver(object):

    '''
    '''
     
    # Constructor by using data file
    def __init__(self,dataFile):
        # Import the SAT object
        #import SAT
        #
        self.sat = SAT.initFromFile(dataFile)
        # Create SAT object from data file
        #self.sat = .initFromFile(dataFile)
        # Assignment of truth values (0,1=True,False) for SAT object
        self.assignment = {}
        # Lambda function to map only ints in sat.varDict to assignment 
        isInt = lambda x : x if isinstance(x,int) else False
        # Iterate over just the int keys from sat.varDict
        for var in map(isInt,self.sat.varDict.keys()):
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
        return True #will need to change to check all assignments with claues
