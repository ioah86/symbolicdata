#!/usr/bin/env python
# @author: Albert Heinle
"""
This module contains different classes for accessing the data in the symbolic data tables.
The usage is specified by the documentation text at the top of every class definition.
"""

import xml.dom.minidom as dom
import os
import MachineSettings as MS
import commands

def convertStringToIntList(input):
    """
    In various xml-files there is often a list of integers given in a string and
    we are interested to convert it in a list of integers. This function serves
    this purpose.
    """
    result = input.rsplit(" ");
    for i in xrange(0,len(result)):
        result[i] = int(result[i])
    return result;
        
#{ Classes that capsulate symbolic data access
################################################################################
####################Class INTPS#################################################
################################################################################
class INTPS(object):
    """
    Class of type INTPS. For detailed description of the data contained in this
    table read the documentation of SymbolicData.
    """
    #TODO: Add all the getters and setters and stuff like that.
    def __init__(self, xmlFileName = None):
        """
        INPUT: Usually, one initializes an instance of an INTPS-object giving the
        path of an XML-File containing an INTPS-Problem. If it is not given, all
        typical parameters will be initialized by "NONE"
        """
        if xmlFileName != None:
            #In this case a file with XML-data is given by the user
            self.__xmlFileName = xmlFileName
            try:
                self.__xmlTree = dom.parse(xmlFileName)
            except:
                print "ERROR IN INTPS: Given path to .XML-File not valid"
                os._exit(-2)
            try:
                self.__vars = self.__extractVarsFromXMLTree()
                self.__parameters = self.__extractParametersFromXMLTree()
                self.__basis = self.__extractBasisFromXMLTree()
                self.__dlist = self.__extractDlistFromXMLTree()
                self.__isHomog = self.__extractIsHomogFromXMLTree()
                self.__llist = self.__extractLlistFromXMLTree()
                self.__degree = self.__extractDegreeFromXMLTree()
                self.__basedomain = self.__extractBaseDomainFromXMLTree()
            except:
                print "ERROR: Could not read data from XML-File"
        else:
            #In this case the user wants to create an empty INTPS-Object to fill
            #it with data
            self.__xmlFileName = None
            self.__xmlTree = None
            self.__vars = None
            self.__basedomain = None
            self.__parameters = None
            self.__basis = None
            self.__file = None
            self.__dlist = None
            self.__isHomog = None
            self.__llist = None
            self.__attributes = None
            self.__degree = None
            self.__dim = None
            self.__isoPrimeDegrees = None
            self.__isoPrimeDims = None
            self.__isoPrimes = None
            self.__RootTableEntries = None
    
    def __extractVarsFromXMLTree(self):
        if (self.__xmlTree.getElementsByTagName("vars") == []):
            return None
        result = []
        variablesNode = self.__xmlTree.getElementsByTagName("vars")[0]
        variables = variablesNode.firstChild.data
        result = variables.rsplit(",")
        for i in xrange(0,len(result)):
            #conversion from unicode to ascii
            result[i] = str(result[i])
        return result
    
    def __extractParametersFromXMLTree(self):
        if (self.__xmlTree.getElementsByTagName("parameters") == []):
            return None
        result = []
        variablesNode = self.__xmlTree.getElementsByTagName("parameters")[0]
        variables = variablesNode.firstChild.data
        result = variables.rsplit(",")
        for i in xrange(0,len(result)):
            #conversion from unicode to ascii
            result[i] = str(result[i])
        return result
    
    def __extractBasisFromXMLTree(self):
        if (self.__xmlTree.getElementsByTagName("basis") == []):
            return None
        result = []
        basis = self.__xmlTree.getElementsByTagName("basis")[0] #TODO: Is there a case, where more than one basis is allowed?
        polynomials = basis.getElementsByTagName("poly");
        for poly in polynomials:
            result.append(poly.firstChild.data)
        for i in xrange(0,len(result)):
            #conversion from unicode to ascii
            result[i] = str(result[i])
        return result
    
    def __extractDlistFromXMLTree(self):
        if (self.__xmlTree.getElementsByTagName("dlist") == []):
            return None
        result = []
        dlistFromTree = self.__xmlTree.getElementsByTagName("dlist")[0] #TODO: is there a case, where more than one dlist
        dlist = dlistFromTree.firstChild.data
        result = convertStringToIntList(dlist)
        return result
    
    def __extractIsHomogFromXMLTree(self):
        if (self.__xmlTree.getElementsByTagName("isHomog") == []):
            return None
        hom = self.__xmlTree.getElementsByTagName("isHomog")[0]
        result = hom.firstChild.data
        if result == "true":
            return True
        if result == "false":
            return false
        return bool(int(result))
    
    def __extractLlistFromXMLTree(self):
        if (self.__xmlTree.getElementsByTagName("llist")==[]):
            return None
        result = []
        llistFromTree = self.__xmlTree.getElementsByTagName("llist")[0] #TODO: is there a case, where more than one llist
        llist = llistFromTree.firstChild.data
        result = convertStringToIntList(llist)
        return result
        
    def __extractDegreeFromXMLTree(self):
        if (self.__xmlTree.getElementsByTagName("degree")==[]):
            return None
        deg = self.__xmlTree.getElementsByTagName("degree")[0]
        result = deg.firstChild.data
        return int(result)
    
    def __extractBaseDomainFromXMLTree(self):
        if (self.__xmlTree.getElementsByTagName("basedomain")==[]):
            return None
        bd = self.__xmlTree.getElementsByTagName("basedomain")[0]
        result = bd.firstChild.data
        return str(result)
    
    def getVars(self):
        return self.__vars
    
    def getBasis(self):
        return self.__basis
    
    def getDlist(self):
        return self.__dlist
    
    def getIsHomog(self):
        return self.__isHomog
    
    def getLlist(self):
        return self.__llist
    
    def getDegree(self):
        return self.__degree
    
    def getBaseDomain(self):
        return self.__basedomain
    
    def getParameters(self):
        return self.__parameters
    
    def __del__(self):
        del self.__xmlFileName
        del self.__xmlTree
        del self.__vars
        del self.__basedomain
        del self.__parameters
        del self.__basis
        del self.__file
        del self.__dlist
        del self.__isHomog
        del self.__llist
        del self.__attributes
        del self.__degree
        del self.__dim
        del self.__isoPrimeDegrees
        del self.__isoPrimeDims
        del self.__isoPrimes
        del self.__RootTableEntries

