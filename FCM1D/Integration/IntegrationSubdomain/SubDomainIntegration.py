from Integration.IntegrationSubdomain.LocalToGlobal import LocalToGlobal
from Integration.IntegrationSubdomain.calcDeterminantJacobian import calcDeterminantJacobian
from Integration.IntegrationSubdomain.calcDetJacobiandomain import calcDetJacobianDomain
from Integration.GaussQuadrature.GaussWeights import GaussQuadratureWeights
from Integration.GaussQuadrature.GaussCoordinates import GaussQuadratureCoordinates

def SubDomainIntegration(subdomain, integrand, element):
    # the polynomial degree is redefined here, which is not an efficient way since it is defined in the model code,
    # the structure will be eased in the following upgrades
    # if you want, you can modify this code to handle this
    PolynomialDegree = 15
    NGP = PolynomialDegree+1
    # the gauss points of the corresponding subdomain is obtained !
    # the gauss points are constructed as like in the FCMLAB code, please refer to readme file for the reference !
    localPoints = GaussQuadratureCoordinates(NGP)
    localWeights = GaussQuadratureWeights(NGP)
    # the points and weights of the subdomains gauss points, that will be integrated to find the result, will be stored !
    points = []
    weights = []
    # the integration points are first mapped to the element
    point, weight = getIntegrationPoint(localPoints[0], localWeights[0], subdomain, element)
    # the integration results is obtained !
    intresult = integrand(point)*weight
    points.append(point)
    weights.append(weight)
    # the subdomains integrations points are further obtained
    for i in range(1, len(localPoints)):
        point, weight = getIntegrationPoint(localPoints[i], localWeights[i], subdomain, element)
        intresult += integrand(point) * weight
        points.append(point)
        weights.append(weight)
    return intresult

def getIntegrationPoint(localPoint, localWeights, subDomain, element):
    # in this function the integration points will be obtained via mapping the gauss points to the each sub-domain
    # the global coordinates of the element
    a = element.global_coordinates
    # the integration point of the corresponding gauss point
    point = LocalToGlobal(localPoint, subDomain)
    # the integration weight of the corresponding integration point
    weight = localWeights * calcDeterminantJacobian(localPoint, subDomain) * calcDetJacobianDomain(a, point)
    return point, weight