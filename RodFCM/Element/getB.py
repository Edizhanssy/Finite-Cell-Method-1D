
import numpy as np
from Element.ShapeFunctions.calcDerivativeofShapeFunction import evalDerivOfShapeFunct
def getB(Coord, PolynomialOrder, element):

    B = np.zeros([1, PolynomialOrder])

    Jacobian = JacobianAtCenter(element)

    B[0, 0:PolynomialOrder] = evalDerivOfShapeFunct(PolynomialOrder-1, Coord)/Jacobian

    return B

def JacobianAtCenter(element):

    FirstVertexCoordinates = element.global_coordinates[0]
    SecondVertexCoordinates = element.global_coordinates[1]

    J = 0.5 * (SecondVertexCoordinates - FirstVertexCoordinates)

    return J