###############################################################################
####################Class FREEALGEBRA##########################################
################################################################################
class FREEALGEBRA(object):
    """
    Class of type FREEALGEBRA. For detailed description of the entries in that table
    read the documentation of SymbolicData.
    INPUT: A path to an xml-File containing an instance of a FREEALGEBRA problem
    should be given as input. The variables intern will then be initialized by the
    values in the xml-File.
    """
    def __init__(self, xmlFileName = None):
        if xmlFileName != None:
            #In this case a file with XML-data is given by the user
            self.__xmlFileName = xmlFileName
            try:
                self.__xmlTree = dom.parse(xmlFileName)
            except:
                print "ERROR in FREEALGEBRA: XML-Path not valid!"
                os._exit(-2)
            try:
                self.__vars = self.__extractVarsFromXMLTree()
                self.__parameters = self.__extractParametersFromXMLTree()
                self.__basis = self.__extractBasisFromXMLTree()
                self.__uptoDeg = self.__extractUpToDegreeFromXMLTree()
                self.__basedomain = self.__extractBaseDomainFromXMLTree()
            except:
                print "ERROR in FREEALGEBRA: The values could not be initialized correctly!"
                os._exit(-2)
        else:
            #In this case the user wants to create an empty INTPS-Object to fill
            #it with data
            self.__xmlFileName = None
            self.__xmlTree = None
            self.__vars = None
            self.__basedomain = None
            self.__parameters = None
            self.__basis = None
            self.__uptoDeg = None
            self.__RootTableEntries = None
    
    def __extractVarsFromXMLTree(self):
        if (self.__xmlTree.getElementsByTagName("vars") == []):
            return None
        result = []
        variablesNode = self.__xmlTree.getElementsByTagName("vars")[0]
        variables = variablesNode.firstChild.data
        result = variables.rsplit(",")
        for i in xrange(0,len(result)):
            #conversion from unicode to ascii
            result[i] = str(result[i])
        return result
    
    def __extractParametersFromXMLTree(self):
        if (self.__xmlTree.getElementsByTagName("parameters") == []):
            return None
        result = []
        variablesNode = self.__xmlTree.getElementsByTagName("parameters")[0]
        variables = variablesNode.firstChild.data
        result = variables.rsplit(",")
        for i in xrange(0,len(result)):
            #conversion from unicode to ascii
            result[i] = str(result[i])
        return result
    
    def __extractBasisFromXMLTree(self):
        if (self.__xmlTree.getElementsByTagName("basis") == []):
            return None
        result = []
        basis = self.__xmlTree.getElementsByTagName("basis")[0] #TODO: Is there a case, where more than one basis is allowed?
        polynomials = basis.getElementsByTagName("poly");
        for poly in polynomials:
            result.append(poly.firstChild.data)
        for i in xrange(0,len(result)):
            #conversion from unicode to ascii
            result[i] = str(result[i])
        return result
    
    def __extractUpToDegreeFromXMLTree(self):
        if (self.__xmlTree.getElementsByTagName("uptoDeg")==[]):
            return None
        deg = self.__xmlTree.getElementsByTagName("uptoDeg")[0]
        result = deg.firstChild.data
        return int(result)
    
    def __extractBaseDomainFromXMLTree(self):
        if (self.__xmlTree.getElementsByTagName("basedomain")==[]):
            return None
        bd = self.__xmlTree.getElementsByTagName("basedomain")[0]
        result = bd.firstChild.data
        return str(result)

    
    def getVars(self):
        return self.__vars
    
    def getBasis(self):
        return self.__basis
    
    def getUpToDegree(self):
        return self.__uptoDeg
    
    def getBaseDomain(self):
        return self.__basedomain
    
    def getParameters(self):
        return self.__parameters
    
    def __del__(self):
        pass
        """del self.__xmlFileName
        del self.__xmlTree
        del self.__vars
        del self.__basedomain
        del self.__parameters
        del self.__basis
        del self.__uptoDeg
        del self.__RootTableEntries"""


