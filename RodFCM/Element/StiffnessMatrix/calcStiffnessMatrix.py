import numpy as np
from Element.getB import getB
from Integration.IntegrationSubdomain.mapLocalToGlobal import mapLocalToGlobal
from Integration.IntegrationSubdomain.integrate import integrate

def calcStiffnessMatrix(element, PolynomialDegree):
    def getIntegrand(coord):
        B = getB(coord, PolynomialDegree, element)
        GlobalCoord = mapLocalToGlobal(coord, element.global_coordinates)
        MatID = getMaterialAtPoint(GlobalCoord, element)
        Mat = getMaterialMatrix(coord, MatID, 1)
        return np.dot(np.dot(B.T, Mat), B)  # B' * Mat * B

    return integrate(getIntegrand, element)

def getMaterialAtPoint(coord, element):

    matID = getDomainIndex(coord)
    return matID

def getDomainIndex(coord):
    # Initialize domain boundaries
    physical_domain1 = [0, 1, 0]
    physical_domain2 = [7/3, 3, 0]
    fictious_domain = [1, 7/3, 0]

    # Check if the point is in the physical domain 1
    if physical_domain1[0] <= coord <= physical_domain1[1]:
        value = 0  # Physical domain 1
    # Check if the point is in the fictitious domain
    elif fictious_domain[0] <= coord <= fictious_domain[1]:
        value = 1  # Fictitious domain
    # Check if the point is in the physical domain 2
    elif physical_domain2[0] <= coord <= physical_domain2[1]:
        value = 0  # Physical domain 2
    else:
        value = -1

    return value


def getMaterialMatrix(coord, MaterialID, materialMatrix):
    if MaterialID == 0:
        return materialMatrix
    elif MaterialID == 1:
        return 1e-8 * materialMatrix
    else:
        raise Exception('the domain is invalid !!')




