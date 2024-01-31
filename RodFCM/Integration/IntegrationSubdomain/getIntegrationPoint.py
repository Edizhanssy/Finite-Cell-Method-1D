from Integration.IntegrationSubdomain.mapLocalToGlobal import mapLocalToGlobal
from Integration.IntegrationSubdomain.calcDetJacobian import calcDetJacobian
from Integration.IntegrationSubdomain.calcDetJacobiandomain import calcDetJacobianDomain
def getIntegrationPoint(element, subdomain):

    localPoints = subdomain.gaussPoints
    localWeights = subdomain.gaussWeights

    points = []
    weights = []

    # the integration points are first mapped to the element
    point, weight = getCurrentIntegrationPoint(localPoints[0], localWeights[0], subdomain, element)
    points.append(point)
    weights.append(weight)

    # the subdomains integrations points are further obtained
    for i in range(1, len(localPoints)):
        point, weight = getCurrentIntegrationPoint(localPoints[i], localWeights[i], subdomain, element)
        points.append(point)
        weights.append(weight)

    return points, weights

def getCurrentIntegrationPoint(localPoint, localWeights, subDomain, element):
    a = element.global_coordinates
    point = mapLocalToGlobal(subDomain, localPoint, element)
    weight = localWeights * calcDetJacobian(subDomain, localPoint) * calcDetJacobianDomain(a, point)

    return point, weight