################################################################################
####################Class COMP##################################################
################################################################################
class COMP(object):
    """
    Instance of class COMP:
    For details on the table COMP, check the Symbolic Data Documentation.
    INPUT: An .XML-File containing an entry of the table COMP. Here, one can get
    access to the variables in one class.
    """
    def __init__(self,xmlFileName = None):
        if xmlFileName != None:
            self.__xmlFileName = xmlFileName
            self.__xmlTree = dom.parse(xmlFileName)
            self.__kind = self.__extractStringDataFromXMLTree("kind")
            self.__ordering = self.__extractStringDataFromXMLTree("ordering")
            self.__coeff = self.__extractStringDataFromXMLTree("coeff")
            self.__Check = self.__extractStringDataFromXMLTree("Check")
            self.__InitComp = self.__extractStringDataFromXMLTree("InitComp")
            self.__InitEx = self.__extractStringDataFromXMLTree("InitEx")
            self.__require = self.__extractStringDataFromXMLTree("require")
            self.__what = self.__extractStringDataFromXMLTree("what")
        else:
            self.__kind = None
            self.__coeff = None
            self.__ordering = None
            self.__Check = None
            self.__InitComp = None
            self.__InitEx = None
            self.__require = None
            self.__what = None
    
    def __extractStringDataFromXMLTree(self, inString):
        if (self.__xmlTree.getElementsByTagName(inString)==[]):
            return None
        strdata = self.__xmlTree.getElementsByTagName(inString)[0]
        result = strdata.firstChild.data
        return str(result)
    
    #TODO:Setter and Getter.
    def getCoeff(self):
        return self.__coeff
    
    def getOrdering(self):
        return self.__ordering
    
    def getKind(self):
        return self.__kind
    
