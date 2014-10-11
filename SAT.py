#

# SAT object that will have work done onto
class SAT(object):
    """
    """

    # SATObject has only a list of variables (for refrence) and a clause list
    def __init__(self):
        # Dictionary of variable strings (keys) to refernce variable (values)
        self.varDict = {} 
        # List of clauses represented with sets of literals
        self.clauses = []

    # Return string representation of SAT object (clauses)
    def __str__(self):
        # String to build up and then return
        string = ""
        # Itrerate over the clauses to get the string representation
        for clause in self.clauses:
            string += "{"
            string += self.getClauseStr(clause)
            string += "}\n"
        return string

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
            var_ = int(literal[isNeg:])
            # Get recasted variable
            if var_ in self.varDict:
            	# Get variable from dictionary
            	var = self.varDict[var_]
            else:
            	# Get variable by appending it to the next spot in dictionary
            	var = len(self.varDict)
            	self.varDict[var_] = var
            # Reform literal from new variable notation (2*v or 2*v+1 if neg) 
            literal = var << 1 | isNeg
            # Add literal for this clause
            clause.add(literal)
        # Add this clause into the group of clauses
        self.clauses.append(clause)

    # Add missing variables to varDict skipped over when reading file
    # Function assumes that the number of variables (numOfVars) is correct 
    def addMissingVarsToDict(self,numOfVars):
        # Get vars from varDict keys (vars given by file)
        varsFromFile = set(self.varDict.keys())
        # Get the vars not already defined in dictionary
        missingVars = varsFromFile.symmetric_difference(set(range(1,numOfVars+1)))
        # Iterate over missing variables & add them to dictionary in next spot
        for var in missingVars:
            self.varDict[var] = len(self.varDict)

    @classmethod
    def getFromFile(cls,cnfFile):
        '''
           Alternative constructor that reads CNF file and imports clauses into 
           SAT object instance. 

           Input: String of CNF filename
        '''
        # Create instance of this object
        satInstance = cls()
        # Get lines from CNF data and then close file
        with open(cnfFile) as f:
            cnfLines = f.readlines()
        # First line gives us information of data format
        metaData = cnfLines.pop(0).split()
        # Get the number (int) of varaibles and clauses specified by file
        numOfVars, numOfClauses = int(metaData[2]), int(metaData[3])
        # Add clauses from file (skip the first line of metadata)
        for line in cnfLines:
            satInstance.getClauseFromLine(line)
        # Add any missing variables that were missed when reading in file
        satInstance.addMissingVarsToDict(numOfVars)
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
            if not isinstance(literal,int) or (literal < 0):
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
        if not isinstance(literal,int) or (literal < 0):
             return "undefined"
        elif (literal >> 1) not in self.varDict: 
        	return "undefined"
        # Add negative
        elif (literal & 1): 
            return "-%d" %self.varDict[literal >> 1]
        else:
            return "%d"  %self.varDict[literal >> 1]

    #
    def getClauseStr(self,clause,joinerStr = ",",fromDict=True):
        clauseStr = ""
        # Build up string by joining
        for literal in clause:
            clauseStr += self.getLiteralStr(literal,fromDict) + joinerStr
        # Remove last joiner before returning
        return clauseStr[:-len(joinerStr)]

