#!/usr/bin/env python
# @author: Albert Heinle

import xml.dom.minidom as dom
import MachineSettings as MS
import commands
from CAS import CAS
from ..datamanagement.COMP import COMP
from ..datamanagement.INTPS import INTPS
from ..datamanagement.FREEALGEBRA import FREEALGEBRA

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
        """
        Input: A Polynomial (Freealgebra) in the MAGMA-Style, and the variables
               in the corresponding free algebra
        Output: A Polynomial in the Letterplace Style (with their positions as
                arguments)
        """
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
            result += "(I);\n"
            result += "print (J, \"%s\");$"
        #TODO:Add further Possible Problem files.
        return result