#}
################################################################################
####################Class TASK##################################################
################################################################################
class Task(object):
    """
    Class Task: Instances of the type task are usually containing the following
    information:
    - A Problem-File in the COMP-Table
    - Instances of the problems that should be calculated
    - A list of computer algebra systems where the computations should be run at.
    INPUT: Usually, a user is creating a task file before using the program
    "create_Tasks.py". The output of that program will be an .XML-file that specifies
    an instance of this class. The path to this program will be the input of this
    class.
    USAGE: After initializing the data of the given XML-File, three variables will be
    created:
    - Completed Calculations
    - Running Calculation
    - Waiting Calculation
    First of all, all problems will be saved to Waiting Calculations. When the
    user wants to extract one problem from the waiting list, he calls the function
    setRunCalculation. After that, there is one calculation active. After the calculation is
    over, one fills the variable with additional information and puts it into the
    Completed Calculations list by using the function SetRunCalculationCompleted
    """
    def __init__(self,xmlFileName=None):
        if xmlFileName != None:
            self.__xmlFileName = xmlFileName
            try:
                self.__xmlTree = dom.parse(xmlFileName)
            except:
                print "ERROR in Task: Could not open given path."
                os._exit(-2)
            try:
                self.__comp = self.__extractStringDataFromXMLTree("COMP")
                self.__casList = self.__extractCASList()
                self.__problemList = self.__extractProblemList()
            except:
                print "ERROR in Task: Could not initialize data properly"
        self.__completedCalculations = []
        self.__runningCalculation     = None
        self.__waitingCalculations   = self.__fillWaitingCalculationsList()
            
    def __extractStringDataFromXMLTree(self, inString):
        if (self.__xmlTree.getElementsByTagName(inString)==[]):
            return None
        strdata = self.__xmlTree.getElementsByTagName(inString)[0]
        result = strdata.firstChild.data
        return str(result).strip()
    
    def __fillWaitingCalculationsList(self):
        """
        Creates a list of touples containing a computer algebra system and
        a concrete instance of one problem.
        """
        result = []
        for prob in self.__problemList:
            for cas in self.__casList:
                result.append([cas,prob.firstChild.data.strip()])
        return result
        
    def __extractCASList(self):
        result = map(lambda a: str(a.firstChild.data.strip()),self.__xmlTree.getElementsByTagName("CAS"))
        return result
    
    def getProceedingsTable(self):
        """
        Creates a table in .html format, that informs the reader, which taks is currently
        running/waiting/completed. Returns this .html file as a string
        """
        result = "<table>"
        for compl in self.__completedCalculations:
            result += "<tr><td>"+compl[0]+":"+compl[1]+"</td><td bgcolor=green>COMPLETED</td></tr>"
        if self.__runningCalculation != None:
            result += "<tr><td>"+self.__runningCalculation[0]+":"+self.__runningCalculation[1]+"</td><td bgcolor=yellow>RUNNING</td></tr>"
        for waiting in self.__waitingCalculations:
            result += "<tr><td>"+waiting[0]+":"+waiting[1]+"</td><td>WAITING</td></tr>"
        return result
            
    def __extractProblemList(self):
        result = self.__xmlTree.getElementsByTagName("problems")[0].childNodes
        result = filter(lambda a: a.nodeType!=dom.Node.TEXT_NODE,result)
        return result
    
    def getWaitingCalculations(self):
        return self.__waitingCalculations
    
    def setRunCalculation(self):
        if (self.__runningCalculation != None):
            return None
        self.__runningCalculation = self.__waitingCalculations.pop()
        return self.__runningCalculation
    
    def setRunCalculationCompleted(self,timeplusoutput):
        self.__completedCalculations.append(self.__runningCalculation+timeplusoutput)
        self.__runningCalculation = None
    
    def createResultsFile(self):
        """
        Creates a html-File containing the computation results. This function is
        going to be called after all computations are completed.
        """
        #####################################
        #Create Content
        #####################################
        content = "<html><head></head><body>"
        content += "<table border=1>"
        tmpResults = self.__completedCalculations
        content += "<tr><td></td>"
        for cas in self.__casList:
            content += "<td><big>"+cas+"</big></td>"
        content += "</tr>"
        lines = []
        while tmpResults != []:
            tmpResult = tmpResults[0]
            lines.append(filter(lambda a: a[1] == tmpResult[1],tmpResults))
            tmpResults = filter(lambda a: a[1] != tmpResult[1],tmpResults)
        for l in lines:
            content += "<tr>"
            content += "<td><big>" + l[0][1] + "</big></td>"
            for cas in self.__casList:
                entry = filter(lambda a: a[0] == cas,l)[0]
                content += "<td>" + ";".join(v for v in entry[2:-1]) +"</td>"
            content += "</tr>"
        content += "</table>"
        content += "</body></html>"
        #######################################
        #Write content to file
        #######################################
        try:
            file = open(self.getXMLFileName()+"RESULTS.html","w")
            file.write(content)
            file.close()
        except:
            print "ERROR: Could not create HTML-File with results."
    
    def getCasList(self):
        return self.__casList
    
    def getProblemList(self):
        return self.__problemList
    
    def getXMLFileName(self):
        return self.__xmlFileName
    
    def getCOMP(self):
        return self.__comp


#{ Classes for handling the different computer algebra systems
################################################################################
####################Class CAS(abstract)#########################################
################################################################################
class CAS(object):
    #The following function gets Data from the SD-Database and translates it
    #into code of the computer algebra system.
    """
    An Abstract Class for computer algebra systems containing the minimum needs
    of a CAS. Every class, which inherits from this one, should have at least this
    properties.
    """
    __name=""
    
    def initData(xmlTree): abstract
    initData = staticmethod(initData)
    
    @staticmethod
    def extractCharacteristicFromString(basedomain):
        if (basedomain == "Z" or basedomain == "Q"):
            return 0
        else:
            l = basedomain.split("(")
            return int(l[1][0:-1])

    def executeFile(self,fileName):abstract
    
    def createExecutableCode(self,xmlComp,xmlProblemFile):abstract
        
    #extractCharacteristicFromString = staticmethod(extractCharacteristicFromString)
    
    def getName(self):
        return self.__name
    
