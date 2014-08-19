"""
This is the template for the computation problem of computing a Groebner basis of an ideal
generated by a finite set of polynomials with coefficients in a finite field (commutative). It creates
code for the computer algebra system GAP.

.. moduleauthor:: Albert Heinle <albert.heinle@rwth-aachen.de>
"""

#--------------------------------------------------
#---------------The template-----------------------
#--------------------------------------------------

def generateCode(vars, basis,characteristic):
    """
    The main function generating the GAP code for the computation of
    the Groebner basis given the input variables.

    :param         vars: A list of variables used in the ModPS-System
    :type          vars: list
    :param        basis: The polynomials forming a basis of the ModPS-System. This input will not be checked whether
                         there are polynomials using variables not in the list of variables.
    :type         basis: list
    :param characteristic: The characteristic of the field where the coefficients are taken from.
    :type  characteristic: int
    """
    result = "\
F := GaloisField(%i);\n\
PR := PolynomialRing(F,[%s]);\n\
%s\n\
I:= Ideal(PR,[%s]);\n\
ord := MonomialGrlexOrdering(%s);\n\
B := GroebnerBasis(I,ord);\n\
Print(\"=====Solution Begin=====\");\n\
B;\n\
Print(\"=====Solution End=====\");\n\
quit;\
" % (characteristic,
    ",".join(str("\""+v+"\"") for v in vars),
     "\n".join(vars[i] + ":= IndeterminatesOfPolynomialRing(PR)[" + str(i+1)+"];" for i in range(len(vars))),
     ",".join(basis),
     ",".join(vars))
    return result

#--------------------------------------------------
#----------------Help Functions--------------------
#--------------------------------------------------
