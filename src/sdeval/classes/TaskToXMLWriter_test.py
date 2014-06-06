import unittest
from TaskToXMLWriter import TaskToXMLWriter
from XMLRessources import XMLRessources

class TestTaskToXMLWriter(unittest.TestCase):
    """
    Tests for the class TaskToXMLWriter

    .. moduleauthor:: Albert Heinle <albert.heinle@uwaterloo.ca>
    """

    def setUp(self):
        xmlres = XMLRessources()
        testName = "PrettyTestTask"
        testComputationProblem = "GB_Z_lp"
        testSDTables = ["IntPS"]
        testPIs = ["Amrhein", "Becker-Niermann", "Bronstein-86"]
        testCASs = ["Singular", "Magma", "Maple"]
        self.testTask = Task(testName, testComputationProblem, testSDTables, testPIs, testCASs)

if __name__=="__main__":
    unittest.main()
