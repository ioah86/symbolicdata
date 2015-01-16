import unittest
from ProceedingsFromXMLBuilder import ProceedingsFromXMLBuilder
from ..Task import Task

class TestProceedingsFromXMLBuilder(unittest.TestCase):
    """
    Tests for the class ProceedingsFromXMLBuilder

    .. moduleauthor:: Albert Heinle <aheinle@uwaterloo.ca>
    """

    def setUp(self):
        #First, define the task we are working with
        testName = "PrettyTestTask"
        testComputationProblem = "PrettierComputationProblem"
        testSDTables = ["sdtable1", "sdtable2", "sdtable3", "sdtable4"]
        testPIs = ["PI1", "PI2"]
        testCASs = ["cas1", "cas2"]
        self.testTask = Task(testName, testComputationProblem, testSDTables, testPIs, testCASs)
        #Now, we give some sample XML strings
        #totally invalid XML:
        self.xml1 = "bla bli blubb"
        #valid xml, but nothing useful for us:
        self.xml2 = """<?xml version="1.0" ?><RunTaskOptions><maxCPU>7200</maxCPU><maxMem>1024</maxMem><maxJobs>8</maxJobs></RunTaskOptions>"""
        #Valid xml, but not valid entries in the completed or erroneous section
        self.xml3= """
        <?xml version="1.0" ?>
        <proceedings>
            <timestamp>
              123456
            </timestamp>
            <task>
              PrettyTestTask
            </task>
            <running/>
            <waiting>
              "same as running"
            </waiting>
            <completed>
              <entry>
              </entry>
            </completed>
            <error>
              <entry>
              </entry>
            </error>
          </proceedings>
        """
        #completely valid Proceedings xml file, no entries for erroneous stuff.
        self.xml4 = """
        <?xml version="1.0" ?>
        <proceedings>
            <timestamp>
              123456
            </timestamp>
            <task>
              PrettyTestTask
            </task>
            <running/>
            <waiting>
              <entry>
                <probleminstance>
                  PI1
                </probleminstance>
                <computeralgebrasystem>
                  cas1
                </computeralgebrasystem>
              </entry>
              <entry>
                <probleminstance>
                  PI2
                </probleminstance>
                <computeralgebrasystem>
                  cas1
                </computeralgebrasystem>
              </entry>
              <entry>
                <probleminstance>
                  PI1
                </probleminstance>
                <computeralgebrasystem>
                  cas2
                </computeralgebrasystem>
              </entry>
              <entry>
                <probleminstance>
                  PI2
                </probleminstance>
                <computeralgebrasystem>
                  cas2
                </computeralgebrasystem>
              </entry>
            </waiting>
            <completed/>
            <error/>
          </proceedings>
        """

if __name__=="__main__":
    unittest.main()
