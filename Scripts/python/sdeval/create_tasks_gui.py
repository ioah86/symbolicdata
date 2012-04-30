#!/usr/bin/env python
# -*- coding: iso-8859-1 -*-
#@author: Albert Heinle

"""
The GUI for SDEVAL

Here, the user can create a task via a graphical user interface. The idea is the
following:
At first, he decides which kind of problem he wants to deal with. By now, we have
the following options:
 - Groebner basis commutative ring.
 - Groebner basis in free algebra.
 - Factorization of Polynomials in the first Weyl Algebra.
In the same window, the user will also clearify, whether he wants to work over a
finite field or just use the settings given in the problems.

After that, he chooses concrete Problems from the database of Symbolicdata.
The program will use the tables corresponding to the given problems.

In the End, the user specifies, which computer algebra system he or she wants to
use. By now, we offer the choice between
 - Singular
 - Maple
 - Maple
 - GAP

With some machine settings the user should set, the creation of the task can start
and there will be a folder created in the end that contains code for the different
computer algebra systems.
"""
import os # This is for the check if the path does exist in the next step
import shutil
#### Our Machine Settings
import MachineSettings as MS
from classes.taskmanagement.Task import Task
from classes.cas import getCASInstanceByXMLName
#### GUI Stuff
import Tkinter
import tkMessageBox
import tkFileDialog
import xml.dom.minidom as dom


################################################################################
#First of all, check, if the directory with the XMLRessources of Symbolicdata
#does exist in the expected path "../../../OWLData/XMLResources/". If not, the
#user will be asked later for the path.
isXMLRessourcesDirectory = \
    os.path.isdir(os.path.join("..","..","..","OWLData","XMLResources"))
    # To make it more platform independent. What stands here would be in unix terms
    #../../../OWLData/XMLResources.

xmlDataPath = None
if (isXMLRessourcesDirectory):
  xmlDataPath = os.path.realpath(os.path.join("..","..","..","OWLData","XMLResources"))

################################################################################
### some Global stuff
taskTree = dom.Document()

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

################################################################################
#Lets start with the gui itself.

