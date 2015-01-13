import unittest
from RunTaskOptions import RunTaskOptions

class TestRunTaskOptions(unittest.TestCase):
    """
    Tests for the class RunTaskOptions

    .. moduleauthor:: Albert Heinle <albert.heinle@uwaterloo.ca>
    """

    def testInitialization(self):
        """
        This class tests the initialization of the RunTaskOptions class.
        In particular, the following test cases are covered:
        1. Initialization without any parameters (i.e. defaults values should be in)
        2. Initialization with maxCPU=None, but everything else set
        3. Initialization with maxMemory=None, but everything else is set
        4. Initialization with maxJobs=None, but everything else is set.
        5. Initialization with all three values set.
        6. Negative values:
           6.a. For maxCPU
           6.b. For maxMem
           6.c. For maxJobs
        """
        #1.
        t = RunTaskOptions()
        self.assertEqual(t.getMaxMem(), None, "Test 1. failed: maxMem should be None, but instead we have: %s"%str(t.getMaxMem()))
        self.assertEqual(t.getMaxCPU(), None, "Test 1. failed: maxCPU should be None, but instead we have: %s"%str(t.getMaxCPU()))
        self.assertEqual(t.getMaxJobs(), 1, "Test 1. failed: maxJobs should be 1, but instead we have: %s"%str(t.getMaxJobs()))
        #2.
        t = RunTaskOptions(maxMem=1024,maxJobs=4)
        self.assertEqual(t.getMaxMem(), 1024, "Test 2. failed: maxMem should be 1024, but instead we have: %s"%str(t.getMaxMem()))
        self.assertEqual(t.getMaxCPU(), None, "Test 2. failed: maxCPU should be None, but instead we have: %s"%str(t.getMaxCPU()))
        self.assertEqual(t.getMaxJobs(), 4, "Test 2. failed: maxJobs should be 4, but instead we have: %s"%str(t.getMaxJobs()))
        #3.
        t = RunTaskOptions(maxCPU=7200,maxJobs=6)
        self.assertEqual(t.getMaxMem(), None, "Test 2. failed: maxMem should be 1024, but instead we have: %s"%str(t.getMaxMem()))
        self.assertEqual(t.getMaxCPU(), 7200, "Test 2. failed: maxCPU should be None, but instead we have: %s"%str(t.getMaxCPU()))
        self.assertEqual(t.getMaxJobs(), 6, "Test 2. failed: maxJobs should be 4, but instead we have: %s"%str(t.getMaxJobs()))
        #4.
        t = RunTaskOptions(maxCPU=7200,maxMem=128)
        self.assertEqual(t.getMaxMem(), 128, "Test 2. failed: maxMem should be 1024, but instead we have: %s"%str(t.getMaxMem()))
        self.assertEqual(t.getMaxCPU(), 7200, "Test 2. failed: maxCPU should be None, but instead we have: %s"%str(t.getMaxCPU()))
        self.assertEqual(t.getMaxJobs(), 1, "Test 2. failed: maxJobs should be 4, but instead we have: %s"%str(t.getMaxJobs()))
        #5.
        t = RunTaskOptions(maxCPU=7200,maxMem=256,maxJobs=2)
        self.assertEqual(t.getMaxMem(), 256, "Test 2. failed: maxMem should be 1024, but instead we have: %s"%str(t.getMaxMem()))
        self.assertEqual(t.getMaxCPU(), 7200, "Test 2. failed: maxCPU should be None, but instead we have: %s"%str(t.getMaxCPU()))
        self.assertEqual(t.getMaxJobs(), 2, "Test 2. failed: maxJobs should be 4, but instead we have: %s"%str(t.getMaxJobs()))
        #6a.
        testPassed = True
        try:
            t = RunTaskOptions(maxCPU=-1,maxMem=256,maxJobs=2)
            testPassed = False
        except:
            pass
        if not testPassed:
            self.fail("Test 6.a. failed: Was able to assign -1 to maxCPU")
        #6b.
        try:
            t = RunTaskOptions(maxCPU=10,maxMem=0,maxJobs=2)
            testPassed = False
        except:
            pass
        if not testPassed:
            self.fail("Test 6.b. failed: Was able to assign -1 to maxMem")
        #6c.
        try:
            t = RunTaskOptions(maxCPU=10,maxMem=10,maxJobs=-10000)
            testPassed = False
        except:
            pass
        if not testPassed:
            self.fail("Test 6.c. failed: Was able to assign -10000 to maxJobs")
