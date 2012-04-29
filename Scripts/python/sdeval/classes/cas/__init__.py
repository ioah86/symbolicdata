#TODO:ALL the Imports here.

from CAS_Singular import CAS_Singular
from CAS_Maple import CAS_Maple
from CAS_Magma import CAS_Magma
from CAS_GAP import CAS_GAP


import xml.dom.minidom as dom
import MachineSettings as MS
import commands
from CAS import CAS

def getCASInstanceByXMLName(name):
    """
    In general, a user just knows the symbolic Data XML-File of a certain
    Computer algebra System. This function gets the name of the CAS as argument,
    and returns an instance of the built-in class as output.
    """
    if (name == "Singular.xml"):
        return CAS_Singular()
    elif (name == "Maple.xml"):
        return CAS_Maple()
    elif (name == "Magma.xml"):
        return CAS_Magma()
    elif (name == "GAP.xml"):
        return CAS_GAP()
    else:
        return None
    #TODO add all the others
