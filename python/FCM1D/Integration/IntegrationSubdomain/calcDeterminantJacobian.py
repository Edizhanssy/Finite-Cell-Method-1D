import numpy as np

def calcDeterminantJacobian(subdomain, localCoords):
    detJ = 0.5 * np.linalg.norm(localCoords[0]-localCoords[1])
    return detJ


