import unittest
import XMLRessources
import os

class TestXMLRessources(unittest.TestCase):
    """
    Tests for the class XMLRessources

    .. moduleauthor:: Albert Heinle <albert.heinle@uwaterloo.ca>
    """

    def setUp(self):
        """
        General Assumptions:
           - Tests run on top of Symbolic Data base, i.e. in the folder structure
             as given in the repository.
             Otherwise the user will be asked to either enter the path to the XMLResources folder
             or to skip the related tests (empty string entering).
        """
        self.xr = None
        try:
            tempPathToXMLRessources = str(os.path.realpath(os.path.dirname(__file__))).split(os.sep)[0:-3]
            self.xr = XMLRessources.XMLRessources(os.path.join(str(os.sep).join(tempPathToXMLRessources),"XMLResources"))
        except:
            tempPathToXMLRessources = raw_input("Path to XMLRessources not at the usual location. Please enter Path\
 to it or press Enter to skip tests related to the Symbolic Data source: ")
            if tempPathToXMLRessources != '':
                self.xr = XMLRessources.XMLRessources(os.path.join(str(os.sep).join(tempPathToXMLRessources),"XMLResources"))
        if self.xr ==None:
            print "WARNING: As the path to the XMLResources is not provided, all tests will be ignored"

    def testInitialization(self):
        """
        Tests the initialization of the class XMLRessources.

        In particular, we check for the following two cases:
        1) it is called with an invalid folder.
           1.1.) The folder does not exist
           1.2.) The folder does not contain a typical Symbolic Data table
        2) It is called without any argument.

        ASSUMPTIONS:
          - Test 2) needs the XMLRessources folder from the SymbolicData project
        """
        #1.1)
        try:
            XMLRessources.XMLResources(os.path.join(".","SillyNameThatWouldNeverAppearInOurProgram"))
            self.fail("Could instanciate XMLRessources with not existent path")
        except:
            pass
        #1.2)
        try:
            XMLRessources.XMLRessources(".")
            self.fail("Could instantiate XMLRessources instance with invalid path")
        except:
            pass
        #2)
        if self.xr != None:
            #This guarantees that we can call it with no arguments
            XMLRessources.XMLRessources()
        else:
            try:
                XMLResources.XMLRessources()
                self.fail("Could instantiate XMLRessources, even if the folder was not given correctly")
            except:
                pass


    def testLoadSDTable(self):
        """
        Tests whether an SDTable can be loaded or not.

        In particular, we will test the following:
        1) Load an existing Symbolic Data table
        2) Try to load a non-existing table

        GENERAL ASSUMPTIONS:
          - XMLRessources folder from the SymbolicData project is existent on the testing machine
        """
        if self.xr != None:
            #1)
            try:
                self.xr.loadSDTable("IntPS")
            except:
                self.fail("Failed to load an existing SDTable")
            #2)
            try:
                self.xr.loadSDTable("SillyNameForTableNeverWouldOccur")
                self.fail("Could load an invalid SDTable.")
            except:
                pass

if __name__=="__main__":
    unittest.main()
