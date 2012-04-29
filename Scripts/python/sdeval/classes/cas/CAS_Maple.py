#!/usr/bin/env python
# @author: Albert Heinle

import xml.dom.minidom as dom
import MachineSettings as MS
import commands
from CAS import CAS
from ..datamanagement.COMP import COMP
from ..datamanagement.INTPS import INTPS
from ..datamanagement.FREEALGEBRA import FREEALGEBRA

class CAS_Maple(CAS):

    _dictCOMPToMaple ={
        "GB":"Basis",
        "FA":"",#NOT AVAILABLE
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
