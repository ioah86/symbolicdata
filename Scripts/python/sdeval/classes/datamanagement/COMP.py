#!/usr/bin/env python
# @author: Albert Heinle

import xml.dom.minidom as dom
import os

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
