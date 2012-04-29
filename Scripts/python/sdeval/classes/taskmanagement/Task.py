#!/usr/bin/env python
# @author: Albert Heinle

import xml.dom.minidom as dom
import os

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