##########SINGULAR###############    
class CAS_Singular(CAS):
    
    dictCOMPToSingular ={
        "GB":"std",
        "FA":"letplaceGBasis"
    }
    
    def __init__(self):
        #first of all: is singular installed?
        self.__name = "Singular.xml"
        #self.__isInstalled = commands.getoutput(MS.CASpaths["Singular"]+" -vq -c quit")
        #TODO: Version check?
        
    def __del__(self):
        pass
    
    def initData(xmlCOMP,xmlFileName):
        tree = dom.parse(xmlFileName)
        #First Case: INTPS:
        if (str(tree.firstChild.tagName) == "INTPS"):
            return CAS_Singular.initINTPS(xmlCOMP,xmlFileName)
        elif (str(tree.firstChild.tagName) == "FREEALGEBRA"):
            return CAS_Singular.initFREEALGEBRA(xmlCOMP,xmlFileName)

    def initINTPS(self,xmlCOMP,xmlFileName):
        """
        Input: xml-File of a concrete INTPS-Problem,
               xml-File of a concrete COMP-Instance, where for instance the
                        the basedomain is specified
        Output: An initialization-Code, where Singular defines the ring and the
                Ideal it should operate later on.
        """
        intps = INTPS(xmlFileName)
        comp = COMP(xmlCOMP)
        result = ""
        #start with ring definition
        #if there is a Basedomain in the Definition of the COMP-Table given,
        #it will be used for our computations. Otherwise the basedomain in the
        #INTPS Table will be used
        if comp.getCoeff() == None:
            bd = intps.getBaseDomain()
        else:
            bd = comp.getCoeff()
        par = intps.getParameters()
        result += "ring R = "
        if (bd == None):
            result +="0,"
        else:
            if (par == None):
                result += str(CAS.extractCharacteristicFromString(bd))+","
            else:
                result += "("+str(CAS.extractCharacteristicFromString(bd))+","
                result += ",".join(v for v in par)
                result += "),"
        tmp = intps.getVars()
        result += "("
        result += ",".join(str(v) for v in tmp)
        result += "),"
        if comp.getOrdering() == None:
            result += "dp;\n" # TODO: One can catch this case
        else:
            result += comp.getOrdering() +";\n"
        #ideal definition
        tmp = intps.getBasis()
        result += "ideal I = "
        result += ",".join(v for v in tmp)
        result +=";\n"
        return result
    
    def __FAPolyToSingularStyle(self,poly,variables):
        result = ""
        plusSplit = poly.split("+")
        for p in plusSplit:
            minusSplit = p.split("-")
            for ms in minusSplit:
                monomials = ms.split("*")
                i = 1
                for m in monomials:
                    if m.strip() not in variables: #Coefficient
                        result += m+"*"
                        continue
                    m = m.strip()+"("+str(i)+")"
                    result += m.strip()+"*"
                    i=i+1
                result = result[:-1] #one * too much
                result += "-"
            result = result[:-1]
            result += "+"
        result = result[:-1]
        return result
                
            
    def initFREEALGEBRA(self,xmlCOMP,xmlFileName):
        fa = FREEALGEBRA(xmlFileName)
        comp = COMP(xmlCOMP)
        result = "LIB \"freegb.lib\";\n"
        if comp.getCoeff() == None:
            bd = fa.getBaseDomain()
        else:
            bd = comp.getCoeff()
        par = fa.getParameters()
        result += "ring r = "
        if (bd == None):
            result +="0,"
        else:
            if (par == None):
                result += str(CAS.extractCharacteristicFromString(bd))+","
            else:
                result += "("+str(CAS.extractCharacteristicFromString(bd))+","
                result += ",".join(v for v in par)
                result += "),"
        tmp = fa.getVars()
        result += "("
        result += ",".join(str(v) for v in tmp)
        result += "),"
        if comp.getOrdering() == None:
            result += "dp;\n" # TODO: One can catch this case
        else:
            result += comp.getOrdering() +";\n"
        result += "int d = "+str(fa.getUpToDegree())+";\n"
        result += "def R = makeLetterplaceRing(d);\n"
        result += "setring(R);\n"
        result += "ideal I ="+",\n".join(self.__FAPolyToSingularStyle(v,fa.getVars()) for v in fa.getBasis())+";\n"
        return result;
    
    def executeFile(self,fileName):
        """
        Executes Singular with fileName as Input. Time will also be returned
        """
        return commands.getoutput(MS.timeCommand+" "+MS.CASpaths["Singular"]+" -q < "+fileName)
    
    def createExecutableCode(self,xmlComp,xmlProblemFile):
        """
        This function creates executable Code for the different possible calculations
        listed in the table COMP. The second Argument is the problem file itself.
        """
        comp = COMP(xmlComp)
        result = "";
        problemTree = dom.parse(xmlProblemFile)
        pr = str(problemTree.firstChild.tagName.strip())
        if (pr == "INTPS"):
            result += self.initINTPS(xmlComp,xmlProblemFile)
            result += self.dictCOMPToSingular[comp.getKind()]
            result +="(I);print(I,\"%s\");$" # TODO: print in Liste
        if (pr == "FREEALGEBRA"):
            fa = FREEALGEBRA(xmlProblemFile)
            result += self.initFREEALGEBRA(xmlComp,xmlProblemFile)
            result += "option(prot);\noption(redTail);\noption(redSB);\n"
            result += "ideal J = "
            result += self.dictCOMPToSingular[comp.getKind()]
            result += "(I,"+str(fa.getUpToDegree())+");\n"
            result += "print (J, \"%s\");$"
        #TODO:Add further Possible Problem files.
        return result
    
