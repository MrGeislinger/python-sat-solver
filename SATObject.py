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
    # full clause is listed on this line.
    def getClauseFromLine(self,clauseLine):
        # Clause won't contain repeating literals (CNF) 
        clause = set()
        # Go over each literal in clause (ignore zero at end)
        for literal in clauseLine.split()[:-1]:
            # Save whether negation (is either 0 or 1)
            isNeg = 1 if (literal[0]=='-') else 0
            # Variable is a literal with (possible) negation removed
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
    def getFromFile(cls,cnfFile):
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
        
    # Get string representation of literal either by direct conversion or as
    # defined by varDict. 
    # Ex: getLiteralStr(5) -> '-2'
    #
    # Input: int represented by literal (2*v or 2*v+1 where v in {0,1,..}
    # Output: string represented by literal or 'undefined' if not valid
    def getLiteralStr(self,literal,fromDict=False):
        '''
            Gives representation of literal to the string. 
            Use `fromDict = True` to return literal as defined by varDict.

            See getLiteralStrFromDict.
        '''
        # Use varDict definition after conversion
        if fromDict:
            return self.getLiteralStrFromDict(literal)
        else:
            # Check if literal can be converted properly (an int and greater than 0)
            if isinstance(literal,int) and (literal < 0):
        	    return "undefined"
            # Check if negated and convert literal to variable with bit shift
            elif (literal & 1): 
                return "-%d" %(literal >> 1)
            else:
                return "%d"  %(literal >> 1)

    # Get string representation of literal as defined from varDict
    # Input: int represented by literal (2*v or 2*v+1 where v in {0,1,..}
    # Output: string represented by literal or 'undefined' if not in varDict
    def getLiteralStrFromDict(self,literal):
        '''
        	Gives string representation of literal as defined by varDict.
        	Converts literal and then returns representation in varDict.

        	Returns: 
        		"undefined" if not in varDict or can't be coverted
        		"-#"        if negated literal
        		"#"         if not negated literal

        '''
        # Check if literal is defined/valid
        if isinstance(literal,int) and (literal < 0):
             return "undefined"
        elif str(literal >> 1) not in self.varDict: 
        	return "undefined"
        # Add negative
        elif (literal & 1): 
            return "-%d" %self.varDict[str(literal >> 1)]
        else:
            return "%d"  %self.varDict[str(literal >> 1)]
