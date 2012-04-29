#!/usr/bin/env python
# @author: Albert Heinle

import xml.dom.minidom as dom
import os

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
