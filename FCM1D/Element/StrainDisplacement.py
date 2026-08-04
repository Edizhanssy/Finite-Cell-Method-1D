import numpy as np
from Element.ShapeFunctions.calcDerivativeofShapeFunction import evalDerivOfShapeFunct


def StrainDisplacement(Coord, element, cfg):
    B = np.zeros([1, cfg.n_modes])
    B[0, :] = evalDerivOfShapeFunct(cfg.p, Coord) / CenterJacobian(element)
    return B


def CenterJacobian(element):
    x1, x2 = element.global_coordinates[0], element.global_coordinates[1]
    return 0.5 * (x2 - x1)









