
import numpy as np
def calcDetJacobian(subdomain, localCoord):
    detJ = 0.5 * np.linalg.norm(localCoord[0]-localCoord[1])
    return detJ


