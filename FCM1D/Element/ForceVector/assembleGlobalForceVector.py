import numpy as np
from Element.ShapeFunctions.calcDerivativeofShapeFunction import evalShapeFunct
from Integration.IntegrationSubdomain.LocalToGlobal import LocalToGlobal
from Integration.IntegrationSubdomain.integrate import integrate

def calculate_element_force(element, cfg):
    def integrand_function(local_coordinates):
        N = evalShapeFunct(cfg.p, local_coordinates)
        x = LocalToGlobal(local_coordinates, element.global_coordinates)
        return N.reshape(-1, 1) * cfg.body_load(x)
    return integrate(integrand_function, element, cfg)


def assemble_Force_Vector(elements, DOF, LtoG, cfg):
    GlobalForce = np.zeros([DOF, 1])
    for i, element in enumerate(elements):
        Fe = calculate_element_force(element, cfg)
        loc = np.array(LtoG[i]).flatten()
        GlobalForce[loc, 0] += Fe.flatten()
    return GlobalForce
