from INTPS import INTPS
import xml.dom.minidom as dom

class INTPSFromXMLBuilder(object):
    """
    This class serves the purpose to create an INTPS instances from  given XML-Files.
    
    @author:  Albert Heinle
    @contact: albert.heinle@rwth-aachen.de
    """

    def __init__(self, sdTable):
        """
        This is the constructor of the INTPSFromXMLBuilder. One only needs to provide the SDTable where
        the INTPS-instances are found.

        @param sdTable: The table that contains all the INTPS-instances
        @type  sdTable: SDTable
        """
        self.__sdTable = sdTable

    def build(self,name, xmlRaw=None):
        """
        The main command in this class. Given an raw xml-String containing an INTPS-instance.
        It creates an instance of type INTPS associated to the xml-string and returns it.

        @param   xmlRaw: The xml-Representation of the INTPS-Entry.
        @type    xmlRaw: string
        @param     name: The name of the INTPS-Entry
        @type      name: string
        @raises IOError: If something is wrong with the XMLstring this exception is raised.
        @returns:        An instance of INTPS associated to the xml Input string
        @rtype:          INTPS
        """
        #-------------------- Input Check --------------------
        try:
            if xmlRaw:
                xmlTree = dom.parseString(xmlRaw)
            else:
                xmlTree = dom.parseString(self.__sdTable.loadEntry(name))
        except:
            raise IOError("Could not parse the given string as XML-Instance")
        if (xmlTree.getElementsByTagName("vars") == []): # Check, if vars are there
            raise IOERROR("The given XMLString does not contain variables for the INTPS System")
        if (xmlTree.getElementsByTagName("basis") == []): # Check, if we have a basis
            raise IOERROR("The given XMLString does not contain a basis for the INTPS System")
        #-------------------- Input Check finished --------------------
        #From here, we can assume that the input is given correct
        variablesCSV = (xmlTree.getElementsByTagName("vars")[0]).firstChild.data
        variables = map(lambda x: str(x).strip(),variablesCSV.rsplit(","))
        polynomials = xmlTree.getElementsByTagName("basis")[0]
        basis = map(lambda poly: str(poly.firstChild.data).strip(),polynomials.getElementsByTagName("poly"))
        return INTPS(name, self.__sdTable, variables, basis)

    #TODO __del__
