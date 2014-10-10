#

# SAT object that will have work done onto
class SATObject(object):
    """
    """

    # SATObject has only a list of variables (for refrence) and a clause list
    def __init__(self):
        # Dictionary of variable strings (keys) to refernce variable (values)
        self.varDict = {} 
        # List of clauses represented with sets of literals
        self.clauses = []

    # Reads in clause from a line, but assumes every line ends with zero and 
    # full clause is listed on this line
    def getClauseFromLine(self,clauseLine):
        # Clause won't contain repeating literals (CNF) 
        clause = set()
        # Go over each literal in clause (ignore zero at end)
        for literal in clauseLine.split()[:-1]:
            # Save whether negation (is either 0 or 1)
            isNeg = 1 if (literal[0]=='-') else 0
            # Variable is a literal with (possible) negation removed
            # Add variable to dict as the next integer available for reference
            #if literal[isNeg:] not in self.varDict:
            #    self.varDict[literal[isNeg:]] = len(self.varDict) 
            # Get recasted variable
            var = self.varDict[literal[isNeg:]]
            # Reform literal from new variable notation (2*v or 2*v+1 if neg) 
            literal = var << 1 | isNeg
            # Add literal for this clause
            clause.add(literal)
        # Add this clause into the group of clauses
        self.clauses.append(clause)

    # Takes in an integer and creates dictionary of that number
    # Ex: setVarDict(3) -> {'1':0, '2':1, '3':2}
    def setVarDict(self,numOfVars):
        for v in range(numOfVars):
            self.varDict[str(v+1)] = v
	
	# Alternative contructor to make SAT object  
    @classmethod
    def getFromFile(cls,cnfFile,hasSet=True):
        # Create instance of this object
        satInstance = cls()
        # Get lines from CNF data and then close file
        with open(cnfFile) as f:
            cnfLines = f.readlines()
        # First line gives us information of data format
        metaData = cnfLines.pop(0).split()
        # Get the number of varaibles and clauses specified by file
        numOfVars, numOfClauses = metaData[2], metaData[3]
        # Add variables to dictionary for reference
        satInstance.setVarDict(int(numOfVars))
        # Add clauses from file (skip the first line of metadata)
        for line in cnfLines:
            satInstance.getClauseFromLine(line)
        return satInstance
