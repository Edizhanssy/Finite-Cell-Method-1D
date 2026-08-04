import numpy as np
from Element.StrainDisplacement import StrainDisplacement
from Integration.IntegrationSubdomain.LocalToGlobal import LocalToGlobal
from Integration.IntegrationSubdomain.integrate import integrate

def calculate_stiffness_matrix(element, cfg):
    def integrand_function(local_coordinates):
        B = StrainDisplacement(local_coordinates, element, cfg)
        GlobalCoord = LocalToGlobal(local_coordinates, element.global_coordinates)
        Mat = cfg.E * cfg.A * cfg.material_factor(cfg.domain_index(GlobalCoord))
        return np.dot(np.dot(B.T, Mat), B)
    return integrate(integrand_function, element, cfg)


def getMaterialMatrix(coord, MaterialID, materialMatrix):
    if MaterialID == 0:
        return materialMatrix
    elif MaterialID == 1:
        return 1e-8 * materialMatrix
    else:
        raise Exception('the domain is invalid !!')




