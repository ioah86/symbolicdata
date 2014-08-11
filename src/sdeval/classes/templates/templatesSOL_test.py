import unittest

from comp.FA_Q_dp.Singular.template_sol import extractSolution
from comp.FA_Q_dp.Singular.template_sol import convertFromLetterplace

class TestTemplatesSOL(unittest.TestCase):
    """
    Tests for the different templates to extract the solution from the
    output of the computer algebra systems.

    .. moduleauthor:: Albert Heinle <albert.heinle@uwaterloo.ca>
    """

    def test_FA_Q_dp_Singular_Sol(self):
        """
        Here, we are testing the template to extract the solution from
        the Singular output on a FA_Q_dp-instance, i.e. the
        computation of a Groebner basis over the free algebra.

        The module consists of two functions:
        1.) extractSolution(outpString)
        2.) convertFromLetterplace(inpPoly):
        
        We test both functions here. The covered test cases are:
        1.1.) extractSolution on invalid inputs
        1.1.a) Wrong datatype
        1.1.b) String without the "=====Solution Begin=====" and
               "=====Solution End=====" tags.
        1.1.c) String with the "=====Solution Begin=====" tag, but not
               with the "=====Solution End=====" tag
        1.1.d) String with the "=====Solution End=====" tag, but not
               with the "=====Solution Begin=====" tag
        1.1.e) String with both the "=====Solution Begin=====" and the
               "=====Solution End=====" tag, but with whitespace in
               between.
        1.2.) extractSolution on valid inputs
        1.2.a) String with The solution right after "=====Solution
               Begin=====" tag, and ending right at "=====Solution
               End====="
        1.2.b) Solution given really by Singular.
        2.1) Giving a string where nothing needs to be replaced (1 as
             solution e.g.)
        2.2) Polynomial with "-" at the front
        2.3) Polynomial with multiple monomials
        2.4) Polynomial with alternating + and - signs.
        """
        testPassed = 1
        solBeginStr = "=====Solution Begin====="
        solEndStr   = "=====Solution End====="
        #1.1.a)
        try:
            extractSolution(1)
            testPassed = 0
        except:
            pass
        if not testPassed:
            self.fail("I was able to try to extract a solution from an \
int.")
        #1.1.b)
        try:
            extractSolution("abc123")
            testPassed = 0
        except:
            pass
        if not testPassed:
            self.fail("Invalid solution string did not cause \
exception")
        #1.1.c)
        try:
            extractSolution(solBeginStr + "\n\n abc123")
            testPassed = 0
        except:
            pass
        if not testPassed:
            self.fail("Could parse a string with begin, but not with \
end tag.")
        #1.1.d)
        try:
            extractSolution("abc123" + solEndStr)
            testPassed = 0
        except:
            pass
        if not testPassed:
            self.fail("Could parse a string with end, but not with \
begin tag")
        #1.1.e)
        try:
            extractSolution(solBeginStr +" " +solEndStr)
            testPassed = 0
        except:
            pass
        if not testPassed:
            self.fail("Could parse a string with no solution in \
between begin and end tag.")
        #1.2.a)
        try:
            tempRes = extractSolution(solBeginStr + "x(1)" + solEndStr)
        except:
            self.fail("Could not accept a solution with no whitespace \
between the begin and the end tag")
        expectedOutp = """<?xml version="1.0" ?>
<FA_Q_dp_SOL>
  <basis>
    <polynomial>x</polynomial>
  </basis>
</FA_Q_dp_SOL>
"""
        self.assertEqual(tempRes,expectedOutp, "XML string did not \
match for 1.2.a)")
        #1.2.b
        singularOutput = """                     SINGULAR                                 /
 A Computer Algebra System for Polynomial Computations       /   version 3-1-7
                                                           0<
 by: W. Decker, G.-M. Greuel, G. Pfister, H. Schoenemann     \   Aug 2013
FB Mathematik der Universitaet, D-67653 Kaiserslautern        \
// ** loaded /Applications/Singular/3-1-7/LIB/freegb.lib (3-1-7-0,Sep_2013)
// ** loaded /Applications/Singular/3-1-7/LIB/bfun.lib (3-1-7-0,Sep_2013)
// ** loaded /Applications/Singular/3-1-7/LIB/presolve.lib (3-1-7-0,Sep_2013)
// ** loaded /Applications/Singular/3-1-7/LIB/elim.lib (3-1-7-0,Sep_2013)
// ** loaded /Applications/Singular/3-1-7/LIB/poly.lib (3-1-7-0,Sep_2013)
// ** loaded /Applications/Singular/3-1-7/LIB/ring.lib (3-1-7-0,Sep_2013)
// ** loaded /Applications/Singular/3-1-7/LIB/primdec.lib (3-1-7-0,Jan_2014)
// ** loaded /Applications/Singular/3-1-7/LIB/absfact.lib (3-1-7-0,Sep_2013)
// ** loaded /Applications/Singular/3-1-7/LIB/triang.lib (3-1-7-0,Sep_2013)
// ** loaded /Applications/Singular/3-1-7/LIB/random.lib (3-1-7-0,Sep_2013)
// ** loaded /Applications/Singular/3-1-7/LIB/matrix.lib (3-1-7-0,Sep_2013)
// ** loaded /Applications/Singular/3-1-7/LIB/general.lib (3-1-7-0,Sep_2013)
// ** loaded /Applications/Singular/3-1-7/LIB/inout.lib (3-1-7-0,Sep_2013)
// ** loaded /Applications/Singular/3-1-7/LIB/nctools.lib (3-1-7-0,Sep_2013)
// ** loaded /Applications/Singular/3-1-7/LIB/dmodapp.lib (3-1-7-0,Sep_2013)
// ** loaded /Applications/Singular/3-1-7/LIB/sing.lib (3-1-7-0,Sep_2013)
// ** loaded /Applications/Singular/3-1-7/LIB/gkdim.lib (3-1-7-0,Sep_2013)
// ** loaded /Applications/Singular/3-1-7/LIB/dmod.lib (3-1-7-1,jan_2014)
// ** loaded /Applications/Singular/3-1-7/LIB/control.lib (3-1-7-0,Sep_2013)
// ** loaded /Applications/Singular/3-1-7/LIB/homolog.lib (3-1-7-0,Sep_2013)
// ** loaded /Applications/Singular/3-1-7/LIB/deform.lib (3-1-7-0,Sep_2013)
// ** loaded /Applications/Singular/3-1-7/LIB/gmssing.lib (3-1-7-0,Sep_2013)
// ** loaded /Applications/Singular/3-1-7/LIB/linalg.lib (3-1-7-0,Sep_2013)
// ** loaded /Applications/Singular/3-1-7/LIB/qhmoduli.lib (3-1-7-0,Sep_2013)
// ** loaded /Applications/Singular/3-1-7/LIB/rinvar.lib (3-1-7-0,Sep_2013)
// ** loaded /Applications/Singular/3-1-7/LIB/zeroset.lib (3-1-7-0,Sep_2013)
// ** loaded /Applications/Singular/3-1-7/LIB/primitiv.lib (3-1-7-0,Sep_2013)
[3:15]2(5)s(4)s(5)s(6)sss3(8)s(9)s(12)s(16)s(18)s(21)s(27)s(30)s(37)s4(48)s(55)s(64)s(73)s(82)--s(92)s(101)s(110)s(119)s(129)s(139)s(151)-s(164)s(178)s(193)s(208)s(223)-s(237)s(252)--s(265)-s(275)----5-----------------------------------------------------------------------(200)---------------------------------------------------------------------6-------------------------------(100)------------------------------------------------7----------------------------------------------------
(S:34)----------------------------------
product criterion:825 chain criterion:110
shift V criterion:3755
=====Solution Begin=====
x2(1)*x1(2)+4*x1(1)*x2(2)-3*x1(1)*x1(2),x2(1)*x2(2)-4*x1(1)*x3(2)+54*x1(1)*x2(2)-40*x1(1)*x1(2),x3(1)*x3(2)-9*x3(1)*x2(2)+2*x1(1)*x4(2)+x1(1)*x1(2),17*x4(1)*x2(2)-41*x1(1)*x4(2)-20*x1(1)*x3(2)+270*x1(1)*x2(2)-200*x1(1)*x1(2),17*x4(1)*x3(2)+204*x4(1)*x1(2)-153*x3(1)*x4(2)+68*x3(1)*x2(2)+697*x3(1)*x1(2)+414*x1(1)*x4(2)+260*x1(1)*x3(2)-3527*x1(1)*x2(2)+2600*x1(1)*x1(2),17*x4(1)*x4(2)-1042*x1(1)*x4(2)-602*x1(1)*x3(2)+6597*x1(1)*x2(2)-4983*x1(1)*x1(2),4*x1(1)*x3(2)*x1(3)-64*x1(1)*x1(2)*x3(3)+1044*x1(1)*x1(2)*x2(3)-735*x1(1)*x1(2)*x1(3),2*x1(1)*x3(2)*x2(3)+8*x1(1)*x2(2)*x3(3)-546*x1(1)*x1(2)*x3(3)+7071*x1(1)*x1(2)*x2(3)-5220*x1(1)*x1(2)*x1(3),306*x3(1)*x2(2)*x3(3)+68*x3(1)*x1(2)*x4(3)-11016*x3(1)*x1(2)*x3(3)+148716*x3(1)*x1(2)*x2(3)-110126*x3(1)*x1(2)*x1(3)+816*x1(1)*x4(2)*x1(3)-612*x1(1)*x3(2)*x4(3)-1088*x1(1)*x2(2)*x3(3)+3132*x1(1)*x1(2)*x4(3)+120590*x1(1)*x1(2)*x3(3)-1712846*x1(1)*x1(2)*x2(3)+1239815*x1(1)*x1(2)*x1(3),4945294458*x3(1)*x2(2)*x4(3)-11590928206*x3(1)*x1(2)*x4(3)-16154463546*x3(1)*x1(2)*x3(3)+292437150876*x3(1)*x1(2)*x2(3)-220005283238*x3(1)*x1(2)*x1(3)+1136470308*x1(1)*x4(2)*x1(3)-2875259808*x1(1)*x3(2)*x4(3)+25990312050*x1(1)*x2(2)*x4(3)-293454954050*x1(1)*x2(2)*x3(3)-37682827965*x1(1)*x1(2)*x4(3)+16792204874504*x1(1)*x1(2)*x3(3)-215661366909620*x1(1)*x1(2)*x2(3)+159500235636143*x1(1)*x1(2)*x1(3),168140011572*x3(1)*x4(2)*x1(3)-2016140964916*x3(1)*x1(2)*x4(3)-1263283387704*x3(1)*x1(2)*x3(3)+13710091274100*x3(1)*x1(2)*x2(3)-11177637711968*x3(1)*x1(2)*x1(3)-2456678073810*x1(1)*x4(2)*x1(3)-988966678500*x1(1)*x3(2)*x4(3)+13446943729218*x1(1)*x2(2)*x4(3)-136417952624228*x1(1)*x2(2)*x3(3)-849620756475*x1(1)*x1(2)*x4(3)+7763955728363828*x1(1)*x1(2)*x3(3)-99574514167841120*x1(1)*x1(2)*x2(3)+73663405211507060*x1(1)*x1(2)*x1(3),154037*x4(1)*x1(2)*x1(3)-1285965*x1(1)*x4(2)*x1(3)-839188*x1(1)*x3(2)*x4(3)+9196218*x1(1)*x2(2)*x4(3)-85464304*x1(1)*x2(2)*x3(3)-6756349*x1(1)*x1(2)*x4(3)+4878039136*x1(1)*x1(2)*x3(3)-62608070032*x1(1)*x1(2)*x2(3)+46309301943*x1(1)*x1(2)*x1(3),616148*x4(1)*x1(2)*x2(3)-3486394*x1(1)*x4(2)*x1(3)-2517564*x1(1)*x3(2)*x4(3)+27588654*x1(1)*x2(2)*x4(3)-256392912*x1(1)*x2(2)*x3(3)-20269047*x1(1)*x1(2)*x4(3)+14637016928*x1(1)*x1(2)*x3(3)-187861722636*x1(1)*x1(2)*x2(3)+138955677794*x1(1)*x1(2)*x1(3),1232296*x4(1)*x1(2)*x3(3)+8744562*x1(1)*x4(2)*x1(3)-839188*x1(1)*x3(2)*x4(3)+9196218*x1(1)*x2(2)*x4(3)-84014544*x1(1)*x2(2)*x3(3)-8548295*x1(1)*x1(2)*x4(3)+4876077696*x1(1)*x1(2)*x3(3)-62595544532*x1(1)*x1(2)*x2(3)+46300152998*x1(1)*x1(2)*x1(3),11849*x4(1)*x1(2)*x4(3)+689112*x1(1)*x2(2)*x3(3)-717869*x1(1)*x1(2)*x4(3)-39847742*x1(1)*x1(2)*x3(3)+510679730*x1(1)*x1(2)*x2(3)-377804060*x1(1)*x1(2)*x1(3),x1(1)*x1(2)*x1(3)*x1(4),x1(1)*x1(2)*x1(3)*x2(4),x1(1)*x1(2)*x1(3)*x3(4),x1(1)*x1(2)*x1(3)*x4(4),x1(1)*x1(2)*x2(3)*x3(4),x1(1)*x1(2)*x2(3)*x4(4),x1(1)*x1(2)*x3(3)*x4(4),x1(1)*x1(2)*x4(3)*x1(4),x1(1)*x2(2)*x3(3)*x1(4),x1(1)*x2(2)*x3(3)*x2(4),x1(1)*x2(2)*x3(3)*x4(4),x1(1)*x2(2)*x4(3)*x1(4),x3(1)*x1(2)*x1(3)*x1(4),x3(1)*x1(2)*x1(3)*x2(4),x3(1)*x1(2)*x1(3)*x3(4),x3(1)*x1(2)*x1(3)*x4(4),x3(1)*x1(2)*x2(3)*x3(4),x3(1)*x1(2)*x2(3)*x4(4),x3(1)*x1(2)*x3(3)*x4(4),x3(1)*x1(2)*x4(3)*x1(4)
=====Solution End=====

$Bye.
real 1.58
user 1.52
sys 0.04"""
        try:
            tempRes = extractSolution(singularOutput)
        except:
            self.fail("Could not parse valid Singular output string")
        expectedOutp = """<?xml version="1.0" ?>
<FA_Q_dp_SOL>
  <basis>
    <polynomial>x2*x1+4*x1*x2-3*x1*x1</polynomial>
    <polynomial>x2*x2-4*x1*x3+54*x1*x2-40*x1*x1</polynomial>
    <polynomial>x3*x3-9*x3*x2+2*x1*x4+x1*x1</polynomial>
    <polynomial>17*x4*x2-41*x1*x4-20*x1*x3+270*x1*x2-200*x1*x1</polynomial>
    <polynomial>17*x4*x3+204*x4*x1-153*x3*x4+68*x3*x2+697*x3*x1+414*x1*x4+260*x1*x3-3527*x1*x2+2600*x1*x1</polynomial>
    <polynomial>17*x4*x4-1042*x1*x4-602*x1*x3+6597*x1*x2-4983*x1*x1</polynomial>
    <polynomial>4*x1*x3*x1-64*x1*x1*x3+1044*x1*x1*x2-735*x1*x1*x1</polynomial>
    <polynomial>2*x1*x3*x2+8*x1*x2*x3-546*x1*x1*x3+7071*x1*x1*x2-5220*x1*x1*x1</polynomial>
    <polynomial>306*x3*x2*x3+68*x3*x1*x4-11016*x3*x1*x3+148716*x3*x1*x2-110126*x3*x1*x1+816*x1*x4*x1-612*x1*x3*x4-1088*x1*x2*x3+3132*x1*x1*x4+120590*x1*x1*x3-1712846*x1*x1*x2+1239815*x1*x1*x1</polynomial>
    <polynomial>4945294458*x3*x2*x4-11590928206*x3*x1*x4-16154463546*x3*x1*x3+292437150876*x3*x1*x2-220005283238*x3*x1*x1+1136470308*x1*x4*x1-2875259808*x1*x3*x4+25990312050*x1*x2*x4-293454954050*x1*x2*x3-37682827965*x1*x1*x4+16792204874504*x1*x1*x3-215661366909620*x1*x1*x2+159500235636143*x1*x1*x1</polynomial>
    <polynomial>168140011572*x3*x4*x1-2016140964916*x3*x1*x4-1263283387704*x3*x1*x3+13710091274100*x3*x1*x2-11177637711968*x3*x1*x1-2456678073810*x1*x4*x1-988966678500*x1*x3*x4+13446943729218*x1*x2*x4-136417952624228*x1*x2*x3-849620756475*x1*x1*x4+7763955728363828*x1*x1*x3-99574514167841120*x1*x1*x2+73663405211507060*x1*x1*x1</polynomial>
    <polynomial>154037*x4*x1*x1-1285965*x1*x4*x1-839188*x1*x3*x4+9196218*x1*x2*x4-85464304*x1*x2*x3-6756349*x1*x1*x4+4878039136*x1*x1*x3-62608070032*x1*x1*x2+46309301943*x1*x1*x1</polynomial>
    <polynomial>616148*x4*x1*x2-3486394*x1*x4*x1-2517564*x1*x3*x4+27588654*x1*x2*x4-256392912*x1*x2*x3-20269047*x1*x1*x4+14637016928*x1*x1*x3-187861722636*x1*x1*x2+138955677794*x1*x1*x1</polynomial>
    <polynomial>1232296*x4*x1*x3+8744562*x1*x4*x1-839188*x1*x3*x4+9196218*x1*x2*x4-84014544*x1*x2*x3-8548295*x1*x1*x4+4876077696*x1*x1*x3-62595544532*x1*x1*x2+46300152998*x1*x1*x1</polynomial>
    <polynomial>11849*x4*x1*x4+689112*x1*x2*x3-717869*x1*x1*x4-39847742*x1*x1*x3+510679730*x1*x1*x2-377804060*x1*x1*x1</polynomial>
    <polynomial>x1*x1*x1*x1</polynomial>
    <polynomial>x1*x1*x1*x2</polynomial>
    <polynomial>x1*x1*x1*x3</polynomial>
    <polynomial>x1*x1*x1*x4</polynomial>
    <polynomial>x1*x1*x2*x3</polynomial>
    <polynomial>x1*x1*x2*x4</polynomial>
    <polynomial>x1*x1*x3*x4</polynomial>
    <polynomial>x1*x1*x4*x1</polynomial>
    <polynomial>x1*x2*x3*x1</polynomial>
    <polynomial>x1*x2*x3*x2</polynomial>
    <polynomial>x1*x2*x3*x4</polynomial>
    <polynomial>x1*x2*x4*x1</polynomial>
    <polynomial>x3*x1*x1*x1</polynomial>
    <polynomial>x3*x1*x1*x2</polynomial>
    <polynomial>x3*x1*x1*x3</polynomial>
    <polynomial>x3*x1*x1*x4</polynomial>
    <polynomial>x3*x1*x2*x3</polynomial>
    <polynomial>x3*x1*x2*x4</polynomial>
    <polynomial>x3*x1*x3*x4</polynomial>
    <polynomial>x3*x1*x4*x1</polynomial>
  </basis>
</FA_Q_dp_SOL>
"""
        self.assertEqual(tempRes,expectedOutp, "Output strings did not \
match for Singular output parse.")
        #2.1.a)
        self.assertEqual("1", convertFromLetterplace("1"), "Could not \
parse a single number")
        self.assertEqual("-1", convertFromLetterplace("-1"), "Could not \
parse a negative number")
        #2.2)
        self.assertEqual("-x", convertFromLetterplace("-x(1)"), "Could \
not parse a polynomial with negative sign.")
        #2.3)
        self.assertEqual("x*y*x + z*y",
                         convertFromLetterplace("x(1)*y(2)*x(3) + \
z(1)*y(2)"),
                         "Could not parse a polynomial consisting of \
multiple monomials")
        #2.4
        self.assertEqual("x*y*z + z - z*y +x*y - y",
                         convertFromLetterplace("x(1)*y(2)*z(3) + z(1) \
- z(1)*y(2) +x(1)*y(2) - y(1)"),
                         "Could not parse polynomial with alternating signs")

if __name__=="__main__":
    unittest.main()
