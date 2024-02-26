import numpy as np
from Element.ShapeFunctions.calcDerivativeofShapeFunction import evalDerivOfShapeFunct

# the stain-displacement matrix will be calculated in this function !
def StrainDisplacement(Coord, PolynomialOrder, element):
    B = np.zeros([1, PolynomialOrder])
    # the jacobian of the center of the element is obtained !
    # the jacobian is calculated at the center to simplify our process and provide good approximation for the
    # elemental matrices
    # Also, since we are dealing with linear-static analysis, the jacobian of the center of the element should be sufficient
    # for large-deformation, and Non-linear problems the jacobian calculation ba
    Jacobian = CenterJacobian(element)
    B[0, 0:PolynomialOrder] = evalDerivOfShapeFunct(PolynomialOrder-1, Coord)/Jacobian
    return B

def CenterJacobian(element):
    FirstCoordinates = element.global_coordinates[0]
    SecondCoordinates = element.global_coordinates[1]
    J = 0.5 * (SecondCoordinates - FirstCoordinates)
    return J









