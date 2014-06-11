import unittest
from template import generateCode

class TestFA_Q_DPGAP(unittest.TestCase):
    """
    Tests for the template to generate executable code for calculating a
    Groebner basis of an ideal in a free algebra over Q.

    .. moduleauthor:: Albert Heinle <albert.heinle@uwaterloo.ca>
    """

    def test_Template(self):
        """
        This test checks the template FA_Q_DP for GAP.

        The covered test cases are:
        1. Create executable string and check for correctness
        """
        #1
        vars = ['x1','x2','x3','x4']
        basis=['x1+x2','x3*x4-x2','x1*x2*x3*x4']
        uptoDeg = 10;
        expectedString = """LoadPackage("GBNP","0",false);
SetInfoLevel(InfoGBNP,1);
SetInfoLevel(InfoGBNPTime,1);
F := Rationals;
A := FreeAssociativeAlgebraWithOne(F,"x4","x3","x2","x1");
g :=GeneratorsOfAlgebraWithOne(A);
x4 := g[1];
x3 := g[2];
x2 := g[3];
x1 := g[4];
weights := [1,1,1,1];
KI_gp := [x1+x2,x3*x4-x2,x1*x2*x3*x4];
KI_np :=GP2NPList(KI_gp);
GB :=SGrobnerTrunc(KI_np,10,weights);
GBNP.ConfigPrint("x4","x3","x2","x1");
PrintNPList(GB);
Length(GB);
quit;"""
        output = generateCode(vars,basis,uptoDeg)
        self.assertEqual(expectedString,output,
                         "Output string was different from what we expected.")
    

if __name__=="__main__":
    unittest.main()
