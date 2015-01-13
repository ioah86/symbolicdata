"""
Once a Taskfolder is created, one can run this file to execute the tasks in this folder.

In a task folder, this function runs the tasks selected by the user
step by step. The user can specify the maximum CPU-time and the maximum memory usage
his tasks should have. Furthermore, the user can specify how many programs can be run in parallel.

This can be done as follows: simply type

python runTasks.py -c86400 -m1024 -j4

to ensure that every task will be killed, when it takes more than one day of calculation
or more than 1KB memory. During the execution of runTasks, 4 computations will be run in parallel.

.. moduleauthor:: Albert Heinle <albert.heinle@rwth-aachen.de>
"""

import os
import sys

#--------------------First we check, if we are in a TaskFolder --------------------
tfPath = os.path.realpath(os.path.dirname(__file__))
if not os.path.isdir(os.path.join(tfPath,"casSources")) or \
    not os.path.isfile(os.path.join(tfPath,"taskInfo.xml")) or \
    not os.path.isfile(os.path.join(tfPath,"machinesettings.xml")):
    print "You must create a taskfolder and then run this command from there.\n\
See create_tasks_gui.py!"
    sys.exit(-1)
#--------------------Check completed  ------------------------------

from optparse import OptionParser
import time
import shutil
import resource
import commands
from classes.MachineSettingsFromXMLBuilder import MachineSettingsFromXMLBuilder
from classes.TaskFromXMLBuilder import TaskFromXMLBuilder
from classes.results.Proceedings import Proceedings
from classes.results.ResultedTimings import ResultedTimings
from classes.results.ProceedingsToHTMLWriter import ProceedingsToHTMLWriter
from classes.results.ProceedingsToXMLWriter import ProceedingsToXMLWriter
from classes.results.ResultedTimingsToHTMLWriter import ResultedTimingsToHTMLWriter
from classes.results.ResultedTimingsToXMLWriter import ResultedTimingsToXMLWriter
from classes.results.ResultingFileFromOutputBuilder import ResultingFileFromOutputBuilder

#-------------------- Checking the user arguments ----------------------------
parser = OptionParser("runTasks.py -cN -mM -jP, where N, M and P are positive integers")
parser.add_option("-c", "--cputime", dest="maxCPUTime",help="Specify the max. time a CAS should calculate on the given problems in seconds")
parser.add_option("-m", "--memoryusage", dest="maxMemUsage", help = "Specify the max. memory (in bytes) a CAS is allowed to use for the given calculations")
parser.add_option("-j", "--jobs", dest="numberOfJobs", help = "Specify the max. number of computations that should be run in parallel")

(opts, args) = parser.parse_args()

if(opts.maxMemUsage!=None):
    maxMem = int(opts.maxMemUsage)
else:
    maxMem = None
if (opts.maxCPUTime != None):
    maxCPU = int(opts.maxCPUTime)
else:
    maxCPU = None
if (opts.numberOfJobs!=None):
    maxJobs = int(opts.numberOfJobs)
else:
    maxJobs = 1
#-------------------- Done Checking user arguments --------------------
#-------------------- Making the results here      --------------------

#Creating the results-folder
timeStamp   = time.strftime("%Y_%m_%d_%H_%M_%S",time.gmtime())
if not os.path.isdir(os.path.join(tfPath,"results")):
    os.mkdir(os.path.join(tfPath,"results"))

#make the timestamp folder to save the results there
os.mkdir(os.path.join(tfPath,"results",timeStamp))
resultsFolder = os.path.join(tfPath,"results",timeStamp)

#posting the machine-information into the folder
shCommandGetCPUInfo = "sysctl -a | grep \"cpu\""
shCommandGetMemInfo = "sysctl -a | grep \"mem\""
shCommandGetOSInfo  = "sysctl -a | grep \"os\""
curMachineCPUInfo  = commands.getoutput(shCommandGetCPUInfo)
curMachineMemInfo  = commands.getoutput(shCommandGetMemInfo)
curMachineOSInfo   = commands.getoutput(shCommandGetOSInfo)
f = open(os.path.join(tfPath,"results",timeStamp,"cpuInfo.txt"),"w")
f.write("The CPU-information has been acquired via the command 'sysctl -a | grep \"cpu\"'\n")
f.write(curMachineCPUInfo)
f.close()
f = open(os.path.join(tfPath,"results",timeStamp,"memInfo.txt"),"w")
f.write("The memory-information has been acquired via the command 'sysctl -a | grep \"mem\"'\n")
f.write(curMachineMemInfo)
f.close()
f = open(os.path.join(tfPath,"results",timeStamp,"osInfo.txt"),"w")
f.write("The OS-information has been acquired via the command 'sysctl -a | grep \"os\"'\n")
f.write(curMachineOSInfo)
f.close()

#posting the information about the parameters in the running script into the folder


#copying the default css for the proceedings and resultedTimings
shutil.copyfile(os.path.join(tfPath,"classes","results", "proceedings_css.css"),os.path.join(tfPath,"results",timeStamp,"proceedings_css.css"))

