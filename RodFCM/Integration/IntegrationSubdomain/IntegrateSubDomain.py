from Integration.IntegrationSubdomain.mapLocalToGlobal import mapLocalToGlobal
from Integration.IntegrationSubdomain.calcDetJacobian import calcDetJacobian
from Integration.IntegrationSubdomain.calcDetJacobiandomain import calcDetJacobianDomain
from Integration.GaussQuadrature.GaussWeights import GaussQuadratureWeights
from Integration.GaussQuadrature.GaussCoordinates import GaussQuadratureCoordinates

def integrateSubDomain(subdomain, integrand, element):
    PolynomialDegree = 15
    NGP = PolynomialDegree+1
    localPoints = GaussQuadratureCoordinates(NGP)
    localWeights = GaussQuadratureWeights(NGP)

    points = []
    weights = []

    # the integration points are first mapped to the element
    point, weight = getCurrentIntegrationPoint(localPoints[0], localWeights[0], subdomain, element)
    result = integrand(point)*weight
    points.append(point)
    weights.append(weight)

    # the subdomains integrations points are further obtained
    for i in range(1, len(localPoints)):
        point, weight = getCurrentIntegrationPoint(localPoints[i], localWeights[i], subdomain, element)
        result = result + integrand(point) * weight
        points.append(point)
        weights.append(weight)

    return result

def getCurrentIntegrationPoint(localPoint, localWeights, subDomain, element):
    a = element.global_coordinates
    point = mapLocalToGlobal(localPoint, subDomain)
    weight = localWeights * calcDetJacobian(localPoint, subDomain) * calcDetJacobianDomain(a, point)

    return point, weight