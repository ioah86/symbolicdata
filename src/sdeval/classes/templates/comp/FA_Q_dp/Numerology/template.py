"""
This is the template for the computation problem of computing a Groebner basis of an
ideal in a free algebra over QQ in the computeralgebra system Singular.

.. moduleauthor:: Albert Heinle <albert.heinle@rwth-aachen.de>
"""

#--------------------------------------------------
#---------------The template-----------------------
#--------------------------------------------------

def generateCode(vars, basis, uptoDeg):
    """
    The main function generating the Singular code for the computation of
    the Groebner basis given the input variables.

    :param         vars: A list of variables used in the FreeAlgebra-System
    :type          vars: list
    :param        basis: a GB calculated uptoDeg (will not be checked)
    :type         basis: list
    :param      uptoDeg: The uptoDeg Entry.
    :type       uptoDeg: unsigned int
    """
    result = ""
    result += "LIB \"freegb.lib\";\n"
    result += "LIB \"fpadim.lib\";\n"
    result += "ring r = 0,(%s),dp;\n" % ",".join(vars)
    result += "int d = %i;\n" % uptoDeg
    result += "def R = makeLetterplaceRing(d);\n setring(R);\n"
    ideal = ",\n".join(FAPolyToSingularStyle(v,vars) for v in basis)
    result += "ideal I = %s;\n" % ideal
    result += "list L = lpDHilbert(I);\n"
    result += "print(\"=====Solution Begin=====\");\n"
    result += "size(I);\n"
    result += "print(L[1]);\n"
    result += "print(L[2]);\n"
    result += "print(\"=====Solution End=====\");$;"
    return result

#--------------------------------------------------
#----------------Help Functions--------------------
#--------------------------------------------------

def FAPolyToSingularStyle(poly,variables):
        """
        Input: A Polynomial (Freealgebra) in the MAGMA-Style, and the variables
               in the corresponding free algebra
        Output: A Polynomial in the Letterplace Style (with their positions as
                arguments)
        :param      poly: The polynomial given in MAGMA-Style
        :type       poly: string
        :param variables: A list containing the occurring variables.
        :type  variables: list
        """
        result = ""
        plusSplit = poly.split("+")
        for p in plusSplit:
            minusSplit = p.split("-")
            for ms in minusSplit:
                monomials = ms.split("*")
                i = 1
                for m in monomials:
                    if m.strip() not in variables: #Coefficient
                        result += m+"*"
                        continue
                    m = m.strip()+"("+str(i)+")"
                    result += m.strip()+"*"
                    i=i+1
                result = result[:-1] #one * too much
                result += "-"
            result = result[:-1]
            result += "+"
        result = result[:-1]
        return result

# vim: set tabstop=4 shiftwidth=4 expandtab :
