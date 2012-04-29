#!/usr/bin/env python
# @author: Albert Heinle


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
