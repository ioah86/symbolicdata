#!/usr/bin/env python
#Author: Albert Heinle
#purpose: After creating a task folder containing different codes for the
#         computer algebra systems, this program serves the purpose to be
#         contained in the folder and to execute the codes on the computer
#         algebra systems.
"""
In an export task folder, this function runs the tasks selected by the user
step by step. The user can specify the maximum CPU-time and the maximum memory usage
his tasks should have. This can be done as following: simply type

python runTasks.py -c86400 -m1024

to ensure that every task will be killed, when it takes more than one day of calculation
or more than 1KB memory.
While the tasks are executed, the user can see the current status in the file proceedings.html,
which can be found in the same folder.
When it is finished, you can also find a RESULTS HTML file in the folder, where the timings for
the different calculations are listed. The output of the computer algebra systems can be found
in the specifix ".res" files.
"""
#INPUT: The User can specify the maximum cpu-time and the maximum memory usage:
from optparse import OptionParser
import sys
import classes
import commands
import os
import time
import resource

parser = OptionParser("runTasks.py -cN -mM , where N and M are numbers")
parser.add_option("-c", "--cputime", dest="maxCPUTime",help="Specify the max. time a CAS should calculate on the given problems")
parser.add_option("-m", "--memoryusage", dest="maxMemUsage", help = "Specify the max. memory (In ) a CAS is allowed to use for the given calculations")

(opts, args) = parser.parse_args()

if(opts.maxMemUsage!=None):
    maxMem = int(opts.maxMemUsage)
else:
    maxMem = None
if (opts.maxCPUTime != None):
    maxCPU = int(opts.maxCPUTime)
else:
    maxCPU = None


def getCPUAndMemoryUsage(pid):
    outp = commands.getoutput("ps -p "+str(pid)+" -o \"cputime rss\"")
    data = outp.split("\n")[1].strip()
    data = filter (lambda a: a != "", data.split())
    timeList = data[0].split(":")
    timeList.reverse()
    time = int(float(timeList[0])) #seconds
    time += int(timeList[1])*60 #Minutes
    tmp = timeList[2].split("-")
    if (len(tmp)==1):
        time+=int(tmp[0])*3600 #hours
    else: #This process runs for a couple of days
        time += int(tmp[1]) * 3600 #hours
        time += int(tmp[0]) * 86400
    return (time, int(data[1]))

xmlFilesInDirectory = filter(lambda a: a.endswith(".xml"),os.listdir(os.getcwd())) # Takes all Files ending with .xml from the current directory
if len(xmlFilesInDirectory) !=1:
    print "There is no unique Task XML-File in the current directory"
    sys.exit(-1)
taskFile = xmlFilesInDirectory[0]
task = classes.Task(taskFile)

def updateProceedings():
    #####
    #Uptdate .html file
    ####
    file = open("proceedings.html","w")
    file.write(task.getProceedingsTable())
    file.close()
    ####

def runTasks(task):
    """
    INPUT: A task specified in the classes.py file
    Purpose: Writes the results of the computations in the current folder.
    """
    #problems    = task.getProblemList()
    #CASList     = task.getCasList()
    computation = task.getCOMP()
    while(task.getWaitingCalculations() != []):
        #for cas in CASList:
        w = task.setRunCalculation()
        updateProceedings()
        fileName    = w[0].strip()+computation.strip()+w[1].strip()
        timeStamp   = time.strftime("%Y_%m_%d_%H_%M_%S",time.gmtime())
        pid = os.fork()
        if (pid == 0): #Process, which starts the computeralgebra system (Child)
            if (maxCPU != None):
                resource.setrlimit(resource.RLIMIT_CPU,(maxCPU,maxCPU))
            if (maxMem != None):
                resource.setrlimit(resource.RLIMIT_DATA,(maxMem,maxMem))
            curCAS = classes.getCASInstanceByXMLName(w[0].strip())
            result = curCAS.executeFile(fileName + ".sdc")
            #TODO: Maybe write in new Directory?
            file = open(fileName+timeStamp+".res","w")
            file.write(result)
            file.close()
            os._exit(0) # TODO: Errors can occur in the previous command
        else: #fatherprocess
            #os.waitpid(pid, os.WNOHANG)
            os.wait()
            timeandoutput = evaluateOutput(fileName+timeStamp+".res")
            task.setRunCalculationCompleted(timeandoutput)
    updateProceedings()
    task.createResultsFile()

def evaluateOutput(outpfile):
    file = open(str(outpfile),"r")
    outp = file.read()
    file.close()
    result = filter(lambda a: str(a) != "",outp.split("\n"))
    timeResults = result[-3:] #Last three entries are the time entries
    timeResults = map(lambda a: str(a).split("\t")[1],timeResults) #We don't want the strings like real, user, sys. Just the time.
    casOutput = "".join(v for v in result[:-3])
    return timeResults+[casOutput]

runTasks(task)