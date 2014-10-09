#

# SAT object that will have work done onto
class SATObject(object):
    """
    """
    # SATObject has only a list of variables (for refrence) and a clause list
    def __init__(self):
        # Dictionary in case variable is greater than total number of variables
        self.varDict = {} 
        # List of clauses represented with tuples of literals
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
            self.varDict[len(self.varDict)] = literal[isNeg:]
            # Reform literal from new variable notation (2*v or 2*v+1 if neg) 
            # Note len of dict is the variable value
            literal = len(self.varDict) << 1 | isNeg
            # Append to the list for this clas
            clause.add(literal)
        # Add this clause into the group of clauses
        self.clauses.append(clause)
