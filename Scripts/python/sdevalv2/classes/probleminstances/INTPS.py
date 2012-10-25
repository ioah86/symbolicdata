from ProblemInstance import ProblemInstance

class INTPS(ProblemInstance):
    """
    The concrete problem instance INTPS from SymbolicData. It represents polynomial systems with integer
    coefficients. Details on INTPS can be found in SymbolicData.
    
    @author:  Albert Heinle
    @contact: albert.heinle@rwth-aachen.de
    """
    
    def __init__(self, name, sdTable,vars=None, basis=None):
        """
        The constructor of an INTPS-Instance. The name and the SD-Table are needed for the superclass ProblemInstance.
        The other parameters are the vars used for the polynomial system and the basis containing polynomials.

        @param         name: The name of the INTPS-ProblemInstance
        @type          name: string
        @param      sdTable: The SDTable containing INTPS-Instances. This input will not be checked.
        @type       sdTable: SDTable
        @param         vars: A list of variables used in the INTP-System
        @type          vars: list
        @param        basis: The polynomials forming a basis of the INTP-System. This input will not be checked whether
                             there are polynomials using variables not in the list of variables.
        @type         basis: list
        """
        super(INTPS,self).__init__(name,sdTable)
        self.__vars              = vars
        self.__basis             = basis
    
    def getVars(self):
        """
        Returns the variables used in the polynomial system.

        @returns: The variables of the polynomial system
        @rtype:   list
        """
        return self.__vars
    
    def getBasis(self):
        """
        Returns the basis of the integer polynomial system.

        @returns: The basis of the integer polynomial system.
        @rtype:   list
        """
        return self.__basis

    def __str__(self):
        """
        Returns a string representation of this INTPS-Entry. It has the following form::
            INTPS-Entry: <name of the Entry>
            Variables:   <comma separated variables>
            basis:
            <poly1>
            <poly2>
            ...
        """
        result="INTPS-Entry: %s\nVariables: %s\nbasis:\n%s" % (self.getName(), ",".join(self.__vars), "\n".join(self.__basis))
        return result
    
    def __del__(self):
        """
        TODO
        """
        pass
