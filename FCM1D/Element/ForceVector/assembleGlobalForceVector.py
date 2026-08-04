import numpy as np
from Element.ShapeFunctions.calcDerivativeofShapeFunction import evalShapeFunct
from Integration.IntegrationSubdomain.LocalToGlobal import LocalToGlobal
from Integration.IntegrationSubdomain.integrate import integrate


def bodyLoad(x):
    if 0.0 <= x <= 1.0:
        return np.sin(4.0 * np.pi * x) / 20.0
    return 0.0


def calculate_element_force(element, NGP):
    def integrand_function(local_coordinates):
        N = evalShapeFunct(NGP - 1, local_coordinates)
        x = LocalToGlobal(local_coordinates, element.global_coordinates)
        return N.reshape(-1, 1) * bodyLoad(x)
    return integrate(integrand_function, element)


def assemble_Force_Vector(elements, NumberOfGaussPoints, DOF, LtoG):
    GlobalForce = np.zeros([DOF, 1])
    for i, element in enumerate(elements):
        Fe = calculate_element_force(element, NumberOfGaussPoints)
        loc = np.array(LtoG[i]).flatten()
        GlobalForce[loc, 0] += Fe.flatten()
    return GlobalForce
