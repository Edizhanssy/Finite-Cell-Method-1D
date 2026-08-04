import numpy as np
from Element.ShapeFunctions.calcDerivativeofShapeFunction import evalShapeFunct


def calculate_element_force(element, cfg, quad):
    Fe = None
    for xi, w, xg in zip(quad.xi, quad.w, quad.x):
        N = evalShapeFunct(cfg.p, xi)
        contribution = N.reshape(-1, 1) * cfg.body_load(xg) * w
        Fe = contribution if Fe is None else Fe + contribution
    return Fe


def assemble_Force_Vector(elements, DOF, LtoG, cfg, quads):
    GlobalForce = np.zeros([DOF, 1])
    for i, element in enumerate(elements):
        Fe = calculate_element_force(element, cfg, quads[i])
        loc = np.array(LtoG[i]).flatten()
        GlobalForce[loc, 0] += Fe.flatten()
    return GlobalForce
