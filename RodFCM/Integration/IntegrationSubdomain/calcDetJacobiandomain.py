import numpy as np


def calcDetJacobianDomain(subdomain, localCoord):

    detJ = 0.5 * np.linalg.norm(subdomain[0] - subdomain[1])

    return detJ