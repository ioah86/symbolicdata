import unittest
import os
from FreeAlgebra import FreeAlgebra
from ModPS import ModPS
from IntPS import IntPS
from IntPSFromXMLBuilder import IntPSFromXMLBuilder
from ModPSFromXMLBuilder import ModPSFromXMLBuilder
from FreeAlgebraFromXMLBuilder import FreeAlgebraFromXMLBuilder
from .. import XMLRessources
from .. import SDTable

class TestProblemInstances(unittest.TestCase):
    """
    Contains tests for the different problem instance classes, namely
    - FreeAlgebra
    - IntPS
    - ModPS
    In the same time, their XMLBuilder are tested, as they are constructed with the builders.

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
            tempPathToXMLRessources = str(os.path.realpath(os.path.dirname(__file__))).split(os.sep)[0:-4]
            self.xr = XMLRessources.XMLRessources(os.path.join(str(os.sep).join(tempPathToXMLRessources),"XMLResources"))
        except:
            tempPathToXMLRessources = raw_input("Path to XMLRessources not at the usual location. Please enter Path\
 to it or press Enter to skip tests related to the Symbolic Data source: ")
            if tempPathToXMLRessources != '':
                self.xr = XMLRessources.XMLRessources(os.path.join(str(os.sep).join(tempPathToXMLRessources),"XMLResources"))
        if self.xr ==None:
            print "WARNING: As the path to the XMLResources is not provided, some tests will be ignored"
    
    def test_FreeAlgebra(self):
        """
        This test tests the class FreeAlgebra for stability.
        The covered tests are:
         1.) Loading a valid entry, and checking if everything got parsed correctly. This includes
             1.a) The name is correct
             1.b) The correct variables
             1.c) The corect value for upToDeg
             1.d) The correct basis
             1.e) The correct string representation
             1.f) The correct SDTable is still there
        """
        sdt = SDTable.SDTable(None, (self.xr,"FreeAlgebra"))
        faBuilder = FreeAlgebraFromXMLBuilder(sdt)
        faInstance = faBuilder.build('h1')
        #1.a
        self.assertEqual(faInstance.getName(), 'h1', "Name in FreeAlgebra instance is not correct.")
        #1.b
        self.assertEqual(faInstance.getVars(),['u','v','U','V'], "Variables were not equal")
        #1.c
        self.assertEqual(faInstance.getUpToDeg(),14,"The uptodeg value was not correct")
        #1.d
        self.assertEqual(faInstance.getBasis(),['u*U-1', 'U*u-1',
            'v*V-1', 'V*v-1', 'v*U*v*v*U*v-1', 'U*v*U*v*U*v-1',
            'u*u*u*v*u*v*v*u*u*u*v*u*v*v-1'],"The basis was not correctly \
imported")
        #1e
        self.assertEqual(str(faInstance),"FreeAlgebra-Entry: h1\n\
Variables: u,v,U,V\n\
Up to degree: 14\n\
basis:\n\
u*U-1\n\
U*u-1\n\
v*V-1\n\
V*v-1\n\
v*U*v*v*U*v-1\n\
U*v*U*v*U*v-1\n\
u*u*u*v*u*v*v*u*u*u*v*u*v*v-1","String representation was not correct")
        #1.f
        self.assertEqual(faInstance.getSDTable(),sdt,"SDTable got altered")

    def test_ModPS(self):
        """
        This test tests the class ModPS for stability.
        The covered tests are:
         1.) Loading a valid entry, and checking if everything got parsed correctly. This includes
             1.a) The name is correct
             1.b) The correct variables
             1.c) The corect value for characteristic
             1.d) The correct basis
             1.e) The correct SDTable is still there
        """
        sdt = SDTable.SDTable(None, (self.xr,"ModPS"))
        modpsBuilder = ModPSFromXMLBuilder(sdt)
        modpsinstance = modpsBuilder.build("Curves.scurve7_18.Generators")
        #1.a
        self.assertEqual(modpsinstance.getName(),
                        'Curves.scurve7_18.Generators',
                        "Name in ModPS instance is not correct.")
        #1.b
        print modpsinstance.getName()
        self.assertEqual(modpsinstance.getVars(),['x0','x1','x2','x3','x4','x5','x6','x7'],
                         "Variables were not equal")
        #1.c
        self.assertEqual(modpsinstance.getCharacteristic(),31991,
                         "The characteristic of the ground field was not correct")
        #1.d
        self.assertEqual(modpsinstance.getBasis(),['x2*x3+14517*x3^2+17829*x0*x4+23141*x1*x4+14225*x2*x4+11871*x3*x4+1100*x4^2+23101*x0*x5+5948*x1*x5+14958*x2*x5+10877*x3*x5+17897*x4*x5+37*x5^2+30577*x0*x6+1522*x1*x6+11721*x2*x6+18163*x3*x6+20422*x4*x6+16065*x5*x6+16850*x6^2+24466*x0*x7+1380*x1*x7+23077*x2*x7+26027*x3*x7+20379*x4*x7+7053*x5*x7+27785*x6*x7+14894*x7^2',
'x1*x3+15967*x3^2+4222*x0*x4+17964*x1*x4+6679*x2*x4+30129*x3*x4+10875*x4^2+4971*x0*x5+4412*x1*x5+9953*x2*x5+26182*x3*x5+9668*x4*x5+10127*x5^2+10449*x0*x6+14311*x1*x6+18073*x2*x6+15935*x3*x6+21923*x4*x6+25082*x5*x6+5157*x6^2+12349*x0*x7+27294*x1*x7+29277*x2*x7+23783*x3*x7+15629*x4*x7+27442*x5*x7+11877*x6*x7+6152*x7^2',
'x0*x3+22981*x3^2+24236*x0*x4+6019*x1*x4+443*x2*x4+16168*x3*x4+16312*x4^2+14626*x0*x5+29047*x1*x5+25560*x2*x5+12894*x3*x5+8336*x4*x5+27722*x5^2+84*x0*x6+15582*x1*x6+16589*x2*x6+30260*x3*x6+8291*x4*x6+8576*x5*x6+31340*x6^2+25035*x0*x7+13334*x1*x7+21390*x2*x7+22679*x3*x7+31847*x4*x7+5472*x5*x7+17893*x6*x7+27148*x7^2',
'x2^2+22367*x3^2+30132*x0*x4+17105*x1*x4+28143*x2*x4+17414*x3*x4+26709*x4^2+20449*x0*x5+19961*x1*x5+30327*x2*x5+5369*x3*x5+2528*x4*x5+27386*x5^2+9830*x0*x6+15685*x1*x6+6007*x2*x6+14202*x3*x6+26913*x4*x6+30722*x5*x6+18217*x6^2+3571*x0*x7+11231*x1*x7+31494*x2*x7+14254*x3*x7+16293*x4*x7+27818*x5*x7+20162*x6*x7+17566*x7^2',
'x1*x2+2969*x3^2+4807*x0*x4+3072*x1*x4+26501*x2*x4+17662*x3*x4+14399*x4^2+22098*x0*x5+13687*x1*x5+27827*x2*x5+12787*x3*x5+17838*x4*x5+3480*x5^2+787*x0*x6+14396*x1*x6+2336*x2*x6+21841*x3*x6+19967*x4*x6+26344*x5*x6+20655*x6^2+4299*x0*x7+835*x1*x7+7317*x2*x7+5754*x3*x7+9319*x4*x7+423*x5*x7+983*x6*x7+17526*x7^2',
'x0*x2+485*x3^2+24616*x0*x4+6126*x1*x4+17543*x2*x4+452*x3*x4+20149*x4^2+23050*x0*x5+974*x1*x5+19293*x2*x5+22487*x3*x5+837*x4*x5+31989*x5^2+16168*x0*x6+8930*x1*x6+3166*x2*x6+4387*x3*x6+13760*x4*x6+17238*x5*x6+2263*x6^2+147*x0*x7+15961*x1*x7+23979*x2*x7+3695*x3*x7+24332*x4*x7+12098*x5*x7+27798*x6*x7+9977*x7^2',
'x1^2+6060*x3^2+23754*x0*x4+8853*x1*x4+16765*x2*x4+12490*x3*x4+14166*x4^2+8102*x0*x5+27999*x1*x5+27232*x2*x5+26576*x3*x5+23733*x4*x5+4610*x5^2+27849*x0*x6+3649*x1*x6+8666*x2*x6+66*x3*x6+16496*x4*x6+19301*x5*x6+30711*x6^2+4277*x0*x7+23479*x1*x7+11319*x2*x7+12730*x3*x7+29532*x4*x7+17792*x5*x7+22506*x6*x7+19160*x7^2',
'x0*x1+14292*x3^2+19859*x0*x4+6331*x1*x4+21405*x2*x4+7248*x3*x4+14283*x4^2+26450*x0*x5+9106*x1*x5+30520*x2*x5+10477*x3*x5+27325*x4*x5+31678*x5^2+7524*x0*x6+21768*x1*x6+6155*x2*x6+5031*x3*x6+10392*x4*x6+20238*x5*x6+31715*x6^2+10148*x0*x7+26776*x1*x7+5902*x2*x7+12642*x3*x7+6838*x4*x7+4474*x5*x7+25417*x6*x7+1888*x7^2',
'x0^2+7694*x3^2+23538*x0*x4+30855*x1*x4+12277*x2*x4+26294*x3*x4+24905*x4^2+29887*x0*x5+2934*x1*x5+23878*x2*x5+22173*x3*x5+19734*x4*x5+9565*x5^2+23306*x0*x6+22461*x1*x6+11306*x2*x6+21052*x3*x6+23811*x4*x6+28040*x5*x6+26033*x6^2+19240*x0*x7+7732*x1*x7+16521*x2*x7+11066*x3*x7+5627*x4*x7+14179*x5*x7+9904*x6*x7+5852*x7^2',
'x3^2*x6+7492*x0*x4*x6+19866*x1*x4*x6+7536*x2*x4*x6+28333*x3*x4*x6+25655*x4^2*x6+393*x0*x5*x6+2168*x1*x5*x6+2154*x2*x5*x6+28405*x3*x5*x6+27999*x4*x5*x6+18705*x5^2*x6+14015*x0*x6^2+8793*x1*x6^2+8900*x2*x6^2+11969*x3*x6^2+18170*x4*x6^2+18403*x5*x6^2+4923*x6^3+30922*x3^2*x7+24899*x0*x4*x7+17664*x1*x4*x7+30896*x2*x4*x7+30405*x3*x4*x7+27633*x4^2*x7+8217*x0*x5*x7+8209*x1*x5*x7+17787*x2*x5*x7+2918*x3*x5*x7+27605*x4*x5*x7+11555*x5^2*x7+22940*x0*x6*x7+8577*x1*x6*x7+28392*x2*x6*x7+11119*x3*x6*x7+25159*x4*x6*x7+14765*x5*x6*x7+13753*x6^2*x7+18017*x0*x7^2+30696*x1*x7^2+308*x2*x7^2+16951*x3*x7^2+11292*x4*x7^2+4394*x5*x7^2+18472*x6*x7^2+18368*x7^3',
'x3*x5^2+23218*x4*x5^2+25700*x5^3+3226*x0*x4*x6+18452*x1*x4*x6+22019*x2*x4*x6+1027*x3*x4*x6+1344*x4^2*x6+24166*x0*x5*x6+11087*x1*x5*x6+18103*x2*x5*x6+23425*x3*x5*x6+23148*x4*x5*x6+23715*x5^2*x6+24758*x0*x6^2+25772*x1*x6^2+17435*x2*x6^2+14992*x3*x6^2+21122*x4*x6^2+1426*x5*x6^2+2845*x6^3+21291*x3^2*x7+27529*x0*x4*x7+11230*x1*x4*x7+26631*x2*x4*x7+27997*x3*x4*x7+1204*x4^2*x7+2898*x0*x5*x7+21149*x1*x5*x7+6729*x2*x5*x7+15705*x3*x5*x7+7405*x4*x5*x7+29540*x5^2*x7+27357*x0*x6*x7+3944*x1*x6*x7+5365*x2*x6*x7+19353*x3*x6*x7+16054*x4*x6*x7+11253*x5*x6*x7+22651*x6^2*x7+8114*x0*x7^2+14569*x1*x7^2+2878*x2*x7^2+19419*x3*x7^2+19236*x4*x7^2+31286*x5*x7^2+6175*x6*x7^2+2872*x7^3',
'x2*x5^2+15256*x4*x5^2+29772*x5^3+30890*x0*x4*x6+17829*x1*x4*x6+502*x2*x4*x6+9192*x3*x4*x6+4912*x4^2*x6+16798*x0*x5*x6+3431*x1*x5*x6+14338*x2*x5*x6+31555*x3*x5*x6+26635*x4*x5*x6+24929*x5^2*x6+3768*x0*x6^2+13675*x1*x6^2+9553*x2*x6^2+20648*x3*x6^2+17960*x4*x6^2+3795*x5*x6^2+19209*x6^3+10247*x3^2*x7+18819*x0*x4*x7+18051*x1*x4*x7+4099*x2*x4*x7+1490*x3*x4*x7+8882*x4^2*x7+22183*x0*x5*x7+26723*x1*x5*x7+25577*x2*x5*x7+25551*x3*x5*x7+9158*x4*x5*x7+31108*x5^2*x7+9619*x0*x6*x7+29491*x1*x6*x7+8697*x2*x6*x7+26471*x3*x6*x7+15086*x4*x6*x7+20765*x5*x6*x7+5916*x6^2*x7+13383*x0*x7^2+16071*x1*x7^2+22800*x2*x7^2+6924*x3*x7^2+5057*x4*x7^2+4418*x5*x7^2+13518*x6*x7^2+27627*x7^3',
'x1*x5^2+8737*x4*x5^2+28470*x5^3+26746*x0*x4*x6+12543*x1*x4*x6+20089*x2*x4*x6+21025*x3*x4*x6+28843*x4^2*x6+17404*x0*x5*x6+4562*x1*x5*x6+24230*x2*x5*x6+2544*x3*x5*x6+372*x4*x5*x6+25685*x5^2*x6+10083*x0*x6^2+24916*x1*x6^2+8926*x2*x6^2+4964*x3*x6^2+8740*x4*x6^2+10252*x5*x6^2+22234*x6^3+12860*x3^2*x7+27133*x0*x4*x7+6887*x1*x4*x7+1304*x2*x4*x7+15754*x3*x4*x7+20487*x4^2*x7+2881*x0*x5*x7+5577*x1*x5*x7+6065*x2*x5*x7+17875*x3*x5*x7+13495*x4*x5*x7+21886*x5^2*x7+9276*x0*x6*x7+26567*x1*x6*x7+19846*x2*x6*x7+24878*x3*x6*x7+9768*x4*x6*x7+18904*x5*x6*x7+4409*x6^2*x7+8525*x0*x7^2+30481*x1*x7^2+14397*x2*x7^2+1039*x3*x7^2+20496*x4*x7^2+13961*x5*x7^2+14509*x6*x7^2+15258*x7^3',
'x0*x5^2+24835*x4*x5^2+4953*x5^3+301*x0*x4*x6+10545*x1*x4*x6+3476*x2*x4*x6+10924*x3*x4*x6+5485*x4^2*x6+9235*x0*x5*x6+18678*x1*x5*x6+15274*x2*x5*x6+28168*x3*x5*x6+25647*x4*x5*x6+2507*x5^2*x6+2801*x0*x6^2+1313*x1*x6^2+12659*x2*x6^2+19221*x3*x6^2+16336*x4*x6^2+15027*x5*x6^2+9654*x6^3+2960*x3^2*x7+13065*x0*x4*x7+11706*x1*x4*x7+8189*x2*x4*x7+20673*x3*x4*x7+5482*x4^2*x7+570*x0*x5*x7+15971*x1*x5*x7+3703*x2*x5*x7+14796*x3*x5*x7+30805*x4*x5*x7+17792*x5^2*x7+28145*x0*x6*x7+23791*x1*x6*x7+31233*x2*x6*x7+8636*x3*x6*x7+27796*x4*x6*x7+15968*x5*x6*x7+27206*x6^2*x7+16127*x0*x7^2+8819*x1*x7^2+18232*x2*x7^2+24431*x3*x7^2+13148*x4*x7^2+11165*x5*x7^2+10045*x6*x7^2+5010*x7^3',
'x4^2*x5+29471*x4*x5^2+28811*x5^3+8024*x0*x4*x6+28710*x1*x4*x6+12965*x2*x4*x6+1002*x3*x4*x6+17011*x4^2*x6+24574*x0*x5*x6+12683*x1*x5*x6+16728*x2*x5*x6+9067*x3*x5*x6+13601*x4*x5*x6+5403*x5^2*x6+24505*x0*x6^2+6978*x1*x6^2+14206*x2*x6^2+15492*x3*x6^2+26710*x4*x6^2+13058*x5*x6^2+2550*x6^3+12558*x3^2*x7+3190*x0*x4*x7+21581*x1*x4*x7+6043*x2*x4*x7+28889*x3*x4*x7+31088*x4^2*x7+6221*x0*x5*x7+28429*x1*x5*x7+8577*x2*x5*x7+28204*x3*x5*x7+24396*x4*x5*x7+11007*x5^2*x7+24147*x0*x6*x7+15978*x1*x6*x7+2302*x2*x6*x7+16092*x3*x6*x7+9161*x4*x6*x7+5132*x5*x6*x7+12177*x6^2*x7+30836*x0*x7^2+28135*x1*x7^2+15514*x2*x7^2+3219*x3*x7^2+17435*x4*x7^2+1531*x5*x7^2+13188*x6*x7^2+26838*x7^3',
'x3*x4*x5+3850*x4*x5^2+17229*x5^3+19983*x0*x4*x6+15439*x1*x4*x6+18908*x2*x4*x6+6325*x3*x4*x6+15016*x4^2*x6+4062*x0*x5*x6+18619*x1*x5*x6+10610*x2*x5*x6+5946*x3*x5*x6+7694*x4*x5*x6+16533*x5^2*x6+20655*x0*x6^2+29831*x1*x6^2+13414*x2*x6^2+15322*x3*x6^2+6406*x4*x6^2+30510*x5*x6^2+19735*x6^3+31576*x3^2*x7+14309*x0*x4*x7+22923*x1*x4*x7+19206*x2*x4*x7+14474*x3*x4*x7+19889*x4^2*x7+7176*x0*x5*x7+21993*x1*x5*x7+7991*x2*x5*x7+14080*x3*x5*x7+10309*x4*x5*x7+30571*x5^2*x7+11685*x0*x6*x7+7941*x1*x6*x7+9901*x2*x6*x7+14672*x3*x6*x7+24005*x4*x6*x7+24503*x5*x6*x7+8774*x6^2*x7+28585*x0*x7^2+23855*x1*x7^2+26148*x2*x7^2+31126*x3*x7^2+31103*x4*x7^2+31143*x5*x7^2+13547*x6*x7^2+20954*x7^3',
'x2*x4*x5+10307*x4*x5^2+445*x5^3+16057*x0*x4*x6+6598*x1*x4*x6+11849*x2*x4*x6+27671*x3*x4*x6+9884*x4^2*x6+2790*x0*x5*x6+13442*x1*x5*x6+7084*x2*x5*x6+25940*x3*x5*x6+5607*x4*x5*x6+14177*x5^2*x6+23165*x0*x6^2+17849*x1*x6^2+20451*x2*x6^2+2920*x3*x6^2+23512*x4*x6^2+11321*x5*x6^2+12965*x6^3+3134*x3^2*x7+5686*x0*x4*x7+15032*x1*x4*x7+4375*x2*x4*x7+18204*x3*x4*x7+3132*x4^2*x7+17691*x0*x5*x7+28692*x1*x5*x7+13163*x2*x5*x7+707*x3*x5*x7+25387*x4*x5*x7+25904*x5^2*x7+14194*x0*x6*x7+25974*x1*x6*x7+5589*x2*x6*x7+8604*x3*x6*x7+18689*x4*x6*x7+30518*x5*x6*x7+29705*x6^2*x7+29527*x0*x7^2+30337*x1*x7^2+9011*x2*x7^2+14231*x3*x7^2+26214*x4*x7^2+19547*x5*x7^2+4556*x6*x7^2+8558*x7^3'],"The \
basis was not correctly imported")
        #1.e
        self.assertEqual(modpsinstance.getSDTable(),sdt,"SDTable got altered")

    def test_IntPS(self):
        """
        This test tests the class FreeAlgebra for stability.
        The covered tests are:
        1.) Loading a valid entry, and checking if everything got parsed correctly. This includes
            1.a) The name is correct
            1.b) The correct variables
            1.c) The correct basis
            1.d) The correct string representation
            1.e) The correct SDTable is still there
        """
        sdt = SDTable.SDTable(None, (self.xr,"IntPS"))
        intpsbuilder = IntPSFromXMLBuilder(sdt)
        intpsinstance = intpsbuilder.build("Amrhein")
        #1.a
        self.assertEqual(intpsinstance.getName(), 'Amrhein', "Name in IntPS instance is not correct.")
        #1.b
        self.assertEqual(intpsinstance.getVars(),['a','b','c','d','e','f'], "Variables were not equal")
        #1.c
        self.assertEqual(intpsinstance.getBasis(),['2*f*b+2*e*c+d^2+a^2+a','2*f*c+2*e*d+2*b*a+b',
                                                   '2*f*d+e^2+2*c*a+c+b^2','2*f*e+2*d*a+d+2*c*b',
                                                   'f^2+2*e*a+e+2*d*b+c^2','2*f*a+f+2*e*b+2*d*c'],
                                                   "The basis was not correctly imported.")
        #1d
        self.assertEqual(str(intpsinstance),"IntPS-Entry: Amrhein\n\
Variables: a,b,c,d,e,f\n\
basis:\n\
2*f*b+2*e*c+d^2+a^2+a\n\
2*f*c+2*e*d+2*b*a+b\n\
2*f*d+e^2+2*c*a+c+b^2\n\
2*f*e+2*d*a+d+2*c*b\n\
f^2+2*e*a+e+2*d*b+c^2\n\
2*f*a+f+2*e*b+2*d*c","String representation was not correct")
        #1.e
        self.assertEqual(intpsinstance.getSDTable(),sdt,"SDTable got altered")
        
if __name__=="__main__":
    unittest.main()
