import unittest
import copy
import FA_Q_dp
import GB_Fp_dp
import GB_Z_lp

class TestComputationProblems(unittest.TestCase):
    def test_FA_Q_dp(self):
        """
        This test tests the class FA_Q_dp for its stability.

        The covered tests are:
        1) FreeAlgebra is contained in the associated table list
        2) The name is FA_Q_dp
        3) The list of possible, applicable computer algebra systems should not be empty
           In fact, it should by now contain at least
           - Singular
           - Magma
           - GAP
        4) adding of an existing associated table does not change the table
        5) adding a non existing associated table works fine
        6) adding an existing computer algebra system does not change the table
        7) adding a non existing computer algebra system works find
        """
        #1)
        compProblem=FA_Q_dp.FA_Q_dp()
        self.assertTrue("FreeAlgebra" in compProblem.getAssociatedTables(),
                        "The standard table, \"FreeAlgebra\", was not contained\
 in the class FA_Q_dp")
        #2)
        self.assertEqual("FA_Q_dp", compProblem.getName(), "The class FA_Q_dp does not\
 return a correct name")
        #3)
        self.assertTrue("Singular" in compProblem.getPossibleComputerAlgebraSystems(),
                        "Singular is missing as a possible computer algebra system\
 solving FA_Q_dp")
        self.assertTrue("Magma" in compProblem.getPossibleComputerAlgebraSystems(),
                        "Magma is missing as a possible computer algebra system\
 solving FA_Q_dp")
        self.assertTrue("GAP" in compProblem.getPossibleComputerAlgebraSystems(),
                        "GAP is missing as a possible computer algebra system\
 solving FA_Q_dp")
        #4)
        temp = copy.deepcopy(compProblem.getAssociatedTables())
        compProblem.addToAssociatedTables(temp[0])
        self.assertTrue(set(temp)==set(compProblem.getAssociatedTables()),
                    "Adding of an existing table to the associated tables of FA_Q_dp\
 caused the list of associated tables to change.")
        #5)
        compProblem.addToAssociatedTables("RandomTableNeverWouldExistsBecauseOfSillyName")
        self.assertFalse(set(temp)==set(compProblem.getAssociatedTables()),
                            "Adding of associated table to FA_Q_dp failed.")
        #6)
        temp = copy.deepcopy(compProblem.getPossibleComputerAlgebraSystems())
        compProblem.addToComputerAlgebraSystems(temp[0])
        self.assertTrue(set(temp)==set(compProblem.getPossibleComputerAlgebraSystems()),
                    "Adding of an existing table to the possible computer algebra systems of FA_Q_dp\
 caused the list of associated tables to change.")
        #7)
        compProblem.addToComputerAlgebraSystems("RandomCASNeverWouldExistsBecauseOfSillyName")
        self.assertFalse(set(temp)==set(compProblem.getPossibleComputerAlgebraSystems()),
                            "Adding of associated table to FA_Q_dp failed.")
        

if __name__=="__main__":
    unittest.main()
