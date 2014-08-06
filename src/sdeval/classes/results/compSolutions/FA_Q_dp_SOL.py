class FA_Q_dp_SOL():
    """
    This class represents the solution of the Groebner basis calculation with respect
    to the degree-lexicographic ordering, given generators of an ideal in the free algebra.

    The solution is represented by a list of generators of the ideal. In our case,
    we provide a list of strings, each representing a generator.

    .. moduleauthor:: Albert Heinle <aheinle@uwaterloo.ca>
    """

    def __init__(self, basis, originalGenerators=[],variables=[], upToDeg=0):
        """
        The constructor of the FA_Q_dp_SOL class. It consumes a parameter basis,
        which is a list of strings, where each string represents an element of the
        groebner basis of the original ideal.

        Optionally, also the original generators, the variable list and the degree,
        up to which the generators were calculated, is provided.

        :param basis: A list of strings, representing the calculated Groebner Basis
        :type  basis: list of string
        :param originalGenerators: A list of strings, representing the original generators
                                   of the considered ideal. If not specified, empty list.
        :type  originalGenerators: list of string
        :param variables: A list of strings, representing the variables that appear in the
                     free algebra. If not specified, empty list.
        :type variables: list of string
        :param upToDeg: Represents the degree, up to which the Groebner basis was calculated.
                        If not specified, zero.
        :type  upToDeg: int
        :raises TypeError: In case, one of the inputs were not of correct type
        """
        #Input Check
        if type(basis)!=list or type(originalGenerators)!=list
            or type(variables)!=list or type(upToDeg)!=int:
            raise TypeError("One of the input parameters of FA_Q_dp_SOL did not have the correct type")

        for i in basis:
            if type(i) != str:
                raise TypeError("The elements in the parameter basis were not of type string")
        for i in originalGenerators:
            if type(i) != str:
                raise TypeError("The elements in the parameter originalGenerators were not of type string")
        for i in variables:
            if type(i) != str:
                raise TypeError("The elements in the parameter variables were not of type string")
        #Input Check Done
        self.__basis = basis
        self.__originalGenerators = originalGenerators
        self.__vars = variables
        self.__upToDeg = upToDeg