#getting the machine settings
f = open(os.path.join(tfPath,"machinesettings.xml"))
msc = MachineSettingsFromXMLBuilder()
ms  = msc.build(f.read())
f.close()

#getting the task
f = open(os.path.join(tfPath,"taskInfo.xml"))
tc = TaskFromXMLBuilder()
t  = tc.build(f.read())
f.close()

#creating the instance of proceedings
proceedings = Proceedings(t,timeStamp)

#creating the instance of ResultedTimings
rt = ResultedTimings(proceedings)

#creating all subfolders
#shutil.copytree(os.path.join(tfPath,"casSources"),os.path.join(resultsFolder,"resultFiles")) OLD VERSION
#We only want to copy those files, which appear in the taskInfo.xml
os.mkdir(os.path.join(resultsFolder,"resultFiles"))
for i in t.getProblemInstances():
    shutil.copytree(os.path.join(tfPath,"casSources",i), os.path.join(resultsFolder,"resultFiles",i))

#Creating the Proceedings Writers
proceedingsHTMLWriter = ProceedingsToHTMLWriter()
proceedingsXMLWriter  = ProceedingsToXMLWriter()
rttoHTMLWriter        = ResultedTimingsToHTMLWriter()
rttoXMLWriter         = ResultedTimingsToXMLWriter()

def update():
    proceedingsXMLFile = open(os.path.join(resultsFolder,"proceedings.xml"),"w")
    proceedingsHTMLFile = open(os.path.join(resultsFolder,"proceedings.html"),"w")
    rtXMLFile = open(os.path.join(resultsFolder,"resultedTimings.xml"),"w")
    rtHTMLFile = open(os.path.join(resultsFolder,"resultedTimings.html"),"w")
    proceedingsXMLFile.write(proceedingsXMLWriter.createXMLFromProceedings(proceedings).toprettyxml())
    proceedingsHTMLFile.write(proceedingsHTMLWriter.createHTMLFromProceedings(proceedings))
    rtXMLFile.write(rttoXMLWriter.createXMLFromResultedTimings(rt).toprettyxml())
    rtHTMLFile.write(rttoHTMLWriter.createHTMLFromResultedTimings(rt))
    proceedingsXMLFile.close()
    proceedingsHTMLFile.close()
    rtXMLFile.close()
    rtHTMLFile.close()

update()

rfBuilder = ResultingFileFromOutputBuilder()

availProc = maxJobs
runningDict = {}
while proceedings.getWAITING() != [] or proceedings.getRUNNING() != []:
    while (proceedings.getWAITING() !=[]) and (availProc >0):
        availProc -= 1
        curCalc = rt.getWAITING()[0]
        rt.setRUNNING(curCalc)
        update()
        pid = os.fork()
        if (pid == 0): #Process, which starts the computeralgebra system (Child)
            if (maxCPU != None):
                resource.setrlimit(resource.RLIMIT_CPU,(maxCPU,maxCPU))
            if (maxMem != None):
                resource.setrlimit(resource.RLIMIT_DATA,(maxMem,maxMem))
            filename = os.path.join(tfPath,"casSources",curCalc[0],curCalc[1],"executablefile.sdc")
            result = commands.getoutput(ms.getTimeCommand()+ " -p "+ms.getCASCommand(curCalc[1])+"< "+filename)
            file = open(os.path.join(resultsFolder,"resultFiles",curCalc[0],curCalc[1],"outputFile.res"),"w")
            file.write(result)
            file.close()
            os._exit(0)
        else:
            runningDict[pid] = curCalc
    #fatherprocess
    pid = None
    while not (pid in runningDict): #Certain processes can be just the CASs.
        pid, sign = os.waitpid(0,0)
    curCalc = runningDict[pid]
    availProc +=1
    del runningDict[pid]
    file = open(os.path.join(resultsFolder,"resultFiles",curCalc[0],curCalc[1],"outputFile.res"))
    resultingFile = rfBuilder.build(curCalc[0],curCalc[1],file.read())
    file.close()
    if os.path.isfile(os.path.join(tfPath,"casSources",curCalc[0],curCalc[1],"template_sol.py")):
        sys.path.append(os.path.join(tfPath,"casSources",curCalc[0],curCalc[1]))
        import template_sol
        reload(template_sol) #(makes sure that the changes are applied)
        solext = template_sol.extractSolution
        try:
            resInXML = solext(resultingFile.getCASOutput())
            resXMLFile =\
                open(os.path.join(resultsFolder,
                                  "resultFiles",
                                  curCalc[0],
                                  curCalc[1],
                                  "solutionInXML.xml"),"w")
            resXMLFile.write(resInXML)
            resXMLFile.close()
            rt.setCOMPLETED(curCalc, resultingFile.getTimes())
        except:
            rt.setERROR(curCalc,resultingFile.getTimes())
        sys.path.remove(os.path.join(tfPath,"casSources",curCalc[0],curCalc[1]))
    else:
        #in this case, we cannot say anything about the
        #output. Therefore we assume, that it just completed as expected.
        rt.setCOMPLETED(curCalc,resultingFile.getTimes())
    update()

update()
