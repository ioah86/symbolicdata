#!/usr/bin/env python
#@author: Albert Heinle

"""
This module contains routines for creating tasks which will then be run on another machine.
This file expects a path for the XML-Data of the symbolic data project as parsing argument.
After that the interactive user mode will be started, where a user can decide which calculation
he wants to perform on which computer algebra system with which input data. After that,
an export folder will be created. For details read the descriptions of the particular functions.
"""

#Initialization Stuff
import xml.dom.minidom as dom
from optparse import OptionParser
from os import listdir as ls
import os
from classes.taskmanagement.Task import Task
from classes.cas import getCASInstanceByXMLName
import sys
import shutil

parser = OptionParser("create_tasks.py [options] Arguments")
parser.add_option("-s", "--source", dest="xmldatapath", help="The complete path to XML-Data")
                                                        #We need the loacation
                                                        #of our XML-Data
(opts, args) = parser.parse_args()

if (len(args) == 0): # We need at least one argument
    print "This program needs at least one argument"
    sys.exit(-2)

xmlDataPath = os.path.realpath(args[0])

#For now, the following list contains different calculation options.
#TODO for the future: Extend symbolic data with them
suppCalculations = filter(lambda a: a.endswith(".xml"),ls(os.path.join(xmlDataPath,"COMP")))
suppProblemClasses = ["INTPS","FREEALGEBRA"]


##And we need a global tree, where all tasks can be saved.
taskTree = dom.Document();

def interactiveUserMode():
    """
    In this function a user can create a Task to compute. First he chooses the
    type of calculation (e.g. Groebner Basis calc), afterwards the data the
    computations should be run at and at the end the computeralgebra systems,
    where the computations has to be executed.
    """
    operation = raw_input("What operation do you want to execute? ")
    while suppCalculations.count(operation) == 0:
        print "Possible inputs:"
        print "\n".join(el for el in suppCalculations)
        operation = raw_input("Choose your operation: ")
    problemClass = raw_input("Choose the table of problems you want to execute your operation with? ")
    while suppProblemClasses.count(problemClass) == 0:
        print "Possible inputs:"
        print "\n".join(el for el in suppProblemClasses)
        problemClass = raw_input("Choose your table: ")
    problemList = filter(lambda a: a.endswith(".xml"),ls(os.path.join(xmlDataPath,problemClass)))
    problems = []
    flag = True
    while (flag):
        problem = raw_input("Now choose a concrete problem you wish to deal with: ")
        while problemList.count(problem) == 0:
            print "Possible inputs:"
            print "\n".join(el for el in problemList)
            problem = raw_input("Choose your problem: ")
        problems.append(problem)
        tmp = raw_input("Type \"y\" if you want to add further problems: ")
        if tmp !="y":
            flag = False
    #CAS = raw_input("On which computer algebra system do you want to execute your calculation? ")
    casList = filter(lambda a: a.endswith(".xml"),ls(os.path.join(xmlDataPath , "CAS")))
    CASs = []
    flag = True
    while (flag):
        CAS = raw_input("On which computer algebra system do you want to execute your calculation? ")
        while casList.count(CAS) == 0:
            print "Possible inputs:"
            print "\n".join(el for el in casList)
            CAS = raw_input("Choose your computer algebra system: ")
        CASs.append(CAS)
        tmp = raw_input("Type \"y\" if you want to add further computer algebra systems: ")
        if tmp !="y":
            flag = False
    fileName = raw_input("Choose a file name where this task should be saved: ")
    if (not fileName.endswith(".xml")):
        fileName = fileName+".xml"
    #file = open(fileName,"w")
    fillTaskTree(fileName, operation, problemClass, problems,CASs)
    #taskTree.writexml(file, "", "", "\n")
    #file.close()
    
def fillTaskTree(fileName, operation, problemClass, problems, compalgsystems):
    """
    This function gets a file name, an operation and a list of problems and
    computer algebra systems where these problems have to be solved. At the end,
    the global variable Tasktree is filled with the input data
    """
    taskTree.appendChild(taskTree.createElement(fileName))
    tmpNode = taskTree.firstChild
    #Add the operation Node
    tmpNode.appendChild(taskTree.createElement("COMP"))
    tmpNode.firstChild.appendChild(taskTree.createTextNode(operation))
    #Add the problems to solve
    tmpNode.appendChild(taskTree.createElement("problems"))
    tmpNode = tmpNode.getElementsByTagName("problems")[0]
    for p in problems:
        tmpChild = tmpNode.appendChild(taskTree.createElement(problemClass))
        tmpChild.appendChild(taskTree.createTextNode(p))
    #Add the computer algebra systems of choice
    tmpNode = taskTree.firstChild
    tmpNode.appendChild(taskTree.createElement("CASs"))
    tmpNode = tmpNode.getElementsByTagName("CASs")[0]
    for cas in compalgsystems:
        tmpChild = tmpNode.appendChild(taskTree.createElement("CAS"))
        tmpChild.appendChild(taskTree.createTextNode(cas))
    #Save this file to .xml
    #return taskTree.toprettyxml()
    
def createExportTaskFolder(dest = None):
    """
    Output: Creates folder containing
            -   runnable code for the different CAS for the specific problems
            -   the xml-File with the problems itself
            -   An executable python file that starts the computations.
    """
    sdevaldir = os.getcwd()
    if dest != None:
        os.chdir(dest)
    #Make the directory that will be copied to another machine
    #taskTree = dom.parse("taskSingularMaple.xml") # TODO: ERASE THAT
    fileName = str(taskTree.firstChild.tagName)
    if not os.path.isdir(fileName+"EXPORTFOLDER"):
        os.mkdir(fileName+"EXPORTFOLDER")
    os.chdir(fileName+"EXPORTFOLDER")
    #copy the XML-Tree to this directory
    file = open(fileName,"w")
    taskTree.writexml(file, "", "", "\n")
    file.close()
    #runnable CAS-Code
    task = Task(fileName)
    for cas in task.getCasList():
        tmpCAS = getCASInstanceByXMLName(cas)
        for prob in task.getProblemList():
            tmpCode = tmpCAS.createExecutableCode(os.path.join(xmlDataPath,"COMP",task.getCOMP()),os.path.join(xmlDataPath,prob.tagName,prob.firstChild.data.strip()))
            #fileName CAS+PROBLEM+COMP+.txt
            file = open(cas+task.getCOMP()+prob.firstChild.data.strip()+".sdc","w") # .sd stands for symbolic Data Code
            file.write(tmpCode);
            file.close();
    shutil.copy(os.path.join(sdevaldir,"runTasks.py"),os.getcwd())
    shutil.copytree(os.path.join(sdevaldir,"classes"),os.path.join(os.getcwd(),"classes"))
    shutil.copy(os.path.join(sdevaldir,"MachineSettings.py"),os.getcwd())    
    

interactiveUserMode()

createExportTaskFolder()

#TODO: Eventuell noch irgendwo einfuegen, was fuer ein Encoding das Teil ist.