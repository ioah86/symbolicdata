#!/usr/bin/env python
# @author: Albert Heinle

import xml.dom.minidom as dom
import MachineSettings as MS
import commands
from CAS import CAS
from ..datamanagement.COMP import COMP
from ..datamanagement.INTPS import INTPS
from ..datamanagement.FREEALGEBRA import FREEALGEBRA

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
    
