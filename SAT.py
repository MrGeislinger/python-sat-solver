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

    # Alternative constructor by using data file in CNF format
    @classmethod
    def initFromFile(cls,cnfFile):
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
        satInstance.numOfVars,numOfClauses = int(metaData[2]), int(metaData[3])
        # Add clauses from file (skip the first line of metadata)
        for line in cnfLines:
            satInstance.getClauseFromLine(line)
        # Add any missing variables that were missed when reading in file
        satInstance.addMissingVarsToDict()
        return satInstance

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
            var_Str = literal[isNeg:]      #str version
            # Get/create recasted variable with varDict
            if var_Str in self.varDict:
            	# Get variable from dictionary
            	var = self.varDict[var_Str]
            else:
            	# Append variable to the next spot in dictionary
            	var = len(self.varDict) >> 1 #divide by 2 since len is 2n
            	self.varDict[var_Str] = var
                # Add reverse look up by string version for easy printing
                self.varDict[var] = var_Str
            # Reform literal from new variable notation (2*v or 2*v+1 if neg) 
            literal = self.getLit(var,isNeg) #var << 1 | isNeg
            # Add literal for this clause
            clause.add(literal)
        # Add this clause into the group of clauses
        self.clauses.append(clause)

    # Add missing variables to varDict skipped over when reading file
    # Function assumes that the number of variables (numOfVars) is correct 
    def addMissingVarsToDict(self):
        # Converts to int if str (else gives -1 since var can't <0)
        isStr = lambda x: int(x) if isinstance(x,str) else -1  
        # Get vars from varDict keys (only str types; vars given by file)
        varsFromFile = set( map(isStr,self.varDict.keys()) ) #all non-str -> -1
        varsFromFile.add(-1)    #ensure something to remove
        varsFromFile.remove(-1) #get rid of the mappings from non-ints
        # Get the vars not already defined in varDict
        missingVars = varsFromFile.symmetric_difference(set(range(1,self.numOfVars+1)))
        # Iterate over missing variables & add them to varDict in next spot
        for var in missingVars:
            varStr = str(var) #convert to string (would've been given by file)
            varInt = len(self.varDict) >> 1 #divide by 2 to get next spot          
            self.varDict[varStr] = varInt 
            self.varDict[varInt] = varStr
       
    #
    def getClauseStr(self,clause,joinerStr = ",",fromDict=True):
        clauseStr = ""
        # Build up string by joining
        for literal in clause:
            clauseStr += self.getLiteralStr(literal,fromDict) + joinerStr
        # Remove last joiner before returning
        return clauseStr[:-len(joinerStr)]

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
            # Check if negated and convert literal to variable 
            elif self.isNeg(literal) == 1: 
                return "-%d" %self.getVar(literal)
            else:
                return "%d"  %self.getVar(literal)

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
        #
        var = self.getVar(literal)
        # Check if literal is valid/defined
        if not isinstance(literal,int) or (literal < 0):
             return "undefined"
        elif var not in self.varDict: 
        	return "undefined"
        # Add negative to the string variable
        elif self.isNeg(literal) == 1: 
            return "-%s" %self.varDict[var]
        # Return the string variable
        else:
            return "%s"  %self.varDict[var]

    ###################################
    # Literal and Variable Operations #
    ###################################

    # Returns 1 if negated, 0 if not negated
    def isNeg(self,literal):
        return (literal & 1) #bit comparison

    # Returns negated literal
    def negate(self,literal):
        return (literal ^ 1) #negate the literal (2*v) <-> (2*v+1)

    # Returns variable that holds a literal
    def getVar(self,literal):
        return (literal >> 1) #essentially a division by 2 (floor)

    # Returns literal from variable (optional negation: isNegated=1)
    def getLit(self,var,isNegated=0):
        return (var << 1 | isNegated)