#############MAPLE######################
class CAS_Maple(CAS):

    _dictCOMPToMaple ={
        "GB":"Basis",
        "lp":"plex",
        "dp":"grlex"
    }#TODO: All in lowercase and change code for that
    
    def __init__(self):
        #first of all: is Maple installed?
        self.__name = "Maple.xml"
        #TODO: TEMPORARYself.__isInstalled = os.system("Maple -c quit;")
        #TODO: Version check?
        
    def __del__(self):
        pass
    
    def initData(xmlCOMP,xmlFileName):
        tree = dom.parse(xmlFileName)
        #First Case: INTPS:
        if (str(tree.firstChild.tagName) == "INTPS"):
            return CAS_Maple.initINTPS(xmlCOMP,xmlFileName)
    
    
    def initINTPS(self,xmlCOMP,xmlFileName):
        """
        Input: xml-File of a concrete INTPS-Problem,
               xml-File of a concrete COMP-Instance, where for instance the
                        the basedomain is specified
        Output: An initialization-Code, where Maple defines the ring and the
                Ideal it should operate later on.
        """
        intps = INTPS(xmlFileName)
        comp = COMP(xmlCOMP)
        result = ""
        #start with ring definition
        #if there is a Basedomain in the Definition of the COMP-Table given,
        #it will be used for our computations. Otherwise the basedomain in the
        #INTPS Table will be used
        if comp.getCoeff() == None:
            bd = intps.getBaseDomain()
        else:
            bd = comp.getCoeff()
        par = intps.getParameters()
        result += "with(Groebner):\n" #Package needed to be load in Maple
        result += "Ideal := {" #Start Ideal definition
        tmp = intps.getBasis()
        result += ",".join(v for v in tmp)
        result +="}"
        #finite characteristic?
        if (bd != None):
            characteristic = CAS.extractCharacteristicFromString(bd)
            if (characteristic != 0):
                result += " mod "+str(characteristic);
        #finite characteristic check end
        result += ":\n"
        result += "ordering:="+self._dictCOMPToMaple[comp.getOrdering().lower()]+"(";
        result += ",".join(v for v in intps.getVars());
        result += "):\n";
        return result;
    
    def executeFile(self,fileName):
        """
        Executes Maple with fileName as Input. Time will also be returned
        """
        return commands.getoutput(MS.timeCommand+" "+MS.CASpaths["Maple"]+" -q < "+fileName)#TODO:Dictionary Eintrag hier
    
    def createExecutableCode(self,xmlComp,xmlProblemFile):
        """
        This function creates executable Code for the different possible calculations
        listed in the table COMP. The second Argument is the problem file itself.
        """
        comp = COMP(xmlComp)
        result = "";
        problemTree = dom.parse(xmlProblemFile)
        pr = str(problemTree.firstChild.tagName.strip())
        if (pr == "INTPS"):
            result += self.initINTPS(xmlComp,xmlProblemFile)
            result += self._dictCOMPToMaple[comp.getKind()]
            result +="(Ideal, ordering):\n printf(\"%a\",%);\n quit;"
        #TODO:Add further Possible Problem files.
        return result

