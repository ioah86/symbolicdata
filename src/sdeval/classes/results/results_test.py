import unittest
from Proceedings import Proceedings
from ..Task import Task

class TestProblemInstances(unittest.TestCase):
    """
    Contains tests for the results-files. These do the following
    - Keeping track of which processes are currently running, waiting, completed or raised an error.
    - If the tests completed, then the consumed time is produced.
    - Writing human readable HTML and machine-readable XML files for displaying the status.

    .. moduleauthor:: Albert Heinle <albert.heinle@uwaterloo.ca>
    """

    def setUp(self):
        """
        The setup for all the tests. We usually will need a Task-instance and a timestamp. Those are created here.
        """
        testName = "PrettyTestTask"
        testComputationProblem = "PrettierComputationProblem"
        testSDTables = ["sdtable1", "sdtable2", "sdtable3", "sdtable4"]
        testPIs = ["PI1", "PI2", "PI3", "PI4"]
        testCASs = ["cas1", "cas2", "cas3", "cas4"]
        self.testTask = Task(testName, testComputationProblem, testSDTables, testPIs, testCASs)
        self.testTimeStamp = "201405161350"

    def test_Proceedings(self):
        """
        This tests checks the correctness of the Proceedings class. The following tests are covered:
        1. Creation of Proceedings with None as the task (fail)
        2. Creation of Proceedings with an integer as task (fail)
        3. Creation of Proceedings with None as timestamp (fail)
        4. Creation of Proceedings with an integer as timestamp (fail)
        5. Correct initialization of the proceedings
           5.1. Test the initial set
           5.2. Test the getters
           5.3. Test setRunning with incorrect value
           5.4. Test setRunning with correct value
           5.5. Test setCompleted with incorrect value
           5.6. Test setCompleted with correct value
           5.7. Test setERROR with incorrect value
           5.8. Test setERROR with correct value.
        """
        #1.
        try:
            prcdngs = Proceedings(None, self.testTimeStamp)
            self.fail("Could create Proceedings with no Task")
        except:
            pass
        #2.
        try:
            prcdngs = Proceedings(1, self.testTimeStamp)
            self.fail("Could create Proceedings with 1 as Task")
        except:
            pass
        #3.
        try:
            prcdngs = Proceedings(self.testTask, None)
            self.fail("Could create Proceedings with None as timestamp")
        except:
            pass
        #4.
        try:
            prcdngs = Proceedings(self.testTask, 1)
            self.fail("Could create Proceedings with 1 as timestamp")
        except:
            pass
        #5.
        prcdngs = Proceedings(self.testTask, self.testTimeStamp)
        #5.1
        self.assertEqual(len(prcdngs.getWAITING()),16,"Number of waiting processes was not correct")
        self.assertEqual(prcdngs.getRUNNING(),[],"Running processes initially wrong")
        self.assertEqual(prcdngs.getCOMPLETED(),[],"Completed processes initially wrong")
        self.assertEqual(prcdngs.getERROR(),[], "Erroneous processes initially wrong")
        #5.2
        self.assertEqual(prcdngs.getTask(), self.testTask.getName(), "Initialization with wrong task performed")
        self.assertEqual(prcdngs.getTimeStamp(), self.testTimeStamp, "Initialization with wrong timeStamp")
        #5.3
        prcdngs.setRUNNING("abc")
        self.assertEqual(len(prcdngs.getWAITING()),16,"invalid setRunning changed WAITING list.")
        self.assertEqual(prcdngs.getRUNNING(),[],"invalid setRunning changed RUNNING list.")
        self.assertEqual(prcdngs.getCOMPLETED(),[],"invalid setRunning changed COMPLETED list.")
        self.assertEqual(prcdngs.getERROR(),[], "invalid setRunning changed ERROR list.")
        #5.4
        prcdngs.setRUNNING(["PI1","cas1"])
        self.assertEqual(len(prcdngs.getWAITING()),15,"setRunning changed WAITING list wrongly.")
        self.assertEqual(prcdngs.getRUNNING(),[["PI1","cas1"]],"setRunning did not affect RUNNING list.")
        self.assertEqual(prcdngs.getCOMPLETED(),[],"setRunning changed COMPLETED list.")
        self.assertEqual(prcdngs.getERROR(),[], "setRunning changed ERROR list.")
        #5.5
        prcdngs.setCOMPLETED("abc")
        self.assertEqual(len(prcdngs.getWAITING()),15,"invalid setCompleted changed WAITING list wrongly.")
        self.assertEqual(prcdngs.getRUNNING(),[["PI1","cas1"]],"invalid setCompleted changed RUNNING list.")
        self.assertEqual(prcdngs.getCOMPLETED(),[],"invalid setCompleted changed COMPLETED list.")
        self.assertEqual(prcdngs.getERROR(),[], "invalid setCompleted changed ERROR list.")
        #5.6
        prcdngs.setCOMPLETED(["PI1","cas1"])
        self.assertEqual(len(prcdngs.getWAITING()),15,"setCompleted changed WAITING list.")
        self.assertEqual(prcdngs.getRUNNING(),[],"setCompleted changed RUNNING list wrongly.")
        self.assertEqual(prcdngs.getCOMPLETED(),[["PI1","cas1"]],"setCompleted did not change COMPLETED list.")
        self.assertEqual(prcdngs.getERROR(),[], "setCompleted changed ERROR list.")
        #5.7
        prcdngs.setERROR(["PI1","cas1"])
        self.assertEqual(len(prcdngs.getWAITING()),15,"invalid setERROR changed WAITING list.")
        self.assertEqual(prcdngs.getRUNNING(),[],"invalid setERROR changed RUNNING list.")
        self.assertEqual(prcdngs.getCOMPLETED(),[["PI1","cas1"]],"invalid setERROR changed COMPLETED list.")
        self.assertEqual(prcdngs.getERROR(),[], "invalid serERROR changed ERROR list.")
        #5.8
        prcdngs.setRUNNING(["PI2","cas1"])
        prcdngs.setERROR(["PI2", "cas1"])
        self.assertEqual(len(prcdngs.getWAITING()),14,"setERROR changed WAITING list.")
        self.assertEqual(prcdngs.getRUNNING(),[],"setERROR changed RUNNING list wrongly.")
        self.assertEqual(prcdngs.getCOMPLETED(),[["PI1","cas1"]],"setERROR changed COMPLETED list.")
        self.assertEqual(prcdngs.getERROR(),[["PI2", "cas1"]], "setERROR changed ERROR list wrongly.")

if __name__=="__main__":
    unittest.main()