class CreateTasksGui:
  def __init__(self):
    self.createMainWindow()
    self.createMainMenu()
    self.createMainFrame()
    self.createWindowProblemSelect()
    self.currentWindow = "ProblemSelect"# Other possibilities are TableSelect and CASSelect
    self.checkXMLRessourcesDir()
    self.input_operation = None
    self.input_problemClass = None
    self.input_problems = []
    self.input_compAlgSystems = []
    #self.createTableSelect()
    #self.createCASSelect()
    Tkinter.mainloop()
    
    
  ##################################################
  ###### Initialization Stuff
  ##################################################
  def createMainWindow(self):
    self.mainWindow = Tkinter.Tk()
    #self.mainWindow.resizable(width = False, height = False)
    self.mainWindow.title("SDEval -- Create Tasks")
  
  def createMainMenu(self):
    self.menuBar = Tkinter.Menu(self.mainWindow)
    self.helpMenu = Tkinter.Menu(self.menuBar,tearoff=0)
    self.helpMenu.add_command(label="About SDEval", command=self.thanksPopup)
    self.menuBar.add_cascade(label="Help",menu=self.helpMenu)
    self.mainWindow.config(menu=self.menuBar)
  
  def thanksPopup(self):
    """
    In the top menubar, there is an option "About SDEval". If you click on it, a
    popup will show up with an information about the project. The showing of the
    popup is made by this window.
    """
    tkMessageBox.showinfo("About SDEVAL", "SDEval is developed at \
Lehrstuhl D für Mathematik, RWTH Aachen University.\
\n\nSpecial thanks to DFG (Deutsche Forschungs Gesellschaft)\
who funded the project at the project Schwerpunkt 1489")
  
  def createMainFrame(self):
    self.mainFrame=Tkinter.Frame(self.mainWindow)
    self.mainFrame.grid();
    
  def checkXMLRessourcesDir(self):
    global xmlDataPath
    validDir = False
    while not validDir:
      validDir = True
      if not xmlDataPath:
        xmlDataPath = tkFileDialog.askdirectory(mustexist=True)
      if (not os.path.isdir(os.path.join(xmlDataPath,"INTPS"))) or\
      (not os.path.isdir(os.path.join(xmlDataPath,"COMP"))) or\
      (not os.path.isdir(os.path.join(xmlDataPath,"FREEALGEBRA"))) or\
      (not os.path.isdir(os.path.join(xmlDataPath,"CAS"))):
        validDir = False
        xmlDataPath = None
    
  def fillListOfProblems(self):
    """
    In the second window, where the user chooses concrete problems he wants to
    deal with, this method fills the list of entries in the listbox.
    """
    global xmlDataPath
    problemList = filter(lambda a: a.endswith(".xml"),os.listdir(os.path.join(xmlDataPath,self.input_problemClass)))
    for entry in problemList:
      self.lstbx_allProblems.insert(Tkinter.END,entry)
    if len(problemList) != 0:
      self.lstbx_allProblems.select_set(0)
  
  def initCASselect(self):
    #Fill the machine settings
    self.entry_GAP.insert(Tkinter.END, MS.CASpaths["GAP"])
    self.entry_Magma.insert(Tkinter.END,MS.CASpaths["Magma"])
    self.entry_Maple.insert(Tkinter.END,MS.CASpaths["Maple"])
    self.entry_Singular.insert(Tkinter.END,MS.CASpaths["Singular"])
    self.entry_Time.insert(Tkinter.END,MS.timeCommand)
    #check whether the Computer Algebra systems can handle the current problem:
    if self.input_operation=="FA_Q_dp.xml":
      self.cb_Maple.config(state = Tkinter.DISABLED)
    
  ##################################################
  #### Button Behaviours
  ##################################################
  
  def btnNextBehaviour(self):
    if (self.currentWindow == "ProblemSelect"):
      """
      User was in the first window, selected a problem and wants now to the tables
      to choose concrete instances.
      """
      #########
      #Read the entries and fill the variables with it
      if self.v.get() == "FA":
        self.input_operation = "FA_Q_dp.xml"
        self.input_problemClass = "FREEALGEBRA"
      elif self.v.get() == "GB":
        self.input_problemClass = "INTPS"
        if self.v2.get() == "Yes":
          self.input_operation = "GB_Fp_dp.xml"
        else:
          self.input_operation = "GB_Z_lp.xml"
        
      #########
      #Creating the new window
      self.currentWindow = "TableSelect"
      self.mainFrame.destroy()
      self.createMainFrame()
      self.createTableSelect()
      self.fillListOfProblems()
    else:
      """
      The only other possibility is that the user is at the second window, and wants
      to move on to the third.
      """
      if self.lstbx_chosenProblems.size()<1:
        #Error message if the user has not selected a problem at all!
        tkMessageBox.showerror(title = "No Problem selected", message = "You have to choose at least one problem instance!")
      else:
        #######
        #Read entries and fill variables
        self.input_problems = self.lstbx_chosenProblems.get(0,Tkinter.END)
        ######
        #Create the new window
        self.currentWindow = "CASSelect"
        self.mainFrame.destroy()
        self.createMainFrame()
        self.createCASSelect()
        self.initCASselect()
      
  #def btnBackBehaviour(self):
  #  """
  #  There is only one window that offers to go back, namely the last one where the user
  #  specifies his machine settings and the computer algebra Systems he wants to use. Therefore
  #  just the window with the TableSelect should be opened.
  #  """
  #  self.currentWindow = "TableSelect"
  #  self.mainFrame.destroy()
  #  self.createMainFrame()
  #  self.createTableSelect()
  #  #TODO: Voreingestellte Werte hier einfügen.
  
  def makeCASList(self):
    """
    In the last window, we have some computer algebra systems to select. This method
    returns a list of the selected Computer Algebra Systems.
    """
    result = []
    if self.var_GAP.get() == "Yes":
      result.append("GAP.xml")
    if self.var_Magma.get() == "Yes":
      result.append("Magma.xml")
    if self.var_Maple.get() == "Yes":
      result.append("Maple.xml")
    if self.var_Singular.get() == "Yes":
      result.append("Singular.xml")
    return result
  
  def btnCreateClick(self):
    #First, some checks if the Entries given by the user are valid
    ourCASs = self.makeCASList()
    if self.entry_taskName.get().strip() == "":
      tkMessageBox.showerror(title = "No Taskname given", message="Your task must have a name.")
    elif len(ourCASs)==0:
      tkMessageBox.showerror(title = "No Computer Algebra System selected", message="You have to select at least one computer algebra system")
    else:
      #Everything is fine. Start creating the Export Task folder
      exportFolder = tkFileDialog.askdirectory(mustexist = True, title = "Choose a directory where the Export Folder should be placed at.")
      fillTaskTree(self.entry_taskName.get().strip()+".xml",self.input_operation,self.input_problemClass,self.input_problems,ourCASs)
      createExportTaskFolder(exportFolder)
      tkMessageBox.showinfo(title="Successful", message = "The task was successfully created.")
      self.mainWindow.destroy()
    
  def btnAddClick(self):
    """
    This method deals with the event, that the user adds a problem to his list
    of chosen problems.
    """
    if self.lstbx_allProblems.size()>0:
      #Add just makes sense if the size of the problem list is greater than 0
      self.lstbx_chosenProblems.insert(Tkinter.END,self.lstbx_allProblems.get(self.lstbx_allProblems.curselection()[0]))
      self.lstbx_allProblems.delete(self.lstbx_allProblems.curselection()[0])
      if self.lstbx_allProblems.size()>0:
        self.lstbx_allProblems.select_set(0)
  
  def btnRemoveClick(self):
    """
    If a problem in the current problem list is not that interesting how it seemed before
    the usere presses the button "remove" and this method will delete it from the list
    """
    if self.lstbx_chosenProblems.size()>0:
      if len(self.lstbx_chosenProblems.curselection())>0:
        self.lstbx_allProblems.insert(Tkinter.END,self.lstbx_chosenProblems.get(self.lstbx_chosenProblems.curselection()[0]))
        self.lstbx_chosenProblems.delete(self.lstbx_chosenProblems.curselection()[0])
  
  ##################################################
  #### Events
  ##################################################
  def listBoxAllProblemsClicked(self,event):
    """
    Here, if you click on a problem on a listbox, you will get a preview on the screen to see whether it is interesting
    for you or not.
    """
    global xmlDataPath
    if self.lstbx_allProblems.size()>0:
      if len(self.lstbx_allProblems.curselection())>0:
        self.txt_preview.delete(1.0, Tkinter.END)
        filePath = os.path.join(xmlDataPath, self.input_problemClass, self.lstbx_allProblems.get(self.lstbx_allProblems.curselection()[0]))
        problemFile = open(filePath)
        problemFileContent = problemFile.read()
        self.txt_preview.insert(Tkinter.END,problemFileContent)
  
  
  ##################################################
  #### Input Cheking in the Windows
  ##################################################
  
  
  ##################################################
  #### Creation of the different Windows
  ##################################################
  def createWindowProblemSelect(self):
    """
    This is the first window the user is about to see. Here he decides what kind
    of calculations he wants to perform. By now, he has the selection between
    - Gröbner Bases in a commutative Ring
    - Gröbner Bases in the free algebra
    - Factorization of polynomials in the first Weyl Algebra
    Furthermore, he can decide whether his basering has finite charakteristic or not.
    The next button leads to the selection of concrete problems written down in different
    tables in the SymbolicData database.
    """
    self.mainWindow.geometry("%dx%d%+d%+d" % (250, 200, 40, 40))
    #top left corner there is the text labeled by "problem"
    self.lbl_Problem = Tkinter.Label(self.mainFrame, text="Problem:")
    self.lbl_Problem.grid(row=0,columnspan = 2,sticky=Tkinter.W)
    #Now a radio button group with groebner and not Groebner
    self.v = Tkinter.StringVar()
    self.v.set("GB")
    self.rb_groebnerCommutative = Tkinter.Radiobutton(self.mainFrame,text = u"Gröbner Basis Commutative", variable = self.v, value="GB")
    self.rb_groebnerCommutative.grid(row=1, columnspan = 2, sticky = Tkinter.W)
    self.rb_groebnerCommutative.select() # This is the default selected Button
    self.rb_groebnerFreeAlgebra = Tkinter.Radiobutton(self.mainFrame,text = u"Gröbner Basis Free Algebra", variable = self.v, value="FA")
    self.rb_groebnerFreeAlgebra.grid(row = 2, columnspan = 2, sticky = Tkinter.W)
    self.rb_FactorWeyl = Tkinter.Radiobutton(self.mainFrame,text = "Factorization First Weyl Algebra", variable = self.v, value="Factorize")
    self.rb_FactorWeyl.grid(row=3,  columnspan = 2,sticky = Tkinter.W)
    #And now the finite field discussion
    self.lbl_FiniteField = Tkinter.Label(self.mainFrame,text = "Finite field?")
    self.lbl_FiniteField.grid(row=4, columnspan = 2, sticky = Tkinter.W)
    self.v2 = Tkinter.StringVar()
    self.v2.set("No")
    self.rb_notFiniteField = Tkinter.Radiobutton(self.mainFrame,text = "No.", variable = self.v2, value = "No")
    self.rb_notFiniteField.select()
    self.rb_notFiniteField.grid(row=5, columnspan = 2, sticky=Tkinter.W)
    self.rb_finiteField = Tkinter.Radiobutton(self.mainFrame,text = "Yes", variable = self.v2, value = "Yes")
    self.rb_finiteField.grid(row = 6, column=0, sticky = Tkinter.W)
    #self.entry_characteristic = Tkinter.Entry(self.mainFrame, state = Tkinter.DISABLED)
    #self.entry_characteristic.config(width=6)
    #self.entry_characteristic.grid(row = 6, column = 1, sticky=Tkinter.E)
    #Next Button
    self.btn_next = Tkinter.Button(self.mainFrame,text="Next",command = self.btnNextBehaviour)
    self.btn_next.grid(row = 7, column = 1, sticky=Tkinter.E)
    
  def createTableSelect(self):
    self.mainWindow.geometry("%dx%d%+d%+d" % (575, 625, 40, 40))
    #upper label
    self.lbl_concreteProblems = Tkinter.Label(self.mainFrame, text = "Concrete Problems")
    self.lbl_concreteProblems.grid(row = 0, columnspan = 3)
    #listbox containing all problems
    self.lstbx_allProblems = Tkinter.Listbox(self.mainFrame)
    self.lstbx_allProblems.bind("<Double-Button-1>", self.listBoxAllProblemsClicked)
    self.lstbx_allProblems.grid(row = 1, column = 0, rowspan = 2 ,sticky = Tkinter.W)
    #The button with whome the user can add the problems to the list.
    self.btn_add = Tkinter.Button(self.mainFrame,text = "Add->",command=self.btnAddClick)
    self.btn_add.grid(row = 1, column = 1)
    #The button with whome the user can remove things from the right hand side list.
    self.btn_remove = Tkinter.Button(self.mainFrame,text = "<-Remove",command = self.btnRemoveClick)
    self.btn_remove.grid(row = 2, column = 1)
    #The list with chosen problems
    self.lstbx_chosenProblems = Tkinter.Listbox(self.mainFrame)
    self.lstbx_chosenProblems.grid(row = 1,column = 2, rowspan = 2, sticky = Tkinter.E)
    #The label of the priview window.
    self.lbl_preview = Tkinter.Label(self.mainFrame, text = "Preview:")
    self.lbl_preview.grid(row = 3, columnspan = 3)
    #The preview textbox
    self.txt_preview = Tkinter.Text(self.mainFrame)
    self.txt_preview.grid(row = 4, columnspan = 3)
    #the Next Button
    self.btn_next = Tkinter.Button(self.mainFrame, text = "Next",command = self.btnNextBehaviour)
    self.btn_next.grid(row = 5, column = 2, sticky = Tkinter.E)
    
  def createCASSelect(self):
    """
    Has the user reached this window, he has already decided which problems he
    wants to deal with. Now he selects the Computer Algebra Systems on which the
    calculations should be perfomed. Additionally, he sets his machine settings
    """
    self.mainWindow.geometry("%dx%d%+d%+d" % (375, 375, 40, 40))
    #Top Label
    self.lbl_computerAlgebraSelect = Tkinter.Label(self.mainFrame, text = "Choose the computer algebra systems\n\
on which your calculations should be performed")
    self.lbl_computerAlgebraSelect.grid(row = 0, columnspan = 2)
    #Checkbox select of the computer algebra systems.
    #GAP
    self.var_GAP = Tkinter.StringVar()
    self.var_GAP.set("No")
    self.cb_GAP = Tkinter.Checkbutton(self.mainFrame,text = "GAP", variable = self.var_GAP,onvalue="Yes", offvalue = "No")
    self.cb_GAP.deselect()
    self.cb_GAP.grid(row = 1, columnspan = 2, sticky = Tkinter.W)
    #Magma
    self.var_Magma = Tkinter.StringVar()
    self.var_Magma.set("No")
    self.cb_Magma = Tkinter.Checkbutton(self.mainFrame,text = "Magma", variable = self.var_Magma,onvalue="Yes", offvalue = "No")
    self.cb_Magma.deselect()
    self.cb_Magma.grid(row = 2, columnspan = 2, sticky = Tkinter.W)
    #Maple
    self.var_Maple = Tkinter.StringVar()
    self.var_Maple.set("No")
    self.cb_Maple = Tkinter.Checkbutton(self.mainFrame,text = "Maple", variable = self.var_Maple,onvalue="Yes", offvalue = "No")
    self.cb_Maple.deselect()
    self.cb_Maple.grid(row = 3, columnspan = 2, sticky = Tkinter.W)
    #Singular
    self.var_Singular = Tkinter.StringVar()
    self.var_Singular.set("No")
    self.cb_Singular = Tkinter.Checkbutton(self.mainFrame,text = "Singular", variable = self.var_Singular,onvalue="Yes", offvalue = "No")
    self.cb_Singular.deselect()
    self.cb_Singular.grid(row = 4, columnspan = 2, sticky = Tkinter.W)
    ############
    #Now the Machine Settings.
    self.lbl_MachineSettings = Tkinter.Label(self.mainFrame, text = "Please enter the command line calls for\n\
the local machine to call the following programs:")
    self.lbl_MachineSettings.grid(row = 5, columnspan = 2)
    #GAP
    self.lbl_GAP = Tkinter.Label(self.mainFrame, text = "GAP:")
    self.lbl_GAP.grid(row = 6, column = 0, sticky = Tkinter.E)
    self.entry_GAP = Tkinter.Entry(self.mainFrame)
    self.entry_GAP.config(width = 10)
    self.entry_GAP.grid(row = 6,column = 1, sticky = Tkinter.W)
    #Magma
    self.lbl_Magma = Tkinter.Label(self.mainFrame, text = "Magma:")
    self.lbl_Magma.grid(row = 7, column = 0, sticky = Tkinter.E)
    self.entry_Magma = Tkinter.Entry(self.mainFrame)
    self.entry_Magma.config(width = 10)
    self.entry_Magma.grid(row = 7,column = 1, sticky = Tkinter.W)
    #Maple
    self.lbl_Maple = Tkinter.Label(self.mainFrame, text = "Maple:")
    self.lbl_Maple.grid(row = 8, column = 0, sticky = Tkinter.E)
    self.entry_Maple = Tkinter.Entry(self.mainFrame)
    self.entry_Maple.config(width = 10)
    self.entry_Maple.grid(row = 8,column = 1, sticky = Tkinter.W)
    #Singular
    self.lbl_Singular = Tkinter.Label(self.mainFrame, text = "Singular:")
    self.lbl_Singular.grid(row = 9, column = 0, sticky = Tkinter.E)
    self.entry_Singular = Tkinter.Entry(self.mainFrame)
    self.entry_Singular.config(width = 10)
    self.entry_Singular.grid(row = 9,column = 1, sticky = Tkinter.W)
    #The Time Command:
    self.lbl_Time = Tkinter.Label(self.mainFrame, text = "Time:")
    self.lbl_Time.grid(row = 10, column = 0, sticky = Tkinter.E)
    self.entry_Time = Tkinter.Entry(self.mainFrame)
    self.entry_Time.config(width = 10)
    self.entry_Time.grid(row = 10,column = 1, sticky = Tkinter.W)
    #Filename to be saved
    self.lbl_name = Tkinter.Label(self.mainFrame, text = "Name of your generated task:")
    self.lbl_name.grid(row = 11, column = 0, sticky = Tkinter.E)
    self.entry_taskName = Tkinter.Entry(self.mainFrame)
    self.entry_taskName.grid(row = 11, column = 1, sticky = Tkinter.W)
    ############  
    #Back and Finish Button
    #self.btn_Back = Tkinter.Button(self.mainFrame, text = "Back", command = self.btnBackBehaviour)
    #self.btn_Back.grid(row = 12, column = 0, sticky = Tkinter.W)
    self.btn_CreateExportFolder = Tkinter.Button(self.mainFrame, text = "Create Export Folder", command = self.btnCreateClick)
    self.btn_CreateExportFolder.grid(row = 12, column = 1, sticky = Tkinter.E)
    
CreateTasksGui()