#####################Class Magma################################################
class CAS_Magma(CAS):

    _dictCOMPToMagma ={
        "GB":"GroebnerBasis",
        "FA":"GroebnerBasis",
        "lp":"lex",
        "dp":"grevlex"
    }#TODO: All in lowercase and change code for that
    
    def __init__(self):
        #first of all: is Magma installed?
        self.__name = "Magma.xml"
        #TODO: TEMPORARYself.__isInstalled = os.system("magma -c quit;")
        #TODO: Version check?
        
    def __del__(self):
        pass
    
    def initData(xmlCOMP,xmlFileName):
        tree = dom.parse(xmlFileName)
        #First Case: INTPS:
        if (str(tree.firstChild.tagName) == "INTPS"):
            return CAS_Magma.initINTPS(xmlCOMP,xmlFileName)
        elif (str(tree.firstChild.tagName) == "FREEALGEBRA"):
            return CAS_Magma.initFREEALGEBRA(xmlCOMP,xmlFileName)
    
    def initINTPS(self,xmlCOMP,xmlFileName):
	intps = INTPS(xmlFileName)
        comp = COMP(xmlCOMP)
        result = ""
        #start with ring definition
        #if there is a Basedomain in the Definition of the COMP-Table given,
        #it will be used for our computations. Otherwise the basedomain in the
        #INTPS Table will be used
        if comp.getCoeff() == None:
            bd = intps.getBaseDomain()
        else:
            bd = comp.getCoeff()
        par = intps.getParameters()
	#Definition of the underlying field	
	result += "K := "
	if (bd == None):
	    result += "RationalField();\n"
	else:
            if CAS.extractCharacteristicFromString(bd)==0:
                result += "RationalField();\n"
            else:
                result += "FiniteField("+ str(CAS.extractCharacteristicFromString(bd)) + ");\n"
        #Are there parameters given?
        if intps.getParameters()==None:
            result += "F:=K;\n"
        else:
            result += "F<"+",".join(str(v) for v in intps.getParameters())+"> := RationalFunctionField(K,"+len(intps.getParameters())+");\n";
	#Definition of the polynomial ring
	tmp = intps.getVars();
	result += "P<"
	result +=",".join(str(v) for v in tmp)
	result +="> := PolynomialRing(F,"+ str(len(tmp)) +");\n";
        result +="I := ideal<P | "+ ",".join(v for v in intps.getBasis()) +">;\n"
        return result;
    
    def initFREEALGEBRA(self,xmlCOMP,xmlFileName):
        fa = FREEALGEBRA(xmlFileName)
        comp = COMP(xmlCOMP)
        result = ""
        #Ring Definition
        if comp.getCoeff() == None:
            bd = fa.getBaseDomain()
        else:
            bd = comp.getCoeff()
        result += "K := "
	if (bd == None):
	    result += "RationalField();\n"
	else:
            if CAS.extractCharacteristicFromString(bd)==0:
                result += "RationalField();\n"
            else:
                result += "FiniteField("+ str(CAS.extractCharacteristicFromString(bd)) + ");\n"
        #Are there parameters given?
        if fa.getParameters()==None:
            result += "F:=K;\n"
        else:
            result += "F<"+",".join(str(v) for v in fa.getParameters())+"> := RationalFunctionField(K,"+str(len(fa.getParameters()))+");\n";
        result += "A<"+",".join(v for v in fa.getVars())+">" #EXAMPLE: A<x,y,z>
        result +=" := FreeAlgebra(F,"+str(len(fa.getVars()))+");\n" #EXAMPLE :=(Rationals(), 3);
        result += "B := [ "+",\n".join(v for v in fa.getBasis())+"];\n" #EXAMPLE B:=[x,y,z]
        return result;
    
    def executeFile(self,fileName):
        """
        Executes Maple with fileName as Input. Time will also be returned
        """
        return commands.getoutput(MS.timeCommand+ " "+  MS.CASpaths["Magma"] + " < "+fileName)
                                                           #TODO: Quiet fuer Magma?
    
    def createExecutableCode(self,xmlComp,xmlProblemFile):
        """
        This function creates executable Code for the different possible calculations
        listed in the table COMP. The second Argument is the problem file itself.
        """
        comp = COMP(xmlComp)
        result = "";
        problemTree = dom.parse(xmlProblemFile)
        pr = str(problemTree.firstChild.tagName.strip())
        if (pr == "INTPS"):
            result += self.initINTPS(xmlComp,xmlProblemFile)
            result +="B := "+self._dictCOMPToMagma[comp.getKind()]+"(I);\nB;\n quit;";
        elif (pr == "FREEALGEBRA"):
            fa = FREEALGEBRA(xmlProblemFile)
            result += self.initFREEALGEBRA(xmlComp,xmlProblemFile)
            result += self._dictCOMPToMagma[comp.getKind()]
            result +="(B,"+str(fa.getUpToDegree())+");\n quit;"
        #TODO:Add further Possible Problem files.
        return result
    
    
