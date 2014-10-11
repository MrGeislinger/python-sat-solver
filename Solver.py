#

# Solver object to preform operations on the SAT object
Solver(object):
    '''
    '''
    # Import the SAT object
    import SAT
    
    # Constructor by using data file
    def __init__(self,dataFile):
        # Create SAT object from data file
        self.sat = SAT.initFromFile(dataFile)
        # Assignment of truth values (0,1=True,False) for SAT object
        self.assignment = {}
        # Initiate each variable assignment with no assignment (None)
        for i in range(numOfVars):
            self.assignment[i] = None

    # Assign assignment varaible a truth value
    def assignVar(self,var,truthValue):
        self.assignment[var] = truthValue
