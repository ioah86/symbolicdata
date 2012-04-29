#!/usr/bin/env python
# @author: Albert Heinle

import xml.dom.minidom as dom
import MachineSettings as MS
import commands
from CAS import CAS
from ..datamanagement.COMP import COMP
from ..datamanagement.INTPS import INTPS
from ..datamanagement.FREEALGEBRA import FREEALGEBRA

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
            result +="B := "+self._dictCOMPToGAP[comp.getKind()]+"(I,ord);\nB;\n quit;";
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