#####################Class GAP################################################
class CAS_GAP(CAS):

    _dictCOMPToGAP ={
        "GB":"GroebnerBasis",
        "FA":"SGrobnerTrunc",
        "lp":"MonomialLexOrdering",
        "dp":"MonomialGrlexOrder"
    }#TODO: All in lowercase and change code for that
    
    def __init__(self):
        #first of all: is GAP installed?
        self.__name = "GAP.xml"
        #TODO: TEMPORARYself.__isInstalled = os.system("gap -c quit;")
        #TODO: Version check?
        
    def __del__(self):
        pass
    
    def initData(xmlCOMP,xmlFileName):
        tree = dom.parse(xmlFileName)
        #First Case: INTPS:
        if (str(tree.firstChild.tagName) == "INTPS"):
            return CAS_GAP.initINTPS(xmlCOMP,xmlFileName)
        elif (str(tree.firstChild.tagName) == "FREEALGEBRA"):
            return CAS_GAP.initFREEALGEBRA(xmlCOMP,xmlFileName)
    
    def initINTPS(self,xmlCOMP,xmlFileName):
	intps = INTPS(xmlFileName)
        comp = COMP(xmlCOMP)
        result = ""
        #start with ring definition
        #if there is a Basedomain in the Definition of the COMP-Table given,
        #it will be used for our computations. Otherwise the basedomain in the
        #INTPS Table will be used
        if comp.getCoeff() == None:
            bd = intps.getBaseDomain()
        else:
            bd = comp.getCoeff()
        par = intps.getParameters()
	#Definition of the underlying field	
	result += "K := "
	if (bd == None):
	    result += "Rationals;\n"
	else:
            if CAS.extractCharacteristicFromString(bd) == 0:
                result += "Rationals;\n"
            else:
                result += "GaloisField("+ str(CAS.extractCharacteristicFromString(bd)) + ");\n"
        #Parameters?
        if intps.getParameters() == None:
            result += "F:=K;\n"
        else:
            result += "F := FunctionField(K,["+",".join("\""+str(v)+"\"" for v in intps.getParameters())+"] );\n"
            for i in xrange(0,len(intps.getParameters())):
                result += str(intps.getParameters()[i])+":=IndeterminatesOfFunctionField(F)["+str((i+1))+"];\n"
	#Definition of the polynomial ring
	tmp = intps.getVars();
        result += "PR := PolynomialRing(F,["+",".join(str("\""+v+"\"") for v in tmp)+"]);\n"
        for i in xrange(0,len(tmp)):
            result+= str(tmp[i])+":= IndeterminatesOfPolynomialRing(PR)["+str((i+1))+"];\n"
        result += "I:= Ideal(PR,["+",".join(v for v in intps.getBasis())+"]);\n"
        result += "ord :="+self._dictCOMPToGAP[comp.getOrdering()]+"("+",".join(v for v in tmp)+");\n"
	return result;
    
    def initFREEALGEBRA(self,xmlCOMP,xmlFileName):
        fa = FREEALGEBRA(xmlFileName)
        comp = COMP(xmlCOMP)
        result = ""
        #Ring Definition
        if comp.getCoeff() == None:
            bd = fa.getBaseDomain()
        else:
            bd = comp.getCoeff()
        #######Initialization stuff for GAP##############
        result += "LoadPackage(\"GBNP\",\"0\",false);\n"
        result += "SetInfoLevel(InfoGBNP,1);\n"
        result += "SetInfoLevel(InfoGBNPTime,1);\n"
        #######End Initialization stuff for GAP##########
        tmp = fa.getVars();
        result += "K:="
        if (bd == None):
	    result += "Rationals;\n"
	else:
            if CAS.extractCharacteristicFromString(bd) == 0:
                result += "Rationals;\n"
            else:
                result += "GaloisField("+ str(CAS.extractCharacteristicFromString(bd)) + ");\n"
        #Parameters?
        if fa.getParameters() == None:
            result += "F:=K;"
        else:
            result += "F := FunctionField(K,["+",".join("\""+str(v)+"\"" for v in fa.getParameters())+"] );\n"
            for i in xrange(0,len(fa.getParameters())):
                result += str(fa.getParameters()[i])+":=IndeterminatesOfFunctionField(F)["+str((i+1))+"];\n"
        result += "A := FreeAssociativeAlgebraWithOne(F,"+",".join(str("\""+v+"\"") for v in tmp)+");\n"
        result += "g:=GeneratorsOfAlgebraWithOne(A);\n"
        for i in xrange(0,len(tmp)):
            result += tmp[i]+":=g["+str((i+1))+"];\n"
        #Ideal generation
        result += "weights := ["+",".join("1" for v in tmp)+"];\n" # Weight vector assigning every variable the weight 1
        result += "KI_gp := ["+",".join(v for v in fa.getBasis())+"];\n"
        result += "KI_np :=GP2NPList(KI_gp);\n"
        return result;
    
    def executeFile(self,fileName):
        """
        Executes GAP with fileName as Input. Time will also be returned
        """
        return commands.getoutput(MS.timeCommand+ " "+  MS.CASpaths["GAP"] + " -b < "+fileName)#TODO:Dictionary Eintrag hier
                                                           #TODO: Quiet fuer Magma?
    
    def createExecutableCode(self,xmlComp,xmlProblemFile):
        """
        This function creates executable Code for the different possible calculations
        listed in the table COMP. The second Argument is the problem file itself.
        """
        comp = COMP(xmlComp)
        result = "";
        problemTree = dom.parse(xmlProblemFile)
        pr = str(problemTree.firstChild.tagName.strip())
        if (pr == "INTPS"):
            result += self.initINTPS(xmlComp,xmlProblemFile)
            result +="B := "+self._dictCOMPToGAP[comp.getKind]+"(I,ord);\nB;\n quit;";
        elif (pr == "FREEALGEBRA"):
            fa = FREEALGEBRA(xmlProblemFile)
            result += self.initFREEALGEBRA(xmlComp,xmlProblemFile)
            result += "GB :="+self._dictCOMPToGAP[comp.getKind()]+"(KI_np,"+str(fa.getUpToDegree())+",weights);\n"
            result += "GBNP.ConfigPrint("+",".join(str("\""+v+"\"") for v in fa.getVars())+");\n"
            result += "PrintNPList(GB);\n"
            result += "Length(GB);\n"
            result += "quit;"
        #TODO:Add further Possible Problem files.
        return result

#}

def getCASInstanceByXMLName(name):
    """
    In general, a user just knows the symbolic Data XML-File of a certain
    Computer algebra System. This function gets the name of the CAS as argument,
    and returns an instance of the built-in class as output.
    """
    if (name == "Singular.xml"):
        return CAS_Singular()
    elif (name == "Maple.xml"):
        return CAS_Maple()
    elif (name == "Magma.xml"):
        return CAS_Magma()
    elif (name == "GAP.xml"):
        return CAS_GAP()
    else:
        return None
    #TODO add all the others
