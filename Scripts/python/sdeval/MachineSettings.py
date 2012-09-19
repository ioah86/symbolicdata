#!/usr/bin/env python
#Author: Albert Heinle
#Purpose: A database for local settings concerning e.g. paths to the computer
#         algebra systems a computation should be run through, etc.

import os
import xml.dom.minidom as dom

machineSettingsXmlFileName = "MachineSettings.xml"

#############
#First check, whether the XML-File is available that contains the machine settings
#information
if not os.path.isfile(machineSettingsXmlFileName):
  #### Filling the dict with default entries, because no XML file is available
  print "Error, no Machine Settings file could been found. Entries will be filled\
by default values."
  CASpaths={"Maple":"maple",
          "Singular":"Singular",
          "Magma":"magma",
          "GAP":"gap"}
  timeCommand = "/usr/bin/time -f \"real\\t%E\\nuser\\t%U\\nsystem\\t%S\""
else:
  ### A XML-File is available. Reading the entries
  MSTree = dom.parse(machineSettingsXmlFileName)
  CASpaths = {}
  timeCommand = ""
  ######
  #At first, fill the dictionary with the computer algebra systems.
  for element in MSTree.firstChild.childNodes:
    if element.nodeName.strip()=="CASdictionary":
      for entry in element.childNodes:
        if entry.nodeName.strip() == "entry":
          key = value = None
          for node in entry.childNodes:
            if node.nodeName.strip() =="key":
              key = node.firstChild.data.strip()
            elif node.nodeName.strip() == "value":
              value = node.firstChild.data.strip()
          CASpaths[key] = value
  ##### And now the Time command
    if element.nodeName.strip() == "OtherVars":
      for entry in element.childNodes:
        if entry.nodeName.strip() == "TimeCommand":
          timeCommand = entry.firstChild.data.strip()
