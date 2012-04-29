#!/usr/bin/env python
# @author: Albert Heinle

import xml.dom.minidom as dom
import os

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

